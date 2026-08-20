# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Provide image loading."""

from PIL import Image
from aas.model.loader.image_validator import ImageValidator


class ImageLoader:
    """Load validated image files."""

    def __init__(self) -> None:
        """Initialize image loader."""

        self._validator = ImageValidator()

    def load(self, path: str) -> Image.Image:
        """Load and return an image.

        Param path:
            The path to the image which will be delegated to a valida-
            tor.

        Returns:
            A validted image.

        """
        return self._validator.validate(path)
