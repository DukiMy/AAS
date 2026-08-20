# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

from PIL import Image

from aas.model.processor.image_processor import ImageProcessor


def test_to_ascii_maps_black_and_white() -> None:
    """Map darkest and brightest pixels to char ramp endpoints."""
    image = Image.new("L", (2, 1))

    image.putpixel((0, 0), 0)
    image.putpixel((1, 0), 255)

    processor = ImageProcessor(image)

    assert processor.to_ascii() == "$ \n"

def test_resize_changes_image_dimensions() -> None:
    """Resize working image to requested dimensions."""
    image = Image.new("RGB", (100, 100))
    processor = ImageProcessor(image)

    processor.resize(20, 10)

    assert processor.image.size == (20, 10)
