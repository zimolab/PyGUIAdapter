import ast
import dataclasses
from typing import Type, Union, Optional

from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QWidget

from .base import BaseCodeEdit, BaseCodeEditConfig
from ...codeeditor import PythonFormatter

PyLiteralType = Union[bool, int, float, bytes, str, list, tuple, dict, set]

FILE_FILTERS = (
    "Python files (*.py);;Text files(*.txt);;Text files(*.text);;All files (*.*)"
)


@dataclasses.dataclass(frozen=True)
class PyLiteralEditConfig(BaseCodeEditConfig):
    default_value: PyLiteralType = ""
    highlighter: Type[QPythonHighlighter] = QPythonHighlighter
    formatter: QPythonHighlighter = PythonFormatter()
    initial_text: str = ""
    file_filters: str = FILE_FILTERS

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

    def _get_data(self, text: str) -> PyLiteralType:
        text = text.strip()
        return ast.literal_eval(text)

    def _set_data(self, data: PyLiteralType) -> str:
        if not isinstance(data, str):
            return str(data)
        return repr(data)
