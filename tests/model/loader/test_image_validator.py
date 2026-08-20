# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

import pytest

from aas.exceptions.load_error import LoadError
from aas.model.loader.image_validator import ImageValidator


def test_nonexistent_image_raises_load_error() -> None:
    """Reject nonexistent image path."""
    with pytest.raises(LoadError, match = "Image file not found"):
        ImageValidator.validate("does-not-exist.png")


def test_non_image_file_raises_load_error(tmp_path: str) -> None:
    """Reject file that Pillow cannot identify."""
    filename = tmp_path / "not-image.txt"
    filename.write_text("Hello!", encoding="utf-8")

    with pytest.raises(
        LoadError, match = "File is not a recognized image"
    ):
        ImageValidator.validate(str(filename))


def test_directory_raises_load_error(tmp_path: str) -> None:
    """Reject directory instead of image."""
    with pytest.raises(
        LoadError, match="Expected an image, but got a directory"
    ):
        ImageValidator.validate(str(tmp_path))
