# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

# TODO: Create separate components for each command. And let the com-
#       ponents subscribe the the model with their specific event.

"""Provide the CLI controller."""

from aas.events.events import (
    ChangeBrightness,
    ChangeContrast,
    ChangeHeight,
    ChangeWidth,
    ControllerEvent,
    DisplayNoticeRequested,
    DisplayWarningRequested,
    ExitRequested,
    ImageInfoRequested,
    LoadImageRequested,
    LoadSessionRequested,
    RenderRequested,
    SaveSessionRequested
)
from aas.events.protocols import ControllerObserver


class CLIController:
    """Control CLI interaction."""

    def __init__(self) -> None:
        """Initialize controller."""

        self._observers: list[ControllerObserver] = []

    def add_observer(self, observer: ControllerObserver) -> None:
        """Register an observer.

        Param observer:
            An observer of this controllers events.

        """
        self._observers.append(observer)

    def _notify_observers(self, event: ControllerEvent) -> None:
        """Notify all registered observers.
        
        Param event:
            The controllerevent that will be sent to the observers.

        """
        for observer in self._observers:
            observer.on_controller_event(event)

    @staticmethod
    def _split_first(command: str) -> tuple[str | None, str]:
        """Split first word from remaining command.

        Param command:
            The command that will be split into a subcommand and rema-
            ining commands.

        Returns:
            A tuple of a subcommand and remaining commands if there a-
            re any.

        """
        parts = command.strip().split(maxsplit=1)

        if not parts:
            return None, ""

        first = parts[0].lower()
        remainder = parts[1] if len(parts) > 1 else ""

        return first, remainder

    def _parse_load_image(
        self, command: str
    ) -> LoadImageRequested | None:
        """Parse 'load image' command.

        Param command:
            A command for loading images.

        Returns:
            An event representing a request to load an image.
        
        """
        parts = command.split()

        if len(parts) == 1:
            filename = parts[0]

            return LoadImageRequested(
                filename,
                None,
            )

        if (len(parts) == 3 and parts[1].lower() == "as"):
            filename = parts[0]
            alias = parts[2]

            return LoadImageRequested(filename, alias)

        return DisplayWarningRequested(
            f"Invalid command: {command}"
        )

    def _parse_load_session(
        self, command: str
    ) -> LoadSessionRequested | None:
        """Parse 'load session' command.
        
        Param command:
            A command for loading a session.

        Returns:
            An event representing a request for loading a session.

        """
        parts = command.split()

        if len(parts) != 1:
            return DisplayWarningRequested(
                f"Invalid command: {command}"
            )

        filename = parts[0]

        return LoadSessionRequested(filename)

    def _parse_width(
        self, image: str, value: str
    ) -> ChangeWidth | None:
        """Parse a width value.

        Param image:
            The reference to the image whos width will be changed.
        
        Param value:
            The value of the new width.

        Returns:
            An event representing a request for changing the width of
            of the image under the provided reference.

        """
        try:
            width = int(value)

        except ValueError:
            return DisplayWarningRequested(
                f"Invalid width value: {value}"
            )

        if width <= 0:
            return DisplayWarningRequested(
                f"Invalid width: {width}"
            )

        return ChangeWidth(image, width)

    def _parse_height(
        self, image: str, value: str
    ) -> ChangeHeight | None:
        """Parse a height value.

        Param image:
            A reference to the image whos height will be changed.

        Param value:
            The value of the new height.

        Returns:
            An event representing a request for changing the height of
            the image under the provided reference.

        """
        try:
            height = int(value)

        except ValueError:
            return DisplayWarningRequested(
                f"Invalid height value: {value}"
            )

        if height <= 0:
            return DisplayWarningRequested(
                f"Invalid height: {height}"
            )

        return ChangeHeight(image, height)

    def _parse_brightness(
        self, image: str, value: str
    ) -> ChangeBrightness | None:
        """Parse a brightness value.

        Param image:
            A reference to the image who brightness will change.

        Param value:
            The value of the new brightness.

        Returns:
            An event representing a request for changing the brightne-
            ss of the image under the provided reference.

        """
        try:
            brightness = float(value)

        except ValueError:
            return DisplayWarningRequested(
                f"Invalid brightness value: {value}"
            )

        if brightness < 0:
            return DisplayWarningRequested(
                f"Invalid brightness: {brightness}"
            )

        return ChangeBrightness(image, brightness)

    def _parse_contrast(
        self, image: str, value: str
    ) -> ChangeContrast | None:
        """Parse a contrast value.

        Param image:
            A reference to the image whos contrast will change.

        Param value:
            The value of the new contrast.

        Returns:
            An event representing a request for changing the contrast
            of the image under the provided reference.

        """
        try:
            contrast = float(value)
        except ValueError:
            return DisplayWarningRequested(
                f"Invalid contrast value: {value}"
            )

        if contrast < 0:
            return DisplayWarningRequested(
                f"Invalid contrast: {contrast}"
            )

        return ChangeContrast(image, contrast)

    def _parse_quit_command(
        self, command: str
    ) -> ExitRequested:
        """Parse a quit command.

        Param command:
            An exit command which will be parsed.           
        Returns:
            A controllerevent representing a request to exit the appl-
            ication.
            
        """
        return ExitRequested()

    def _parse_info_command(
        self, command: str
    ) -> ImageInfoRequested:
        """Parse an info command.

        Param command:
            An info request command that will be parsed.

        Returns:
            A controllerevent representing a request to display infor-
            mation of an image.

        """
        return ImageInfoRequested()


    def _parse_save_command(
        self, command: str
    ) -> SaveSessionRequested | None:
        """Parse a save command.

        Param command:
            A 'save session as' command which will be parsed.

        Returns:
            A controller event representing a request to save a
            session, or a none if the command is malformed.

        """

        parts = command.split()

        if (len(parts) == 3
            and parts[0].lower() == "session"
            and parts[1].lower() == "as"
        ):
            filename = parts[2]

            return SaveSessionRequested(filename)

        return DisplayWarningRequested(
            f"Invalid save command: {command}"
        )

    def _parse_render_command(
        self, command: str
    ) -> RenderRequested | None:
        """Parse a render command.

        Param command:
            A 'render' command which will be parsed.

        Returns:
            A controller event representing a request to render an im-
            age, or 'None' if it fails to parse the 'set' command.

        """
        parts = command.split()

        if not parts:
            return RenderRequested()

        if len(parts) == 1:
            return RenderRequested(
                image=parts[0]
            )

        if (
            len(parts) == 3
            and parts[1].lower() == "to"
        ):
            return RenderRequested(
                image=parts[0], destination=parts[2]
            )

        return DisplayWarningRequested(
            f"Invalid render command: {command}"
        )

    def _parse_set_command(
        self, command: str
    ) -> ControllerEvent | None:
        """Parse a set command.

        Param command:
            The 'set' command which will be parsed.

        Returns:
            A controller event related to the 'set' command, or a
            'None' if any of the methods delegates fail.

        """
        parts = command.split()

        if len(parts) != 3:
            return DisplayWarningRequested(
                f"Invalid command: {command}"
            )

        image = parts[0]
        property_name = parts[1].lower()
        value = parts[2]

        if property_name == "width":
            return self._parse_width(image, value)

        if property_name == "height":
            return self._parse_height(image, value)

        if property_name == "brightness":
            return self._parse_brightness(image, value)

        if property_name == "contrast":
            return self._parse_contrast(image, value)

        return DisplayWarningRequested(f"Invalid command: {command}")

    def _parse_load_command(
        self, command: str
    ) -> ControllerEvent | None:
        """Parse a load command.

        Param command:
            A command to load either an image or a session.

        Returns:
            An event reprsenting a request for loading a session or an
            image.

        """
        subcommand, remainder = self._split_first(command)

        if subcommand == "image":
            return self._parse_load_image(remainder)

        if subcommand == "session":
            return self._parse_load_session(remainder)

        return DisplayWarningRequested(f"Invalid command: {command}")

    def _parse_command(self, command: str) -> ControllerEvent | None:
        """Parse a complete CLI command.

        Param command:
            The complete CLI command which will be parsed.

        Returns:
            An event from this controller or 'None' if the command is
            malformed.

        """
        subcommand, remainder = self._split_first(command)

        if subcommand is None:
            return None

        if subcommand == "load":
            return self._parse_load_command(remainder)

        if subcommand == "set":
            return self._parse_set_command(remainder)

        if subcommand == "render":
            return self._parse_render_command(remainder)

        if subcommand == "save":
            return self._parse_save_command(remainder)

        if subcommand == "info":
            return self._parse_info_command(remainder)

        if subcommand == "quit":
            return self._parse_quit_command(remainder)

        return DisplayWarningRequested(f"Invalid command: {command}")

    def _take_command(self) -> str:
        """Read a command from the user.

        Returns:
            A string of commands with no spaces at [0] and [-1].

        """
        self._notify_observers(
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

            self._notify_observers(event)
