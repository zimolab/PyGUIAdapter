import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .base import StandaloneCodeEditorConfig
from .pyliteraledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType
from ... import utils
from ...fn import ParameterInfo
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class DictEditConfig(PyLiteralEditConfig):
    """DictEdit的配置类"""

    default_value: Optional[dict] = dataclasses.field(default_factory=dict)
    """控件的默认值"""

    height: Optional[int] = None
    """inplace编辑器的高度"""

    width: Optional[int] = None
    """inplace编辑器的宽度"""

    standalone_editor: bool = True
    """是否启用独立（standalone）代码编辑器"""

    standalone_editor_button: bool = "Edit Dict"
    """standalone编辑器启动按钮文本"""

    standalone_editor_config: StandaloneCodeEditorConfig = dataclasses.field(
        default_factory=StandaloneCodeEditorConfig
    )
    """standalone编辑器配置"""

    initial_text: str = "{}"

    @classmethod
    def target_widget_class(cls) -> Type["DictEdit"]:
        return DictEdit


class DictEdit(PyLiteralEdit):
    ConfigClass = DictEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: DictEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def _get_data(self, text: str) -> Optional[dict]:
        if text is None or text.strip() == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, dict):
            raise ValueError(f"not a dict")
        return data

    def check_value_type(self, value: Any):
        type_check(value, (dict,), allow_none=True)

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, dict):
            raise ValueError(f"not a dict: {data}")
        return super()._set_data(data)

    @classmethod
    def _dict_mapping_rule(
        cls, parameter_info: ParameterInfo
    ) -> Optional[Type["DictEdit"]]:
        return DictEdit if utils.is_subclass_of(parameter_info.type, dict) else None
