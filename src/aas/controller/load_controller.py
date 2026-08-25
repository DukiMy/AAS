from aas.events.events import LoadImageRequested
from aas.events.events import LoadSessionRequested
from aas.events.events import DisplayWarningRequested
from aas.controller.controller import Controller

class LoadController(Controller):
    """docstring for LoadController."""
    def __init__(self):
        super(LoadController, self).__init__()

    def _parse_load_image(self, command: str) -> None:
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

        if (len(parts) == 3 and parts[1].lower() == "as"):
            filename = parts[0]
            alias = parts[2]

            super().notify_observers(
                LoadImageRequested(filename, alias)
            )

        return DisplayWarningRequested(
            f"Invalid command: {command}"
        )

    def _parse_load_session(self, command: str) -> None:
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

    def parse_load_command(self, command: str) -> None:
        """Parse a load command.

        Param command:
            A command to load either an image or a session.

        Returns:
            An event reprsenting a request for loading a session or an
            image.

        """
        subcommand, remainder = super()._split_first(command)

        if subcommand == "image":
            return self._parse_load_image(remainder)

        if subcommand == "session":
            return self._parse_load_session(remainder)

        super().notify_observers(
            ExitRequested(
                DisplayWarningRequested(f"Invalid command: {command}")
            )
        )

