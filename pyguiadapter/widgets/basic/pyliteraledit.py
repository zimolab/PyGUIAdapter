import ast
import dataclasses

from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .base import BaseCodeEdit, BaseCodeEditConfig, StandaloneCodeEditorConfig
from ...codeeditor import PythonFormatter
from ...utils import PyLiteralType, type_check


@dataclasses.dataclass(frozen=True)
class PyLiteralEditConfig(BaseCodeEditConfig):
    """PyLiteralEdit的配置类"""

    default_value: PyLiteralType = ""
    """控件的默认值"""

    height: Optional[int] = None
    """inplace编辑器的高度"""

    width: Optional[int] = None
    """inplace编辑器的宽度"""

    standalone_editor: bool = True
    """是否使用独立（standalone）编辑器窗口"""

    standalone_editor_button_text: str = "Edit Python Literal"
    """standalone编辑器窗口打开按钮的文本"""

    standalone_editor_config: StandaloneCodeEditorConfig = dataclasses.field(
        default_factory=StandaloneCodeEditorConfig
    )
    """standalone编辑器配置"""

    initial_text: str = ""

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
