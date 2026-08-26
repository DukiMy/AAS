from aas.controller.controller import Controller
from aas.events.events import ImageInfoRequested


class InfoController(Controller):
    """docstring for InfoController."""

    def __init__(self):
        """Inits the InfoController."""
        super(InfoController, self).__init__()

    def parse(self, command: str) -> None:
        """Notifies observers of user info request.

        Param command:
            Ignored.

        Note:
            The parameter 'command' is for standardising the 'parse'
            functions across the controller modules.

        """
        super().notify_observers(ImageInfoRequested())
