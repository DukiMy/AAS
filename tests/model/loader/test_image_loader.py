# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

from PIL import Image

from aas.model.loader.image_loader import ImageLoader


def test_load_valid_image(tmp_path: str) -> None:
    """Load a valid image."""
    filename = tmp_path / "image.png"

    Image.new("RGB", (20, 10)).save(filename)

    loader = ImageLoader()
    image = loader.load(str(filename))

    assert image.size == (20, 10)
    assert image.mode == "RGB"
