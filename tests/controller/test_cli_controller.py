# Copyright (c) 2026 Durim Miziraj.
# --------------------------------------------------------------------

import pytest

from aas.controller.cli_controller import CLIController
from aas.events.events import (
    ChangeBrightness,
    ChangeContrast,
    ChangeHeight,
    ChangeWidth,
    ControllerEvent,
    ExitRequested,
    ImageInfoRequested,
    LoadImageRequested,
    LoadSessionRequested,
    RenderRequested,
    SaveSessionRequested,
    DisplayWarningRequested
)


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("load image cat.png", LoadImageRequested(filename="cat.png", alias=None)),
        ("LOAD IMAGE CAT.PNG", LoadImageRequested("CAT.PNG", alias=None)),
        ("load image cat.png as cat", LoadImageRequested("cat.png", alias="cat")),
        ("LOAD IMAGE CAT.PNG AS CAT", LoadImageRequested("CAT.PNG", alias="CAT")),
        ("load session session.json", LoadSessionRequested("session.json")),
        ("LOAD SESSION SESSION.JSON", LoadSessionRequested("SESSION.JSON"))
    ]
)
def test_valid_load(command: str, expected: object) -> None:
    """Convert load command into load event."""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    ("command", "invalid_command"),
    [
        ("load", ""),
        ("load cat.png", "cat.png"),
        ("load nope cat.png", "nope cat.png"),
        ("load image cat.png nope cat", "cat.png nope cat")
    ]
)
def test_invalid_load(
    command: str, invalid_command: str
) -> None:
    """Reject malformed load commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result == DisplayWarningRequested(
        f"Invalid command: {invalid_command}"
    )


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("set cat brightness 1.5", ChangeBrightness("cat", 1.5)),
        ("set cat contrast 0.8", ChangeContrast("cat", 0.8)),
        ("set cat height 20", ChangeHeight("cat", 20)),
        ("set cat width 100", ChangeWidth("cat", 100)),
        ("SET CAT WIDTH 100", ChangeWidth("CAT", 100))
    ]
)
def test_valid_set_commands(command: str, expected: object) -> None:
    """Test valid image property commands."""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    ("command", "subcommand", "invalid_value"),
    [
        ("set cat brightness -1", "brightness", "-1.0"),
        ("set cat brightness nope", "brightness value", "nope"),
        ("set cat contrast -1", "contrast", "-1.0"),
        ("set cat contrast nope", "contrast value", "nope"),
        ("set cat height 0", "height", "0"),
        ("set cat height -10", "height", "-10"),
        ("set cat height nope", "height value", "nope"),
        ("set cat width 0", "width", "0"),
        ("set cat width -10", "width", "-10"),
        ("set cat width nope", "width value", "nope")
    ]
)
def test_invalid_set_commands(
    command: str, subcommand: str, invalid_value: str
) -> None:
    """Reject malformed set commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result == DisplayWarningRequested(
        f"Invalid {subcommand}: {invalid_value}"
    )


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("render", RenderRequested()),
        ("render cat", RenderRequested(image="cat")),
        ("render cat to output.txt", RenderRequested(image="cat", destination="output.txt")),
        ("RENDER CAT TO OUTPUT.TXT", RenderRequested(image="CAT", destination="OUTPUT.TXT"))
    ]
)
def test_valid_render_commands(
    command: str, expected: ControllerEvent
) -> None:
    """Test valid render commands"""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    ("command", "subcommand"),
    [
        ("render cat nope", "cat nope")
    ]
)
def test_invalid_render_commands(
    command: str, subcommand: str
) -> None:
    """Reject malformed render commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result == DisplayWarningRequested(
        f"Invalid render command: {subcommand}"
    )


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("save session as session.json", SaveSessionRequested("session.json")),
        ("SAVE SESSION AS SESSION.JSON", SaveSessionRequested("SESSION.JSON"))
    ]
)
def test_valid_save_commands(
    command: str, expected: ControllerEvent
) -> None:
    """Convert valid CLI commands into corresponding events."""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    ("command", "subcommand"),
    [
        ("save", ""),
        ("save nope", "nope"),
        ("save session nope", "session nope")
    ]
)
def test_invalid_save_commands(
    command: str, subcommand: str
) -> None:
    """Reject malformed save commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result == DisplayWarningRequested(
        f"Invalid save command: {subcommand}"
    )


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("info", ImageInfoRequested()),
        ("quit", ExitRequested())
    ]
)
def test_valid_single_commands(
    command: str, expected: ControllerEvent
) -> None:
    """Convert valid CLI commands into corresponding events."""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    "command",
    [
        "nope"
    ]
)
def test_invalid_single_commands(
    command: str
) -> None:
    """Reject malformed single commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result == DisplayWarningRequested(
        f"Invalid command: {command}"
    )
