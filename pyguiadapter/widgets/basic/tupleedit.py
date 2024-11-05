import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .base import StandaloneCodeEditorConfig
from .pyliteraledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class TupleEditConfig(PyLiteralEditConfig):
    """TupleEdit的配置类"""

    default_value: Optional[tuple] = ()
    """控件的默认值"""

    height: Optional[int] = None
    """inplace编辑器的高度"""

    width: Optional[int] = None
    """inplace编辑器的宽度"""

    standalone_editor: bool = True
    """是否启用独立（standalone）代码编辑器"""

    standalone_editor_button_text: str = "Edit Tuple"
    """standalone编辑器启动按钮文本"""

    standalone_editor_config: StandaloneCodeEditorConfig = dataclasses.field(
        default_factory=StandaloneCodeEditorConfig
    )
    """standalone编辑器配置"""

    initial_text: str = "()"

    @classmethod
    def target_widget_class(cls) -> Type["TupleEdit"]:
        return TupleEdit


class TupleEdit(PyLiteralEdit):
    ConfigClass = TupleEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: TupleEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        type_check(value, (tuple,), allow_none=True)

    def _get_data(self, text: str) -> Optional[tuple]:
        text = text.strip()
        if text is None or text == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, tuple):
            raise ValueError(f"not a tuple")
        return data

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, tuple):
            raise ValueError(f"not a tuple: {data}")
        return super()._set_data(data)
