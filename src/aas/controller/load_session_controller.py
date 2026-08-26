from aas.controller.controller import Controller
from aas.events.events import DisplayWarningRequested
from aas.events.events import LoadSessionRequested

class LoadSessionCtrlr(Controller):
    """docstring for LoadSessionCtrlr."""

    def __init__(self):
        super(LoadSessionCtrlr, self).__init__()

    def parse(self, command: str) -> None:
        """Parse 'load session' command.
        
        Param command:
            A command for loading a session.

        Returns:
            An event representing a request for loading a session.

        """
        parts = command.split()

        if len(parts) != 1:
            super().notify_observers(
                DisplayWarningRequested(f"Invalid command: {command}")
            )

        filename = parts[0]

        super().notify_observers(
            LoadSessionRequested(filename)
        )

