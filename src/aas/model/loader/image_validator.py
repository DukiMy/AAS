# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Validate image files."""

from PIL import Image, UnidentifiedImageError
from aas.exceptions.load_error import LoadError


class ImageValidator:
    """Validate and open image files."""

    @staticmethod
    def validate(path: str) -> Image.Image:
        """Validate an image path and return the loaded image.

        Param path:
            The path to the image which will be validated.

        Returns:
            A validated image.

        Raises:
            FileNotFoundError:
                Raised if the path points to a file that doesnt exist.

            PermissionError:
                Raised if the path points to a file that the user does
                not have permission ro read.

            IsADirectoryError:
                Raised if the path points to a directory.

            InidentifiedImageError:
                Raised if the path points to a file which is not an
                image supported by 'pillow'.

            """
        try:
            image = Image.open(path)
            image.load()

        except FileNotFoundError as error:
            raise LoadError(
                f"Image file not found: '{path}'."
            ) from error

        except PermissionError as error:
            raise LoadError(
                f"Permission denied: '{path}'."
            ) from error

        except IsADirectoryError as error:
            raise LoadError(
                f"Expected an image, but got a directory: '{path}'."
            ) from error

        except UnidentifiedImageError as error:
            raise LoadError(
                f"File is not a recognized image: '{path}'."
            ) from error

        return image
