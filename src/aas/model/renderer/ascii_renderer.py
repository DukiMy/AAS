# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Provide ASCII rendering."""

from PIL import Image
from aas.model.processor.image_processor import ImageProcessor


class AsciiRenderer:
    """Render images as ASCII."""

    @staticmethod
    def render(
        image: Image.Image,
        width: int,
        height: int,
        brightness: float = 1.0,
        contrast: float = 1.0
    ) -> str:
        """Render image according to supplied settings.

        Param image:
            The image that will be represented in ASCII.

        Param width:
            The replacement value for the width of the image.

        Param height:
            The replacement value for the height of the image.

        Param brightness:
            The multiplier for the brightness of the image.

        Param contrast:
            The multiplier for the contrast of the image.

        Returns:
            An image represented in ASCII.

        """
        processor = ImageProcessor(image)

        processor.adjust_brightness(brightness)
        processor.adjust_contrast(contrast)
        processor.resize(width, height)

        return processor.to_ascii()
