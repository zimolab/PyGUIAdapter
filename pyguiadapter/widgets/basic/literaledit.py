import ast
import dataclasses
from typing import Type, Optional, Any

from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QWidget

from .base import BaseCodeEdit, BaseCodeEditConfig
from ...codeeditor import PythonFormatter
from ...exceptions import ParameterError
from ...utils import PyLiteralType

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

    def check_value_type(self, value: Any):
        if not isinstance(
            value, (bool, int, float, bytes, str, list, tuple, dict, set, type(None))
        ):
            raise ParameterError(
                parameter_name=self.parameter_name,
                message=f"invalid type of '{self.parameter_name}': expect literal, got {type(value)}",
            )

    def _get_data(self, text: str) -> PyLiteralType:
        text = text.strip()
        return ast.literal_eval(text)

    def _set_data(self, data: PyLiteralType) -> str:
        if not isinstance(data, str):
            return str(data)
        return repr(data)
