from __future__ import annotations

import ast
import dataclasses
from typing import Type, Union, TypeVar, Any

from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QWidget

from .base import BaseDataEditor, BaseDataEditorConfig
from .codeeditor import PythonCodeFormatter

PyLiteralType = Union[bool, int, float, bytes, str, list, tuple, dict, set]


@dataclasses.dataclass(frozen=True)
class PyLiteralEditorConfig(BaseDataEditorConfig):
    default_value: Any = None
    highlighter: Type[QPythonHighlighter] = QPythonHighlighter
    code_formatter: QPythonHighlighter = PythonCodeFormatter()
    initial_text: str = "None"

    @classmethod
    def target_widget_class(cls) -> Type["PyLiteralEditor"]:
        return PyLiteralEditor


class PyLiteralEditor(BaseDataEditor):
    Self = TypeVar("Self", bound="PythonLiteralEditor")
    ConfigClass = PyLiteralEditorConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: PyLiteralEditorConfig,
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> PyLiteralType:
        return ast.literal_eval(text)

    def from_data(self, data: PyLiteralType) -> str:
        if not isinstance(data, str):
            return str(data)
        return repr(data)
