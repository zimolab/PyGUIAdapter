from __future__ import annotations

import dataclasses
import json
from typing import Type, TypeVar, Any

from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtWidgets import QWidget

from .base import BaseDataEdit, BaseDataEditConfig
from ..codeeditor import JsonFormatter


@dataclasses.dataclass(frozen=True)
class JsonEditConfig(BaseDataEditConfig):
    default_value: Any = dataclasses.field(default_factory=dict)
    highlighter: Type[QJSONHighlighter] = QJSONHighlighter
    code_formatter: JsonFormatter = dataclasses.field(default_factory=JsonFormatter)

    @classmethod
    def target_widget_class(cls) -> Type["JsonEdit"]:
        return JsonEdit


class JsonEdit(BaseDataEdit):

    Self = TypeVar("Self", bound="JsonEdit")
    ConfigClass = JsonEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: JsonEditConfig,
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> Any:
        return json.loads(text)

    def from_data(self, data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=self._config.indent_size)
