from aas.events.events import (
    DisplayWarningRequested,
    ChangeWidth,
    ChangeHeight,
)
from aas.controller.set_brightness_ctrlr import SetBrightnessCtrlr
from aas.controller.set_contrast_ctrlr import SetContrastCtrlr
from aas.controller.set_height_ctrlr import SetHeightCtrlr
from aas.controller.set_width_ctrlr import SetWidthCtrlr

class SetController():
    """docstring for SetController."""

    def __init__(self):

        self._brightness_controller = SetBrightnessCtrlr()
        self._contrast_controller = SetContrastCtrlr()
        self._height_controller = SetHeightCtrlr()
        self._width_controller = SetWidthCtrlr()

        self._commands: dict[
            str,
            Callable[[str, str], None]
        ] = {
            "width": self._width_controller.parse,
            "height": self._height_controller.parse,
            "brightness": self._brightness_controller.parse,
            "contrast": self._contrast_controller.parse,
        }

    def parse(self, command: str) -> None:
        """Parse a set command."""

        parts = command.split()

        if len(parts) != 3:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid command: {command}"
                )
            )
            return

        image = parts[0]
        property_name = parts[1].lower()
        value = parts[2]

        parser = self._commands.get(property_name)

        if parser is None:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid command: {command}"
                )
            )
            return

        parser(image, value)
