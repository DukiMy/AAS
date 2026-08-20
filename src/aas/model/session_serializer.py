"""Serialize AAS sessions."""

import json
from typing import TypedDict
from aas.model.image_state import ImageState


class SerializedImage(TypedDict):
    """Serialized image state."""

    filename: str
    alias: str | None
    target_width: int
    target_height: int
    brightness: float
    contrast: float


class SerializedSession(TypedDict):
    """Serialized AAS session."""

    current: str | None
    images: dict[str, SerializedImage]


class SessionSerializer:
    """Save and load AAS sessions."""

    @staticmethod
    def save(
        filename: str,
        images: dict[str, ImageState],
        current: ImageState | None
    ) -> None:
        """Save session to JSON.
        Param filename:
            The name of the JSON file.

        Param images:
            The list of images that will be saved to 'filename'.

        Param current:
            The current image of the session.

        """
        data: SerializedSession = {
            "current": (
                current.name
                if current is not None
                else None
            ),
            "images": {
                name: {
                    "filename": state.filename,
                    "alias": state.alias,
                    "target_width": state.target_width,
                    "target_height": state.target_height,
                    "brightness": state.brightness,
                    "contrast": state.contrast
                }
                for name, state in images.items()
            },
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load(filename: str) -> SerializedSession:
        """Load session data from JSON.

        Param filename:
            The name of the JSON file that will be loaded.

        Returns:
            A session.

        """
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
