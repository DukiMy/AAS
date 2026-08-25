from aas.events.events import (
    DisplayWarningRequested,
    ChangeWidth,
    ChangeHeight,
    ChangeContrast,
    ChangeBrightness
)
from aas.controller.controller import Controller

class SetController(Controller):
    """docstring for SetController."""
    def __init__(self):
        super(SetController, self).__init__()

    def _parse_height(self, image: str, value: str) -> None:
        """Parse a height value.

        Param image:
            A reference to the image whos height will be changed.

        Param value:
            The value of the new height.

        Returns:
            An event representing a request for changing the height of
            the image under the provided reference.

        """
        try:
            height = int(value)

        except ValueError:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid height value: {value}"
                )
            )

        if height <= 0:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid height: {height}"
                )
            )

        super().notify_observers(
            ChangeHeight(image, height)
        )

    def _parse_width(self, image: str, value: str) -> None:
        """Parse a width value.

        Param image:
            The reference to the image whos width will be changed.
        
        Param value:
            The value of the new width.

        Returns:
            An event representing a request for changing the width of
            of the image under the provided reference.

        """
        try:
            width = int(value)

        except ValueError:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid width value: {value}"
                )
            )

        if width <= 0:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid width: {width}"
                )
            )

        super().notify_observers(
            ChangeWidth(image, width)
        )

    def _parse_brightness(
        self, image: str, value: str
    ) -> ChangeBrightness | None:
        """Parse a brightness value.

        Param image:
            A reference to the image who brightness will change.

        Param value:
            The value of the new brightness.

        Returns:
            An event representing a request for changing the brightne-
            ss of the image under the provided reference.

        """
        try:
            brightness = float(value)

        except ValueError:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid brightness value: {value}"
                )
            )

        if brightness < 0:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid brightness: {brightness}"
                )
            )

        super().notify_observers(
            ChangeBrightness(image, brightness)
        )

    def _parse_contrast(
        self, image: str, value: str
    ) -> ChangeContrast | None:
        """Parse a contrast value.

        Param image:
            A reference to the image whos contrast will change.

        Param value:
            The value of the new contrast.

        Returns:
            An event representing a request for changing the contrast
            of the image under the provided reference.

        """
        try:
            contrast = float(value)
        except ValueError:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid contrast value: {value}"
                )
            )

        if contrast < 0:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid contrast: {contrast}"
                )
            )

        super().notify_observers(
            ChangeContrast(image, contrast)
        )


    def parse_set_command(self, command: str) -> None:
        """Parse a set command.

        Param command:
            The 'set' command which will be parsed.

        Returns:
            A controller event related to the 'set' command, or a
            'None' if any of the methods delegates fail.

        """
        parts = command.split()

        if len(parts) != 3:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid command: {command}"
                )
            )

        image = parts[0]
        property_name = parts[1].lower()
        value = parts[2]

        if property_name == "width":
            self._parse_width(image, value)

        if property_name == "height":
            self._parse_height(image, value)

        if property_name == "brightness":
            self._parse_brightness(image, value)

        if property_name == "contrast":
            self._parse_contrast(image, value)

        super().notify_observers(
            DisplayWarningRequested(f"Invalid command: {command}")
        )
