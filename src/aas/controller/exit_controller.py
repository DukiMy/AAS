from aas.controller.controller import Controller
from aas.events.events import ExitRequested

class ExitController(Controller):
    """docstring for ExitController."""
    def __init__(self):
        super(ExitController, self).__init__()

    def parse_quit_command(self, command: str) -> ExitRequested:
        """Parse a quit command.

        Param command:
            An exit command which will be parsed.           
        Returns:
            A controllerevent representing a request to exit the appl-
            ication.
            
        """
        super().notify_observers(ExitRequested())

