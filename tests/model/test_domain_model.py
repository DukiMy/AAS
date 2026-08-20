# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

from pathlib import Path

import pytest
from PIL import Image

from aas.events.events import (
    ChangeBrightness,
    ChangeContrast,
    ChangeHeight,
    ChangeWidth,
    ControllerEvent,
    DisplayAsciiRendering,
    DisplaySessionInfo,
    DisplayWarning,
    ExitRequested,
    ImageInfoRequested,
    ImageSummary,
    LoadImageRequested,
    LoadSessionRequested,
    ModelEvent,
    RenderRequested,
    SaveSessionRequested
)
from aas.exceptions.load_error import LoadError
from aas.model.domain_model import AASModel
from aas.model.image_state import ImageState
from aas.model.loader.image_loader import ImageLoader
from aas.model.renderer.ascii_renderer import AsciiRenderer
from aas.model.session_serializer import (
    SerializedSession,
    SessionSerializer
)


class FakeObserver:
    """Collect model events for assertions."""

    def __init__(self) -> None:
        """Initialize event collection."""
        self.events: list[ModelEvent] = []

    def on_model_event(self, event: ModelEvent) -> None:
        """Collect a model event."""
        self.events.append(event)


def _load_test_image(
    model: AASModel,
    monkeypatch: pytest.MonkeyPatch,
    alias: str | None = "cat"
) -> None:
    """Load a predictable in-memory image into the model."""
    image = Image.new("RGB", (100, 50))

    def fake_load(_self: ImageLoader, _path: str) -> Image.Image:
        return image

    monkeypatch.setattr(ImageLoader, "load", fake_load)

    model.on_controller_event(
        LoadImageRequested("cat.png", alias)
    )


def test_exit_request_is_forwarded() -> None:
    """Forward exit request to registered observer."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)
    model.on_controller_event(ExitRequested())

    assert observer.events == [ExitRequested()]


def test_calculate_height_preserves_proportions() -> None:
    """Calculate corrected ASCII height."""
    height = AASModel._calculate_height(
        width = 50,
        original_width = 100,
        original_height = 50
    )

    assert height == 12


def test_calculate_height_has_minimum_one() -> None:
    """Never calculate a height below one."""
    height = AASModel._calculate_height(
        width = 1,
        original_width = 1000,
        original_height = 1
    )

    assert height == 1


def test_unsupported_event_raises_type_error() -> None:
    """Reject events without a registered model handler."""
    model = AASModel()

    with pytest.raises(
        TypeError,
        match="Unsupported controller event: object",
    ):
        model.on_controller_event(object())


def test_brightness_unknown_image_warns() -> None:
    """Warn when brightness target cannot be found."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    model.on_controller_event(
        ChangeBrightness("missing", 2.0)
    )

    assert observer.events == [
        DisplayWarning("Image 'missing' not found.")
    ]


def test_contrast_unknown_image_warns() -> None:
    """Warn when contrast target cannot be found."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    model.on_controller_event(
        ChangeContrast("missing", 2.0)
    )

    assert observer.events == [
        DisplayWarning("Image 'missing' not found.")
    ]


def test_width_unknown_image_warns() -> None:
    """Warn when width target cannot be found."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    model.on_controller_event(
        ChangeWidth("missing", 2)
    )

    assert observer.events == [
        DisplayWarning("Image 'missing' not found.")
    ]


def test_height_unknown_image_warns() -> None:
    """Warn when height target cannot be found."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    model.on_controller_event(
        ChangeHeight("missing", 2)
    )

    assert observer.events == [
        DisplayWarning("Image 'missing' not found.")
    ]


def test_render_unknown_image_warns() -> None:
    """Warn when image to render cannot be found."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    model.on_controller_event(
        RenderRequested("missing", "destination")
    )

    assert observer.events == [
        DisplayWarning("No image available to render.")
    ]


def test_load_image_adds_image_to_session(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Load an image and expose it through session information."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    _load_test_image(model, monkeypatch)

    model.on_controller_event(ImageInfoRequested())

    assert observer.events == [
        DisplaySessionInfo(
            images = (
                ImageSummary(
                    name = "cat",
                    filename = "cat.png",
                    size=(100, 50),
                    target_size = (50, 12),
                    brightness = 1.0,
                    contrast = 1.0
                ),
            ),
            current="cat"
        )
    ]


def test_load_image_without_alias_uses_filename(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Use filename as image name when no alias is supplied."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    _load_test_image(model, monkeypatch, alias = None)

    model.on_controller_event(ImageInfoRequested())

    info = observer.events[-1]

    assert isinstance(info, DisplaySessionInfo)
    assert info.images[0].name == "cat.png"
    assert info.current == "cat.png"


def test_load_image_failure_warns(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Forward image loading errors as model warnings."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    def fake_load(_self: ImageLoader, _path: str) -> Image.Image:
        raise LoadError("Unable to load image.")

    monkeypatch.setattr(ImageLoader, "load", fake_load)

    model.on_controller_event(
        LoadImageRequested("missing.png")
    )

    assert observer.events == [
        DisplayWarning("Unable to load image.")
    ]


def test_find_image_by_filename(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Find an aliased image using its original filename."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    _load_test_image(model, monkeypatch)

    model.on_controller_event(
        ChangeBrightness("cat.png", 2.0)
    )

    model.on_controller_event(ImageInfoRequested())

    info = observer.events[-1]

    assert isinstance(info, DisplaySessionInfo)
    assert info.images[0].brightness == 2.0
    assert info.current == "cat"


@pytest.mark.parametrize(
    (
        "event",
        "expected_size",
        "expected_brightness",
        "expected_contrast"
    ),
    [
        (ChangeBrightness("cat", 2.0), (50, 12), 2.0, 1.0),
        (ChangeContrast("cat", 1.5), (50, 12), 1.0, 1.5),
        (ChangeWidth("cat", 80), (80, 20), 1.0, 1.0),
        (ChangeHeight("cat", 20), (80, 20), 1.0, 1.0)
    ]
)
def test_change_image_properties(
    event: ControllerEvent,
    expected_size: tuple[int, int],
    expected_brightness: float,
    expected_contrast: float,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Change rendering properties of a loaded image."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    _load_test_image(model, monkeypatch)

    model.on_controller_event(event)
    model.on_controller_event(ImageInfoRequested())

    info = observer.events[-1]

    assert isinstance(info, DisplaySessionInfo)

    summary = info.images[0]

    assert summary.target_size == expected_size
    assert summary.brightness == expected_brightness
    assert summary.contrast == expected_contrast


def test_render_current_image_notifies_observer(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Render current image and send result to observer."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    _load_test_image(model, monkeypatch)

    def fake_render(
        image: Image.Image,
        width: int,
        height: int,
        brightness: float = 1.0,
        contrast: float = 1.0,
    ) -> str:
        return "ASCII\n"

    monkeypatch.setattr(
        AsciiRenderer, "render", staticmethod(fake_render)
    )

    model.on_controller_event(RenderRequested())

    assert observer.events == [
        DisplayAsciiRendering("ASCII\n")
    ]


def test_render_to_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path
) -> None:
    """Write ASCII rendering to requested destination."""
    model = AASModel()

    _load_test_image(model, monkeypatch)

    def fake_render(
        image: Image.Image,
        width: int,
        height: int,
        brightness: float = 1.0,
        contrast: float = 1.0
    ) -> str:
        return "ASCII\n"

    monkeypatch.setattr(
        AsciiRenderer, "render", staticmethod(fake_render)
    )

    destination = tmp_path / "ascii.txt"

    model.on_controller_event(
        RenderRequested(
            image = "cat", destination = str(destination)
        )
    )

    assert destination.read_text(encoding="utf-8") == "ASCII\n"


def test_empty_session_info() -> None:
    """Report an empty session."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    model.on_controller_event(ImageInfoRequested())

    assert observer.events == [
        DisplaySessionInfo(images = (), current = None)
    ]


def test_save_session(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path
) -> None:
    """Save the current model session."""
    model = AASModel()

    _load_test_image(model, monkeypatch)

    filename = tmp_path / "session.json"

    model.on_controller_event(
        SaveSessionRequested(str(filename))
    )

    assert filename.exists()


def test_save_session_failure_warns(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Forward session saving errors as warnings."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    def fake_save(
        _filename: str,
        _images: dict[str, ImageState],
        _current: ImageState | None
    ) -> None:
        raise OSError("Disk full.")

    monkeypatch.setattr(
        SessionSerializer,
        "save",
        staticmethod(fake_save)
    )

    model.on_controller_event(SaveSessionRequested("session.json"))

    assert observer.events == [DisplayWarning("Disk full.")]


def test_load_session(monkeypatch: pytest.MonkeyPatch) -> None:
    """Restore images and current image from a session."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    session: SerializedSession = {
        "current": "cat",
        "images": {
            "cat": {
                "filename": "cat.png",
                "alias": "cat",
                "target_width": 80,
                "target_height": 20,
                "brightness": 1.5,
                "contrast": 0.8
            }
        }
    }

    def fake_session_load(_filename: str) -> SerializedSession:
        return session

    image = Image.new("RGB", (100, 50))

    def fake_image_load(
        _self: ImageLoader, _filename: str
    ) -> Image.Image:
        return image

    monkeypatch.setattr(
        SessionSerializer, "load", staticmethod(fake_session_load)
    )

    monkeypatch.setattr(ImageLoader, "load", fake_image_load)

    model.on_controller_event(LoadSessionRequested("session.json"))

    model.on_controller_event(ImageInfoRequested())

    assert observer.events == [
        DisplaySessionInfo(
            images = (
                ImageSummary(
                    name = "cat",
                    filename = "cat.png",
                    size = (100, 50),
                    target_size = (80, 20),
                    brightness = 1.5,
                    contrast = 0.8
                ),
            ),
            current="cat"
        )
    ]


def test_load_session_without_current_image(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Restore a session that has no current image."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    session: SerializedSession = {
        "current": None,
        "images": {}
    }

    def fake_session_load(_filename: str) -> SerializedSession:
        return session

    monkeypatch.setattr(
        SessionSerializer, "load", staticmethod(fake_session_load)
    )

    model.on_controller_event(
        LoadSessionRequested("session.json")
    )

    model.on_controller_event(ImageInfoRequested())

    assert observer.events == [
        DisplaySessionInfo(
            images = (),
            current=None
        )
    ]


@pytest.mark.parametrize(
    "exception",
    [
        OSError("Unable to read session."),
        LoadError("Unable to load image."),
        KeyError("images")
    ]
)
def test_load_session_failure_warns(
    exception: Exception,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Forward session loading failures as warnings."""
    model = AASModel()
    observer = FakeObserver()

    model.add_observer(observer)

    def fake_load(
        _filename: str,
    ) -> SerializedSession:
        raise exception

    monkeypatch.setattr(
        SessionSerializer,
        "load",
        staticmethod(fake_load),
    )

    model.on_controller_event(
        LoadSessionRequested("session.json")
    )

    assert observer.events == [
        DisplayWarning(str(exception))
    ]
