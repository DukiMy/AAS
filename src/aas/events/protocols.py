# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Define observer protocols. Does not define runtime behavior."""

from typing import Protocol

from aas.events.events import ControllerEvent, ModelEvent


class ControllerObserver(Protocol):
    """Observe controller events."""

    def on_controller_event(self, event: ControllerEvent) -> None:
        """Handle a controller event."""

        ...


class ModelObserver(Protocol):
    """Observe model events."""

    def on_model_event(self, event: ModelEvent) -> None:
        """Handle a model event."""

        ...
