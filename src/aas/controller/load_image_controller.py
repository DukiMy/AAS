from aas.controller.controller import Controller
from aas.events.events import DisplayWarningRequested
from aas.events.events import LoadImageRequested

class LoadImageCtrlr(Controller):
    """docstring for LoadImageCtrlr."""
    def __init__(self):
        super(LoadImageCtrlr, self).__init__()

    def parse(self, command: str) -> None:
        """Parse 'load image' command.

        Param command:
            A command for loading images.

        Returns:
            An event representing a request to load an image.
        
        """
        parts = command.split()

        if len(parts) == 1:
            filename = parts[0]

            super().notify_observers(
                LoadImageRequested(filename, None)
            )
            return

        if (len(parts) == 3 and parts[1].lower() == "as"):
            filename = parts[0]
            alias = parts[2]

            super().notify_observers(
                LoadImageRequested(filename, alias)
            )
            return

        super().notify_observers(
            DisplayWarningRequested(
                f"Invalid command: {command}"
            )
        )
