from aas.controller.controller import Controller
from aas.events.events import ExitRequested

class ExitController(Controller):
    """docstring for ExitController."""

    def __init__(self):
        """Inits the exitcontroller."""
        super(ExitController, self).__init__()

    def parse(self, command) -> None:
        """Notifies observers of user exit request.

        Param command:
            Ignored.

        Note:
            The parameter 'command' is for standardising the 'parse'
            functions across the controller modules.

        """
        super().notify_observers(ExitRequested())
