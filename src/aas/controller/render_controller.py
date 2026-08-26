from aas.controller.controller import Controller
from aas.events.events import RenderRequested, DisplayWarningRequested

class RenderController(Controller):
    """docstring for RenderController."""
    def __init__(self):
        super(RenderController, self).__init__()

    def parse(self, command: str) -> None:
        """Parse a render command.

        Param command:
            A 'render' command which will be parsed.

        Returns:
            A controller event representing a request to render an im-
            age, or 'None' if it fails to parse the 'set' command.

        """
        parts = command.split()

        if not parts:
            super().notify_observers(
                RenderRequested()
            )
            return

        if len(parts) == 1:
            super().notify_observers(
                RenderRequested(
                    image = parts[0]
                )
            )
            return

        if (
            len(parts) == 3
            and parts[1].lower() == "to"
        ):
            super().notify_observers(
                RenderRequested(
                    image = parts[0],
                    destination = parts[2]
                )
            )
            return

        super().notify_observers(
            DisplayWarningRequested(
                f"Invalid !! render command: {command}"
            )
        )
