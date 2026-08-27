from aas.controller.controller import Controller
from aas.events.events import (
    ChangeContrast,
    DisplayWarningRequested
)
class SetContrastCtrlr(Controller):
    """docstring for SetContrastCtrlr."""

    def __init__(self):
        super(SetContrastCtrlr, self).__init__()

    def parse(self, image: str, value: str) -> None:
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


