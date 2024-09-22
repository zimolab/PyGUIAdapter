from __future__ import annotations

import warnings
from typing import List, Tuple, Literal

from qtpy.QtCore import Qt, QUrl
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLineEdit, QInputDialog, QColorDialog

from .ucontext import _request_get_input
from .. import utils
from ..windows import FnExecuteWindow

EchoMode = QLineEdit.EchoMode
InputMethodHint = Qt.InputMethodHint
InputMethodHints = Qt.InputMethodHints


def get_text(
    title: str = "Input Text",
    label: str = "",
    echo: EchoMode | None = None,
    text: str = "",
    ime_hints: InputMethodHint | InputMethodHints | None = None,
) -> str | None:
    if echo is None:
        echo = EchoMode.Normal

    if ime_hints is None:
        ime_hints = InputMethodHint.ImhNone

    def _impl(wind: FnExecuteWindow | None) -> str | None:
        input_text, ok = QInputDialog.getText(
            wind, title, label, echo, text, inputMethodHints=ime_hints
        )
        if ok:
            return input_text
        return None

    return _request_get_input(_impl)


def get_multiline_text(
    title: str = "Input Text",
    label: str = "",
    text: str = "",
    ime_hints: InputMethodHint | InputMethodHints | None = None,
) -> str | None:

    if ime_hints is None:
        ime_hints = InputMethodHint.ImhNone

    def _impl(wind: FnExecuteWindow | None) -> str | None:
        input_text, ok = QInputDialog.getMultiLineText(
            wind, title, label, text, inputMethodHints=ime_hints
        )
        if not ok:
            return None
        return input_text

    return _request_get_input(_impl)


def get_int(
    title: str = "Input Integer",
    label: str = "",
    value: int = 0,
    min_value: int = -2147483647,
    max_value: int = 2147483647,
    step: int = 1,
) -> int | None:
    def _impl(wind: FnExecuteWindow | None) -> int | None:
        input_int, ok = QInputDialog.getInt(
            wind, title, label, value, min_value, max_value, step
        )
        if not ok:
            return None
        return input_int

    return _request_get_input(_impl)


def get_float(
    title: str = "Input Float",
    label: str = "",
    value: float = 0.0,
    min_value: float = -2147483647.0,
    max_value: float = 2147483647.0,
    decimals: int = 1,
) -> float | None:

    min_value = float(min_value)
    max_value = float(max_value)

    def _impl(wind: FnExecuteWindow | None) -> float | None:
        input_float, ok = QInputDialog.getDouble(
            wind, title, label, value, min_value, max_value, decimals
        )
        if not ok:
            return None
        return input_float

    return _request_get_input(_impl)


def get_selected_item(
    items: List[str],
    title: str = "Select Item",
    label: str = "",
    current: int = 0,
    editable: bool = False,
) -> str | None:
    def _impl(wind: FnExecuteWindow | None):
        selected_item, ok = QInputDialog.getItem(
            wind, title, label, items, current, editable=editable
        )
        if not ok:
            return None
        return selected_item

    return _request_get_input(_impl)


def _to_color(c: str | tuple | QColor) -> QColor:
    if isinstance(c, str):
        if hasattr(QColor, "fromString"):
            return QColor.fromString(c)
        color = QColor()
        color.setNamedColor(c)
        return color
    if isinstance(c, tuple):
        return QColor.fromRgb(*c)
    return c


def get_color(
    initial: QColor | str | tuple = Qt.white,
    title: str = "Select Color",
    alpha_channel: bool = True,
    return_type: Literal["tuple", "str", "QColor"] = "str",
) -> Tuple[int, int, int] | Tuple[int, int, int] | str | QColor | None:

    initial = _to_color(initial)

    def _impl(wind: FnExecuteWindow | None) -> QColor | None:
        if alpha_channel:
            color = QColorDialog.getColor(
                initial, wind, title, options=QColorDialog.ShowAlphaChannel
            )
        else:
            color = QColorDialog.getColor(initial, wind, title)
        if color.isValid():
            return utils.convert_color(color, return_type, alpha_channel)
        return None

    return _request_get_input(_impl)


def get_existing_directory(
    title: str = "Open Directory",
    start_dir: str = "",
) -> str | None:
    def _impl(wind: FnExecuteWindow | None) -> str | None:
        return utils.get_existing_directory(wind, title, start_dir) or None

    return _request_get_input(_impl)


def get_existing_directory_url(
    title: str = "Open Directory URL",
    start_dir: QUrl | None = None,
    supported_schemes: List[str] | None = None,
) -> QUrl:
    def _impl(wind: FnExecuteWindow | None) -> QUrl:
        return utils.get_existing_directory_url(
            wind, title, start_dir, supported_schemes
        )

    return _request_get_input(_impl)


def get_open_file(
    title: str = "Open File",
    start_dir: str = "",
    filters: str = "",
) -> str | None:
    def _impl(wind: FnExecuteWindow | None) -> str | None:
        return utils.get_open_file(wind, title, start_dir, filters)

    return _request_get_input(_impl)


def get_open_files(
    title: str = "Open Files",
    start_dir: str = "",
    filters: str = "",
) -> List[str] | None:
    def _impl(wind: FnExecuteWindow | None) -> List[str] | None:
        return utils.get_open_files(wind, title, start_dir, filters)

    return _request_get_input(_impl)


def get_save_file(
    title: str = "Save File",
    start_dir: str = "",
    filters: str = "",
) -> str | None:
    def _impl(wind: FnExecuteWindow | None) -> str | None:
        return utils.get_save_file(wind, title, start_dir, filters)

    return _request_get_input(_impl)
