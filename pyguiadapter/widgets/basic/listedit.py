import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .base import StandaloneCodeEditorConfig
from .pyliteraledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class ListEditConfig(PyLiteralEditConfig):
    """ListEdit的配置类"""

    default_value: Optional[list] = dataclasses.field(default_factory=list)
    """控件的默认值"""

    height: Optional[int] = None
    """inplace编辑器的高度"""

    width: Optional[int] = None
    """inplace编辑器的宽度"""

    standalone_editor: bool = True
    """是否启用独立（standalone）代码编辑器"""

    standalone_editor_button: bool = "Edit List"
    """standalone编辑器启动按钮文本"""

    standalone_editor_config: StandaloneCodeEditorConfig = StandaloneCodeEditorConfig()
    """standalone编辑器配置"""

    initial_text: str = "[]"

    @classmethod
    def target_widget_class(cls) -> Type["ListEdit"]:
        return ListEdit


class ListEdit(PyLiteralEdit):
    ConfigClass = ListEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: ListEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        if value == "":
            return
        type_check(value, (list,), allow_none=True)

    def _get_data(self, text: str) -> Optional[list]:
        text = text.strip()
        if text is None or text == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, list):
            raise ValueError(f"not a list")
        return data

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, list):
            raise ValueError(f"not a list: {data}")
        return super()._set_data(data)
