import dataclasses
import json
from typing import Type, Any, Optional

from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtWidgets import QWidget

from ..basic.base import BaseCodeEdit, BaseCodeEditConfig, StandaloneCodeEditorConfig
from ...codeeditor import JsonFormatter

JSON_FILE_FILTERS = (
    "JSON files (*.json);;Text files(*.txt);;Text files(*.text);;All files (*.*)"
)


@dataclasses.dataclass(frozen=True)
class JsonEditConfig(BaseCodeEditConfig):
    """JsonEdit的配置类。"""

    default_value: Optional[Any] = dataclasses.field(default_factory=set)
    """控件的默认值"""

    height: Optional[int] = 230
    """inplace编辑器的高度"""

    width: Optional[int] = None
    """inplace编辑器的宽度"""

    standalone_editor: bool = True
    """是否启用独立（standalone）代码编辑器"""

    standalone_editor_button: bool = "Edit Json"
    """standalone编辑器启动按钮文本"""

    standalone_editor_config: StandaloneCodeEditorConfig = StandaloneCodeEditorConfig()
    """standalone编辑器配置"""

    indent_size: int = 2
    """json格式化缩进大小"""

    initial_text: str = "{}"

    highlighter: Type[QJSONHighlighter] = QJSONHighlighter
    formatter: JsonFormatter = dataclasses.field(default_factory=JsonFormatter)

    @classmethod
    def target_widget_class(cls) -> Type["JsonEdit"]:
        return JsonEdit


class JsonEdit(BaseCodeEdit):
    ConfigClass = JsonEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: JsonEditConfig,
    ):
        super().__init__(parent, parameter_name, config)

    def _get_data(self, text: str) -> Any:
        try:
            return json.loads(text)
        except Exception as e:
            raise ValueError(f"not a json str: {e}") from e

    def _set_data(self, data: Any) -> str:
        config: JsonEditConfig = self.config
        try:
            return json.dumps(data, ensure_ascii=False, indent=config.indent_size)
        except Exception as e:
            raise ValueError(f"not a json object: {e}") from e
