# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------

"""Provide the CLI view for AAS."""

from functools import singledispatchmethod

from aas.events.events import (
    DisplayAsciiRendering,
    DisplaySessionInfo,
    DisplayWarning,
    DisplayNotice,
    ExitRequested,
    ModelEvent
)


class CLIView:
    """Present application state through the command line."""

    @singledispatchmethod
    def on_model_event(self, event: ModelEvent) -> None:
        """Handle event submitted by model.

        Param event:
            A modelevent that will be dispatched if defined by this
            view.

        """
        raise TypeError(
            "Unsupported model event: "
            f"{type(event).__name__}"
        )

    @on_model_event.register
    def _(self, event: ExitRequested) -> None:
        """Handle exit request.

        Param event:
            A modelevent requesting termination of the program.
        
        """
        print("Bye!")
        raise SystemExit(0)

    @on_model_event.register
    def _(self, event: DisplayAsciiRendering) -> None:
        """Display ASCII image.

        Param event:
            A modelevent requesting a display of the ASCII image.

        """
        print(
            event.ascii_rendering,
            end="",
        )

    @on_model_event.register
    def _(self, event: DisplaySessionInfo) -> None:
        """Display session information.

        Param event:
            A modelevent requesting a display of the sessioninfo.

        """
        print("=== Current session ===")
        print("Images:")

        for image in event.images:
            print(image.name)
            print(f"  filename: {image.filename}")
            print(f"  size: {image.size}")
            print(
                f"  target size: "
                f"{image.target_size}"
            )
            print(
                f"  brightness: "
                f"{image.brightness}"
            )
            print(
                f"  contrast: "
                f"{image.contrast}"
            )

        print(f"Current image: {event.current}")

    @on_model_event.register
    def _(self, event: DisplayWarning) -> None:
        """Display warning.

        Param event:
            A modelevent requesting the display of a warning.

        """
        print(f"Warning: {event.warning}")


    @on_model_event.register
    def _(self, event: DisplayNotice) -> None:
        """Display warning.

        Param event:
            A modelevent requesting the display of a warning.

        """
        print(f"{event.notice}", end="")
    
