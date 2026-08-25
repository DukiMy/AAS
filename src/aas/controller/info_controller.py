from aas.controller.controller import Controller
from aas.events.events import ImageInfoRequested


class InfoController(Controller):
    """docstring for InfoController."""
    def __init__(self):
        super(InfoController, self).__init__()

    def parse_info_command(self, command: str) -> None:
        """Parse an info command.

        Param command:
            An info request command that will be parsed.

        Returns:
            A controllerevent representing a request to display infor-
            mation of an image.

        """
        super().notify_observers(ImageInfoRequested())
