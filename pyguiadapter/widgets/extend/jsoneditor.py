import dataclasses
import json
from typing import Type, Any, Optional

from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtWidgets import QWidget

from ..basic.base import BaseCodeEdit, BaseCodeEditConfig
from ...codeeditor import JsonFormatter

JSON_FILE_FILTERS = (
    "JSON files (*.json);;Text files(*.txt);;Text files(*.text);;All files (*.*)"
)
INDENT_SIZE = 4


@dataclasses.dataclass(frozen=True)
class JsonEditConfig(BaseCodeEditConfig):
    default_value: Any = dataclasses.field(default_factory=dict)
    highlighter: Type[QJSONHighlighter] = QJSONHighlighter
    indent_size: int = INDENT_SIZE
    formatter: JsonFormatter = dataclasses.field(default_factory=JsonFormatter)
    file_filters: str = JSON_FILE_FILTERS

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
        return json.loads(text)

    def _set_data(self, data: Any) -> str:
        config: JsonEditConfig = self.config
        return json.dumps(data, ensure_ascii=False, indent=config.indent_size)
