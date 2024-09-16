from __future__ import annotations

import ast
import dataclasses
from typing import Type, Union, Any

from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QWidget

from .base import BaseCodeEdit, BaseCodeEditConfig
from ...codeeditor import PythonCodeFormatter

PyLiteralType = Union[bool, int, float, bytes, str, list, tuple, dict, set]


@dataclasses.dataclass(frozen=True)
class PyLiteralEditConfig(BaseCodeEditConfig):
    default_value: Any = None
    highlighter: Type[QPythonHighlighter] = QPythonHighlighter
    formatter: QPythonHighlighter = PythonCodeFormatter()
    initial_text: str = "None"

    @classmethod
    def target_widget_class(cls) -> Type["PyLiteralEdit"]:
        return PyLiteralEdit


class PyLiteralEdit(BaseCodeEdit):
    ConfigClass = PyLiteralEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: PyLiteralEditConfig,
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> PyLiteralType:
        return ast.literal_eval(text)

    def from_data(self, data: PyLiteralType) -> str:
        if not isinstance(data, str):
            return str(data)
        return repr(data)
