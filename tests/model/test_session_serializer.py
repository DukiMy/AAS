# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

from pathlib import Path

from PIL import Image

from aas.model.image_state import ImageState
from aas.model.session_serializer import SessionSerializer


def test_save_and_load_session(tmp_path: Path) -> None:
    """Save session and restore equivalent serialized data."""
    filename = tmp_path / "session.json"

    state = ImageState(
        filename="cat.png",
        alias="cat",
        image=Image.new("RGB", (100, 50)),
        target_width=50,
        target_height=25,
        brightness=1.5,
        contrast=0.8
    )

    images = {"cat": state}
    SessionSerializer.save(str(filename), images, state)
    session = SessionSerializer.load(str(filename))

    assert session["current"] == "cat"
    assert session["images"]["cat"]["filename"] == "cat.png"
    assert session["images"]["cat"]["alias"] == "cat"
    assert session["images"]["cat"]["target_width"] == 50
    assert session["images"]["cat"]["target_height"] == 25
    assert session["images"]["cat"]["brightness"] == 1.5
    assert session["images"]["cat"]["contrast"] == 0.8
