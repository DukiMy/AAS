# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Provide the AAS domain model."""

from functools import singledispatchmethod

from aas.events.events import (
    ChangeBrightness,
    ChangeContrast,
    ChangeHeight,
    ChangeWidth,
    ControllerEvent,
    DisplayAsciiRendering,
    DisplayNotice,
    DisplayNoticeRequested,
    DisplaySessionInfo,
    DisplayWarning,
    DisplayWarningRequested,
    ExitRequested,
    ImageInfoRequested,
    ImageSummary,
    LoadImageRequested,
    LoadSessionRequested,
    ModelEvent,
    RenderRequested,
    SaveSessionRequested
)

from aas.events.protocols import ModelObserver
from aas.exceptions.load_error import LoadError
from aas.model.image_state import ImageState
from aas.model.loader.image_loader import ImageLoader
from aas.model.renderer.ascii_renderer import AsciiRenderer
from aas.model.session_serializer import SessionSerializer

class AASModel:
    """Represent AAS domain state."""

    DEFAULT_WIDTH = 50

    def __init__(self) -> None:
        """Initialize model."""

        # Session state
        self._images: dict[str, ImageState] = {}
        self._current: ImageState | None = None

        # Services
        self._image_loader = ImageLoader()
        self._ascii_renderer = AsciiRenderer()
        self._session_serializer = SessionSerializer()

        # Observers
        self._observers: list[ModelObserver] = []

    def add_observer(self, observer: ModelObserver) -> None:
        """Register observer.

        Param observer:
            An observer of this models events.

        """
        self._observers.append(observer)

    def _notify_observers(self, event: ModelEvent) -> None:
        """Notify registered observers.

        Param event:
            A modelevent that will be sent to the observers.

        """
        for observer in self._observers:
            observer.on_model_event(event)

    def _find_image(self, name: str | None) -> ImageState | None:
        """Find image and make it current.

        Param name:
            The name of the image that will be made current.

        Returns:
            A current image.

        """
        if name is None or name == "current":
            return self._current

        image = self._images.get(name)

        if image is None:
            image = next(
                (
                    state
                    for state in self._images.values()
                    if state.filename == name
                    or state.alias == name
                ),
                None
            )

        if image is not None:
            self._current = image

        return image

    @staticmethod
    def _calculate_height(
        width: int, original_width: int, original_height: int
    ) -> int:
        """Calculate target height while preserving proportions.

        Param width:
            The desired width of the ASCII image.

        Param original_width:
            The width of the source image.

        Param original_height:
            The height of the source image.

        Returns:
            The calculated height of the ASCII image in rows with a
            minimum of 1 row.

        """
        aspect_ratio = original_height / original_width
        character_correction = 0.5

        return max(
            1,
            round(width * aspect_ratio * character_correction)
        )

    @singledispatchmethod
    def on_controller_event(self, event: ControllerEvent) -> None:
        """Handle an event submitted by the controller.

        Param event:
            A controllerevent that will be dispatched if defined.

        """
        raise TypeError(
            "Unsupported controller event: "
            f"{type(event).__name__}"
        )

    @on_controller_event.register
    def _(self, event: LoadImageRequested) -> None:
        """Load an image into the current session.

        Param event:
            A controllerevent requesting the loading of an image.

        """
        try:
            image = self._image_loader.load(event.filename)

        except LoadError as warning:
            self._notify_observers(
                DisplayWarning(str(warning))
            )
            return

        width, height = image.size

        target_height = self._calculate_height(
            self.DEFAULT_WIDTH, width, height
        )

        image_state = ImageState(
            filename = event.filename,
            alias = event.alias,
            image = image,
            target_width = self.DEFAULT_WIDTH,
            target_height = target_height
        )

        self._images[image_state.name] = image_state
        self._current = image_state

    @on_controller_event.register
    def _(self, event: ChangeBrightness ) -> None:
        """Change image brightness.

        Param event:
            A controllerevent requesting a change in image brightness.

        """
        image = self._find_image(event.image)

        if image is None:
            self._notify_observers(
                DisplayWarning(f"Image '{event.image}' not found.")
            )
            return

        image.brightness *= event.brightness

    @on_controller_event.register
    def _(self, event: ChangeContrast) -> None:
        """Change image contrast.

        Param event:
            A controllerevent requesting a change in image contrast.

        """
        image = self._find_image(event.image)

        if image is None:
            self._notify_observers(
                DisplayWarning(f"Image '{event.image}' not found.")
            )
            return

        image.contrast *= event.contrast

    @on_controller_event.register
    def _(self, event: ChangeWidth) -> None:
        """Change rendered image width.

        Param event:
            A controllerevent requesting a chang in image width.

        """
        image = self._find_image(event.image)

        if image is None:
            self._notify_observers(
                DisplayWarning(f"Image '{event.image}' not found.")
            )
            return

        image.target_width = event.width
        original_width, original_height = image.image.size
        image.target_height = self._calculate_height(
            event.width,
            original_width,
            original_height
        )

    @on_controller_event.register
    def _(self, event: ChangeHeight) -> None:
        """Change rendered image height.

        Param event:
            A controllerevent requesting a change in image height.

        """
        image = self._find_image(event.image)

        if image is None:
            self._notify_observers(
                DisplayWarning(f"Image '{event.image}' not found.")
            )
            return

        image.target_height = event.height
        original_width, original_height = image.image.size
        aspect_ratio = original_width / original_height
        image.target_width = max(
            1,
            round(event.height * aspect_ratio / 0.5)
        )

    @on_controller_event.register
    def _(self, event: RenderRequested) -> None:
        """Render an image as ASCII.
        
        Param event:
            A controllerevent requesting that the current image is
            rendered to view or to file.

        """
        image = self._find_image(event.image)

        if image is None:
            self._notify_observers(
                DisplayWarning(
                    "No image available to render."
                )
            )
            return

        ascii_rendering = (
            self._ascii_renderer.render(
                image=image.image,
                width=image.target_width,
                height=image.target_height,
                brightness=image.brightness,
                contrast=image.contrast
            )
        )

        if event.destination is not None:
            with open(
                event.destination, "w", encoding="utf-8"
            ) as file:
                file.write(ascii_rendering)

            return

        self._notify_observers(DisplayAsciiRendering(ascii_rendering))

    @on_controller_event.register
    def _(self, event: ImageInfoRequested) -> None:
        """Request display of session information.

        Param event:
            A controllerevent requesting that that imageinfo is
            created.

        """
        summaries = tuple(
            ImageSummary(
                name=state.name,
                filename=state.filename,
                size=state.size,
                target_size=state.target_size,
                brightness=state.brightness,
                contrast=state.contrast
            )
            for state in self._images.values()
        )

        current = (
            self._current.name
            if self._current is not None
            else None
        )

        self._notify_observers(
            DisplaySessionInfo(images = summaries, current = current)
        )

    @on_controller_event.register
    def _(self, event: SaveSessionRequested) -> None:
        """Save current session.

        Param event:
            A controllerevent requesting that the session gets saved
            into persistent memory.

        """
        try:
            self._session_serializer.save(
                event.filename,
                self._images,
                self._current
            )

        except OSError as warning:
            self._notify_observers(DisplayWarning(str(warning)))

    @on_controller_event.register
    def _(self, event: LoadSessionRequested) -> None:
        """Load a saved session.

        Param event:
            A controllerevent requesting the loading of a session.

        """
        try:
            session = self._session_serializer.load(event.filename)

            images: dict[str, ImageState] = {}

            for name, saved in session["images"].items():
                image = self._image_loader.load(saved["filename"])

                state = ImageState(
                    filename=saved["filename"],
                    alias=saved["alias"],
                    image=image,
                    target_width=saved["target_width"],
                    target_height=saved["target_height"],
                    brightness=saved["brightness"],
                    contrast=saved["contrast"]
                )

                images[name] = state

            self._images = images
            current = session["current"]
            self._current = (
                self._images.get(current)
                if current is not None
                else None
            )

        except (OSError, LoadError, KeyError) as warning:
            self._notify_observers(DisplayWarning(str(warning)))

    @on_controller_event.register
    def _(self, event: ExitRequested) -> None:
        """Forward exit request to the view.

        Param event:
            A controllerevent requesting an exit.

        """
        self._notify_observers(ExitRequested())


    @on_controller_event.register
    def _(self, event: DisplayWarningRequested) -> None:
        """Request display of warning.

        Param event:
            A controllerevent requesting a warning to be displayed.

         """
        self._notify_observers(
            DisplayWarning(event.warning)
        )

    @on_controller_event.register
    def _(self, event: DisplayNoticeRequested) -> None:
        """Request display of notice.

        Param event:
            A controllerevent requesting a notice to be displayed.

         """
        self._notify_observers(
            DisplayNotice(event.notice)
        )
