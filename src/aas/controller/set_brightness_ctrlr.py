from aas.controller.controller import Controller
from aas.events.events import (
    ChangeBrightness,
    DisplayWarningRequested
)

class SetBrightnessCtrlr(Controller):
    """docstring for SetBrightnessCtrlr."""

    def __init__(self):
        super(SetBrightnessCtrlr, self).__init__()

    def parse(self, image: str, value: str) -> None:
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
