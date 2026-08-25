# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

# TODO: Create separate components for each command. And let the com-
#       ponents subscribe the the model with their specific event.

"""Provide the CLI controller."""

from aas.events.events import (
    ControllerEvent,
    DisplayNoticeRequested,
    DisplayWarningRequested,
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
        self._exit_controller = ExitController()
        self._info_controller = InfoController()
        self._load_controller = LoadController()
        self._set_controller = SetController()
        self._render_controller = RenderController()
        self._save_controller = SaveController()

    def _parse_command(self, command: str) -> ControllerEvent | None:
        """Parse a complete CLI command.

        Param command:
            The complete CLI command which will be parsed.

        Returns:
            An event from this controller or 'None' if the command is
            malformed.

        """
        subcommand, remainder = super()._split_first(command)

        if subcommand is None:
            return None

        if subcommand == "load":
            self._load_controller.parse_load_command(remainder)
            return None

        if subcommand == "set":
            self._set_controller.parse_set_command(remainder)
            return None

        if subcommand == "render":
            self._render_controller.parse_render_command(remainder)
            return None

        if subcommand == "save":
            self._save_controller.parse_save_command(remainder)
            return None

        if subcommand == "info":
            self._info_controller.parse_info_command(remainder)
            return None

        if subcommand == "quit":
            self._exit_controller.parse_quit_command(remainder)
            return None

        return DisplayWarningRequested(f"Invalid command: {command}")

    def _take_command(self) -> str:
        """Read a command from the user.

        Returns:
            A string of commands with no spaces at [0] and [-1].

        """
        super().notify_observers(
            DisplayNoticeRequested("AAS: ")
        )
        return input().strip()

    def start(self) -> None:
        """Start accepting commands.

        Takes command, convert to event and notify observers.

        """
        while True:
            command = self._take_command()

            if command is None:
                continue

            event = self._parse_command(command)

            if event is None:
                continue

            super().notify_observers(event)
