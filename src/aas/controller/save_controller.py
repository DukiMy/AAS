from aas.controller.controller import Controller
from aas.events.events import (
    SaveSessionRequested,
    DisplayWarningRequested
)

class SaveController(Controller):
    """docstring for SaveController."""
    def __init__(self):
        super(SaveController, self).__init__()

    def _parse_save_command(self, command: str) -> None:
        """Parse a save command.

        Param command:
            A 'save session as' command which will be parsed.

        Returns:
            A controller event representing a request to save a
            session, or a none if the command is malformed.

        """

        parts = command.split()

        if (len(parts) == 3
            and parts[0].lower() == "session"
            and parts[1].lower() == "as"
        ):
            filename = parts[2]

            super().notify_observers(
                SaveSessionRequested(filename)
            )

        super().notify_observers(
            DisplayWarningRequested(
                f"Invalid save command: {command}"
            )
        )
