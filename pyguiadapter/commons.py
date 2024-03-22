import enum
import os
import warnings
from typing import TypeVar, Optional

from PyQt6.QtWidgets import QLayout
from function2widgets.parser import FunctionDescriptionParser
from function2widgets.factory import ParameterWidgetFactory

T = TypeVar("T")


__res_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "res/"))

__icon_dir = os.path.join(__res_dir, "icons")
__icon_file_ext = ".svg"

__font_dir = os.path.join(__res_dir, "fonts")

__function_parser = FunctionDescriptionParser()
__widget_factory = ParameterWidgetFactory()


class DocumentFormat(enum.Enum):
    HTML = "html"
    MARKDOWN = "markdown"
    PLAIN = "plain"


def get_function_parser() -> FunctionDescriptionParser:
    global __function_parser
    return __function_parser


def get_widget_factory() -> ParameterWidgetFactory:
    global __widget_factory
    return __widget_factory


def get_res_dir() -> str:
    global __res_dir
    return __res_dir


def set_res_dir(res_dir: str):
    global __res_dir
    __res_dir = res_dir


def get_icon_dir() -> str:
    global __icon_dir
    return __icon_dir


def set_icon_dir(icon_dir: str):
    global __icon_dir
    __icon_dir = icon_dir


def get_icon_file_ext() -> str:
    global __icon_file_ext
    return __icon_file_ext


def set_icon_file_ext(icon_file_ext: str):
    global __icon_file_ext
    __icon_file_ext = icon_file_ext


def get_font_dir(path: str) -> str:
    global __font_dir
    return os.path.join(__res_dir, path)


def get_icon_file(icon_name: str):
    global __icon_dir
    global __icon_file_ext
    if os.path.isfile(icon_name):
        return icon_name
    return os.path.join(__icon_dir, f"{icon_name}{__icon_file_ext}")


def safe_read(filename: str, encoding: str = "utf-8") -> Optional[str]:
    if not os.path.isfile(filename):
        return None
    try:
        with open(filename, "r", encoding=encoding) as f:
            return f.read()
    except BaseException as e:
        warnings.warn(f"failed to read file '{filename}': {e}")
        return None


def clear_layout(layout: QLayout) -> None:
    if not layout:
        return
    while layout.count() > 0:
        item = layout.takeAt(0)

        widget = item.widget()
        if widget:
            widget.deleteLater()

        child_layout = item.layout()
        if child_layout:
            clear_layout(child_layout)
            continue

        spacer_item = item.spacerItem()
        if spacer_item:
            layout.removeItem(spacer_item)
