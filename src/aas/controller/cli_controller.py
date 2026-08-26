# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

# TODO: Create separate components for each command. And let the com-
#       ponents subscribe the the model with their specific event.

"""Provide the CLI controller."""

from aas.events.events import (
    DisplayNoticeRequested, DisplayWarningRequested
)
from aas.controller.controller import Controller
from aas.controller.exit_controller import ExitController
from aas.controller.info_controller import InfoController
from aas.controller.load_controller import LoadController
from aas.controller.set_controller import SetController
from aas.controller.render_controller import RenderController
from aas.controller.save_controller import SaveController

class CLIController(Controller):
    """Control CLI interaction."""

    def __init__(self) -> None:
        """Initialize controller."""

        super(CLIController, self).__init__()

        self._commands = {
            "load": LoadController().parse,
            "set": SetController().parse,
            "render": RenderController().parse,
            "save": SaveController().parse,
            "info": InfoController().parse,
            "quit": ExitController().parse,
        }

    def start(self) -> None:
        """Start accepting commands."""
        while True:
            super().notify_observers(DisplayNoticeRequested("AAS: "))

            try:
                command = input().strip()

            except (KeyboardInterrupt, EOFError):
                super().parse_command("quit", self._commands)

            if command is None:
                continue

            super().parse_command(command, self._commands)
