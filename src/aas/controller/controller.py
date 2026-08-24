from aas.events.events import ControllerEvent
from aas.events.protocols import ControllerObserver


class Controller:
    """Base class for controllers."""

    def __init__(self) -> None:
        self._observers: list[ControllerObserver] = []

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
        for observer in self._observers:
            observer.on_controller_event(event)
