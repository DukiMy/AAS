# Copyright (c) 2026 Durim Miziraj
# --------------------------------------------------------------------
"""Define events exchanged between MVC components."""

from dataclasses import dataclass


# --------------------------------------------------------------------
# Controller events
# --------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ExitRequested:
    """Notify observers of exit request."""


@dataclass(frozen=True, slots=True)
class ImageInfoRequested:
    """Notify observers of session information request."""


@dataclass(frozen=True, slots=True)
class LoadImageRequested:
    """Notify observers of image load request."""

    filename: str
    alias: str | None = None


@dataclass(frozen=True, slots=True)
class LoadSessionRequested:
    """Notify observers of session load request."""

    filename: str


@dataclass(frozen=True, slots=True)
class SaveSessionRequested:
    """Notify observers of session save request."""

    filename: str


@dataclass(frozen=True, slots=True)
class RenderRequested:
    """Notify observers of render request."""

    image: str | None = None
    destination: str | None = None


@dataclass(frozen=True, slots=True)
class ChangeBrightness:
    """Notify observers of brightness change request."""

    image: str
    brightness: float


@dataclass(frozen=True, slots=True)
class ChangeContrast:
    """Notify observers of contrast change request."""

    image: str
    contrast: float


@dataclass(frozen=True, slots=True)
class ChangeHeight:
    """Notify observers of height change request."""

    image: str
    height: int


@dataclass(frozen=True, slots=True)
class ChangeWidth:
    """Notify observers of width change request."""

    image: str
    width: int


type ControllerEvent = (
    ExitRequested
    | ImageInfoRequested
    | LoadImageRequested
    | LoadSessionRequested
    | SaveSessionRequested
    | RenderRequested
    | ChangeBrightness
    | ChangeContrast
    | ChangeHeight
    | ChangeWidth
)


# --------------------------------------------------------------------
# Model events
# --------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class DisplayAsciiRendering:
    """Notify view to display an ASCII rendering."""

    ascii_rendering: str


@dataclass(frozen=True, slots=True)
class ImageSummary:
    """Notify view to display information about one image."""

    name: str
    filename: str
    size: tuple[int, int]
    target_size: tuple[int, int]
    brightness: float
    contrast: float


@dataclass(frozen=True, slots=True)
class DisplaySessionInfo:
    """Notify view to display current session information."""

    images: tuple[ImageSummary, ...]
    current: str | None


@dataclass(frozen=True, slots=True)
class DisplayWarning:
    """Notify view to display a warning."""

    warning: str


type ModelEvent = (
    ExitRequested
    | DisplayAsciiRendering
    | DisplaySessionInfo
    | DisplayWarning
)
