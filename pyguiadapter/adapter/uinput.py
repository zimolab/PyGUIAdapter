from concurrent.futures import Future
from typing import List, Tuple, Literal, Callable, Any, Optional, Union, Sequence

from qtpy.QtCore import QUrl
from qtpy.QtGui import QColor

from .ucontext import _context
from ..utils import EchoMode, inputdialog, filedialog, IconType, PyLiteralType
from ..utils.inputdialog import LineWrapMode
from ..windows.fnexec import FnExecuteWindow


def _request_get_input(get_input_impl: Callable[[FnExecuteWindow], Any]) -> Any:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.get_input_requested.emit(result_future, get_input_impl)
    return result_future.result()


def get_string(
    title: str = "Input Text",
    label: str = "",
    echo: Optional[EchoMode] = None,
    text: str = "",
) -> Optional[str]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return inputdialog.input_string(wind, title, label, echo, text)

    return _request_get_input(_impl)


def get_text(
    title: str = "Input Text", label: str = "", text: str = ""
) -> Optional[str]:

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return inputdialog.input_text(wind, title, label, text)

    return _request_get_input(_impl)


def get_int(
    title: str = "Input Integer",
    label: str = "",
    value: int = 0,
    min_value: int = -2147483647,
    max_value: int = 2147483647,
    step: int = 1,
) -> Optional[int]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[int]:
        return inputdialog.input_integer(
            wind, title, label, value, min_value, max_value, step
        )

    return _request_get_input(_impl)


def get_float(
    title: str = "Input Float",
    label: str = "",
    value: float = 0.0,
    min_value: float = -2147483647.0,
    max_value: float = 2147483647.0,
    decimals: int = 3,
    step: float = 1.0,
) -> Optional[float]:

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[float]:
        return inputdialog.input_float(
            wind, title, label, value, min_value, max_value, decimals, step
        )

    return _request_get_input(_impl)


def get_selected_item(
    items: List[str],
    title: str = "Select Item",
    label: str = "",
    current: int = 0,
    editable: bool = False,
) -> Optional[str]:
    def _impl(wind: Optional[FnExecuteWindow]):
        return inputdialog.select_item(wind, items, title, label, current, editable)

    return _request_get_input(_impl)


def get_color(
    initial: Union[QColor, str, tuple] = "white",
    title: str = "",
    alpha_channel: bool = True,
    return_type: Literal["tuple", "str", "QColor"] = "str",
) -> Union[Tuple[int, int, int], Tuple[int, int, int], str, QColor, None]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[QColor]:
        return inputdialog.input_color(wind, initial, title, alpha_channel, return_type)

    return _request_get_input(_impl)


def get_json_object(
    title: str = "Input Json",
    icon: IconType = None,
    size: Tuple[int, int] = (600, 400),
    ok_button_text: str = "Ok",
    cancel_button_text: Optional[str] = "Cancel",
    initial_text: str = "",
    auto_indent: bool = True,
    indent_size: int = 4,
    auto_parentheses: bool = True,
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth,
    line_wrap_width: int = 88,
    font_family: Union[str, Sequence[str], None] = "Consolas",
    font_size: Optional[int] = None,
    **kwargs,
) -> Any:
    def _impl(wind: Optional[FnExecuteWindow]) -> Any:
        return inputdialog.input_json_object(
            wind,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            initial_text=initial_text,
            auto_indent=auto_indent,
            indent_size=indent_size,
            auto_parentheses=auto_parentheses,
            line_wrap_mode=line_wrap_mode,
            line_wrap_width=line_wrap_width,
            font_family=font_family,
            font_size=font_size,
            **kwargs,
        )

    return _request_get_input(_impl)


def get_py_literal(
    title: str = "Input Python Literal",
    icon: IconType = None,
    size: Tuple[int, int] = (600, 400),
    ok_button_text: str = "Ok",
    cancel_button_text: Optional[str] = "Cancel",
    initial_text: str = "",
    auto_indent: bool = True,
    indent_size: int = 4,
    auto_parentheses: bool = True,
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth,
    line_wrap_width: int = 88,
    font_family: Union[str, Sequence[str], None] = "Consolas",
    font_size: Optional[int] = None,
    **kwargs,
) -> PyLiteralType:
    def _impl(wind: Optional[FnExecuteWindow]) -> Any:
        return inputdialog.input_py_literal(
            wind,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            initial_text=initial_text,
            auto_indent=auto_indent,
            indent_size=indent_size,
            auto_parentheses=auto_parentheses,
            line_wrap_mode=line_wrap_mode,
            line_wrap_width=line_wrap_width,
            font_family=font_family,
            font_size=font_size,
            **kwargs,
        )

    return _request_get_input(_impl)


def get_existing_directory(
    title: str = "",
    start_dir: str = "",
) -> Optional[str]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return filedialog.get_existing_directory(wind, title, start_dir) or None

    return _request_get_input(_impl)


def get_existing_directory_url(
    title: str = "",
    start_dir: Optional[QUrl] = None,
    supported_schemes: Optional[List[str]] = None,
) -> QUrl:
    def _impl(wind: Optional[FnExecuteWindow]) -> QUrl:
        return filedialog.get_existing_directory_url(
            wind, title, start_dir, supported_schemes
        )

    return _request_get_input(_impl)


def get_open_file(
    title: str = "",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return filedialog.get_open_file(wind, title, start_dir, filters)

    return _request_get_input(_impl)


def get_open_files(
    title: str = "",
    start_dir: str = "",
    filters: str = "",
) -> Optional[List[str]]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[List[str]]:
        return filedialog.get_open_files(wind, title, start_dir, filters)

    return _request_get_input(_impl)


def get_save_file(
    title: str = "",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return filedialog.get_save_file(wind, title, start_dir, filters)

    return _request_get_input(_impl)
