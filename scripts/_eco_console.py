from __future__ import annotations

import sys
from typing import TextIO


def configure_windows_safe_console() -> None:
    """Avoid CLI crashes when stdout/stderr cannot encode status glyphs."""

    for stream in (sys.stdout, sys.stderr):
        _configure_stream(stream)


def _configure_stream(stream: TextIO | None) -> None:
    if stream is None:
        return

    reconfigure = getattr(stream, "reconfigure", None)
    if reconfigure is None:
        return

    try:
        reconfigure(errors="backslashreplace")
    except (TypeError, ValueError):
        return
