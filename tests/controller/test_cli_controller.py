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
    SaveSessionRequested
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
    ("command"),
    [
        "load",
        "load cat.png",
        "load nope cat.png",
        "load image cat.png nope cat"
    ]
)
def test_invalid_load(
    command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Reject malformed load commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result is None
    assert capsys.readouterr().out == "Invalid command.\n"


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
    "command",
    [
        "set cat brightness -1",
        "set cat brightness nope",
        "set cat contrast -1",
        "set cat contrast nope",
        "set cat height 0",
        "set cat height nope",
        "set cat width 0",
        "set cat width -10",
        "set cat width nope"
    ]
)
def test_invalid_set_commands(
        command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Reject malformed set commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result is None
    assert capsys.readouterr().out == "Invalid command.\n"


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("render", RenderRequested()),
        ("render cat", RenderRequested(image="cat")),
        ("render cat to output.txt", RenderRequested(image="cat", destination="output.txt")),
        ("RENDER CAT TO OUTPUT.TXT", RenderRequested(image="CAT", destination="OUTPUT.TXT"))
    ]
)
def test_valid_render_commands(command: str, expected: ControllerEvent) -> None:
    """Test valid render commands"""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    "command",
    [
        "render cat nope"
    ]
)
def test_invalid_render_commands(
        command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Reject malformed save commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result is None
    assert capsys.readouterr().out == "Invalid command.\n"




@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("save session as session.json", SaveSessionRequested("session.json")),
        ("SAVE SESSION AS SESSION.JSON", SaveSessionRequested("SESSION.JSON"))
    ]
)
def test_valid_save_commands(command: str, expected: ControllerEvent) -> None:
    """Convert valid CLI commands into corresponding events."""
    controller = CLIController()

    assert controller._parse_command(command) == expected


@pytest.mark.parametrize(
    "command",
    [
        "save",
        "save nope",
        "save session nope"
    ]
)
def test_invalid_save_commands(
        command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Reject malformed save commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result is None
    assert capsys.readouterr().out == "Invalid command.\n"



@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("info", ImageInfoRequested()),
        ("quit", ExitRequested()),
    ]
)
def test_valid_single_commands(command: str, expected: ControllerEvent) -> None:
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
        command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Reject malformed single commands."""
    controller = CLIController()

    result = controller._parse_command(command)

    assert result is None
    assert capsys.readouterr().out == "Invalid command.\n"


