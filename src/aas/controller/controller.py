from aas.events.events import ControllerEvent
from aas.events.protocols import ControllerObserver


class Controller:
    """Base class for controllers."""

    _observers: ClassVar[list[ControllerObserver]] = []

    def __init__(self) -> None:
        pass

    def add_observer(self, observer: ControllerObserver) -> None:
        """Register an observer.

        Param observer:
            An observer of this controllers events.

        """
        self._observers.append(observer)

    def notify_observers(self, event: ControllerEvent) -> None:
        """Notify all registered observers.

        Param event:
            The controllerevent that will be sent to the observers.

        """
        print("Notifying controllerevent")
        for observer in self._observers:
            print(type(event))
            observer.on_controller_event(event)

    def _split_first(self, command: str) -> tuple[str | None, str]:
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

