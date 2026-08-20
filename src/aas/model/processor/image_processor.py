# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Provide image processing for ASCII conversion."""

from PIL import Image, ImageEnhance


class ImageProcessor:
    """Prepare an image for ASCII rendering."""

    CHAR_RAMP = (
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!l"
        "I;:,\"^`'. "
    )

    def __init__(self, image: Image.Image) -> None:
        """Create a working copy of the image."""

        self.image = image.copy()
        self._to_grayscale()

    def adjust_brightness(self, brightness: float) -> None:
        """Adjust image brightness.

        Param brightness:
            A multiplier that changes the brightness of an image.

        """

        self.image = (
            ImageEnhance.Brightness(self.image).enhance(brightness)
        )

    def adjust_contrast(self, contrast: float) -> None:
        """Adjust image contrast.

        Param contrast:
            A multiplier that changes the contrast of an image.

        """
        self.image = (
            ImageEnhance.Contrast(self.image).enhance(contrast)
        )

    def resize(self, width: int, height: int) -> None:
        """Resize image to target ASCII dimensions.

        Param width:
            A replacement value for the width of the image.

        Param height:
            A replacement value for the height of the image.

        """
        self.image = self.image.resize(
            (width, height), Image.Resampling.LANCZOS
        )

    def _to_grayscale(self) -> None:
        """Convert image to grayscale."""

        self.image = self.image.convert("L")

    def to_ascii(self) -> str:
        """Convert processed image to ASCII.
        
        Returns:
            An ASCII representation of the instance object image.

        """
        rows: list[str] = []

        for y in range(self.image.height):
            row: list[str] = []

            for x in range(self.image.width):
                shade = self.image.getpixel((x, y))

                index = round(shade * (len(self.CHAR_RAMP) - 1) / 255)

                row.append(self.CHAR_RAMP[index])

            rows.append("".join(row))

        return "\n".join(rows) + "\n"
