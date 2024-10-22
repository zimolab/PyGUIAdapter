import ast
import dataclasses

from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .base import BaseCodeEdit, BaseCodeEditConfig
from ...codeeditor import PythonFormatter
from ...utils import PyLiteralType, type_check

FILE_FILTERS = (
    "Python files (*.py);;Text files(*.txt);;Text files(*.text);;All files (*.*)"
)


@dataclasses.dataclass(frozen=True)
class PyLiteralEditConfig(BaseCodeEditConfig):
    default_value: PyLiteralType = ""
    initial_text: str = ""
    file_filters: str = FILE_FILTERS
    # DON'T CHANGE THE VALUES BELOW
    highlighter: Type[QPythonHighlighter] = QPythonHighlighter
    formatter: QPythonHighlighter = PythonFormatter()

    @classmethod
    def target_widget_class(cls) -> Type["PyLiteralEdit"]:
        return PyLiteralEdit


class PyLiteralEdit(BaseCodeEdit):
    ConfigClass = PyLiteralEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: PyLiteralEditConfig,
    ):
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        type_check(
            value,
            allowed_types=(bool, int, float, bytes, str, list, tuple, dict, set),
            allow_none=True,
        )

    def _get_data(self, text: str) -> PyLiteralType:
        text = text.strip()
        try:
            return ast.literal_eval(text)
        except Exception as e:
            raise ValueError(f"not a python literal: {e}") from e

    def _set_data(self, data: PyLiteralType) -> str:
        if not isinstance(data, str):
            return str(data)
        return repr(data)
