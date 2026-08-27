from aas.controller.controller import Controller
from aas.events.events import (
    ChangeHeight,
    DisplayWarningRequested
)

class SetHeightCtrlr(Controller):
    """docstring for SetHeightCtrlr."""
    def __init__(self):
        super(SetHeightCtrlr, self).__init__()

    def parse(self, image: str, value: str) -> None:
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
            return

        if height <= 0:
            super().notify_observers(
                DisplayWarningRequested(
                    f"Invalid height: {height}"
                )
            )
            return

        super().notify_observers(
            ChangeHeight(image, height)
        )
