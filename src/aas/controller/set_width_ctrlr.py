from aas.controller.controller import Controller
from aas.events.events import (
    ChangeWidth,
    DisplayWarningRequested
)

class SetWidthCtrlr(Controller):
    """docstring for SetWidthCtrlr."""
    def __init__(self):
        super(SetWidthCtrlr, self).__init__()

    def parse(self, image: str, value: str) -> None:
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
            return

        if width <= 0:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid width: {width}"
                )
            )
            return

        super().notify_observers(
            ChangeWidth(image, width)
        )
