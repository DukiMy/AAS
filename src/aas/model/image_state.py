"""Represent state associated with a loaded image."""

from dataclasses import dataclass

from PIL import Image


@dataclass(slots=True)
class ImageState:
    """Represent an image and its rendering settings."""

    filename: str
    image: Image.Image
    target_width: int
    target_height: int
    alias: str | None = None
    brightness: float = 1.0
    contrast: float = 1.0

    @property
    def name(self) -> str:
        """Return alias if available, otherwise filename.

        Returns:
            A alias if there is one, a filename otherwise.

        """
        return self.alias or self.filename

    @property
    def size(self) -> tuple[int, int]:
        """Return original image size.

        Returns:
            The size of the image.

        """
        return self.image.size

    @property
    def target_size(self) -> tuple[int, int]:
        """Return target ASCII rendering size.

        Returns:
            A tuple containing the desired width and height.

        """
        return self.target_width, self.target_height
