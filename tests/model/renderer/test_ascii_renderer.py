# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

from PIL import Image

from aas.model.renderer.ascii_renderer import AsciiRenderer


def test_render_black_and_white_image() -> None:
    """Render a simple image as ASCII."""
    image = Image.new("L", (2, 1))

    image.putpixel((0, 0), 0)
    image.putpixel((1, 0), 255)

    result = AsciiRenderer.render(
        image=image,
        width=2,
        height=1
    )

    assert result == "$ \n"


def test_render_uses_requested_dimensions() -> None:
    """Render using requested width and height."""
    image = Image.new("L", (10, 10), 255)

    result = AsciiRenderer.render(
        image=image,
        width=3,
        height=2
    )

    rows = result.splitlines()

    assert len(rows) == 2
    assert all(len(row) == 3 for row in rows)
