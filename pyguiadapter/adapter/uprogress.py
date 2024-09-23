from __future__ import annotations

from typing import Literal

from .ucontext import _context


def show_progressbar(
    min_value: int = 0,
    max_value: int = 100,
    inverted_appearance: bool = False,
    *,
    message_visible: bool = False,
    message_format: str = "%p%",
    message_centered: str = True,
    show_info: bool = True,
    info_centered: bool = True,
    info_text_format: Literal[
        "richtext", "markdown", "plaintext", "autotext"
    ] = "autotext",
    initial_info: str = "",
):
    config = {
        "min_value": min_value,
        "max_value": max_value,
        "inverted_appearance": inverted_appearance,
        "message_visible": message_visible,
        "message_format": message_format,
        "message_centered": message_centered,
        "show_info_label": show_info,
        "info_text_centered": info_centered,
        "info_text_format": info_text_format,
        "initial_info": initial_info,
    }
    _context.show_progressbar.emit(config)


def hide_progressbar():
    _context.hide_progressbar.emit()


def update_progress(value: int, info: str | None = None):
    _context.update_progress.emit(value, info)
