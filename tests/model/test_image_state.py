# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

from PIL import Image

from aas.model.image_state import ImageState


def test_name_returns_alias_when_present() -> None:
    """Return alias as image name if alias exists."""
    image = Image.new("RGB", (100, 50))

    state = ImageState(
        filename="cat.png",
        alias="cat",
        image=image,
        target_width=50,
        target_height=25
    )

    assert state.name == "cat"


def test_name_returns_filename_without_alias() -> None:
    """Return filename when no alias exists."""
    image = Image.new("RGB", (100, 50))

    state = ImageState(
        filename="cat.png",
        image=image,
        target_width=50,
        target_height=25
    )

    assert state.name == "cat.png"


def test_size_returns_original_image_size() -> None:
    """Return dimensions of original image."""
    image = Image.new("RGB", (100, 50))

    state = ImageState(
        filename="cat.png",
        image=image,
        target_width=40,
        target_height=20
    )

    assert state.size == (100, 50)


def test_target_size_returns_ascii_dimensions() -> None:
    """Return configured ASCII dimensions."""
    image = Image.new("RGB", (100, 50))

    state = ImageState(
        filename="cat.png",
        image=image,
        target_width=40,
        target_height=20
    )

    assert state.target_size == (40, 20)
