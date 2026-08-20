# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

import pytest

from aas.events.events import (
    DisplayAsciiRendering,
    DisplayWarning,
    ExitRequested
)
from aas.view.view import CLIView


def test_display_warning(capsys: pytest.CaptureFixture[str]) -> None:
    """Print warning supplied by model."""
    view = CLIView()

    view.on_model_event(DisplayWarning("Something failed."))

    captured = capsys.readouterr()

    assert captured.out == "Warning: Something failed.\n"


def test_exit_requested_exits_successfully(
capsys: pytest.CaptureFixture[str],
) -> None:
    """Exit with status zero after exit event."""
    view = CLIView()

    with pytest.raises(SystemExit) as exception:
        view.on_model_event(ExitRequested())

    captured = capsys.readouterr()

    assert captured.out == "Bye!\n"
    assert exception.value.code == 0


def test_display_ascii_rendering(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Print ASCII rendering unchanged."""
    view = CLIView()

    view.on_model_event(
        DisplayAsciiRendering("$@\n")
    )

    captured = capsys.readouterr()

    assert captured.out == "$@\n"
