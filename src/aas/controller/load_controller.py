from aas.controller.controller import Controller
from aas.controller.load_session_controller import LoadSessionCtrlr
from aas.controller.load_image_controller import LoadImageCtrlr

class LoadController(Controller):
    """docstring for LoadController."""
    def __init__(self):
        super(LoadController, self).__init__()

        self._commands = {
            "image": LoadImageCtrlr().parse,
            "session": LoadSessionCtrlr().parse,
        }


    def parse(self, command: str) -> None:
        """Parse a load command.

        Param command:
            A command to load either an image or a session.

        Returns:
            An event reprsenting a request for loading a session or an
            image.

        """
        super().parse_command(command, self._commands)

