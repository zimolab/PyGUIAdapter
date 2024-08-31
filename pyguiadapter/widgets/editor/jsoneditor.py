from __future__ import annotations

import dataclasses
import json
from typing import Type, TypeVar, Any

from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtWidgets import QWidget

from .base import BaseDataEditor, BaseDataEditorConfig
from .codeeditor import JsonFormatter


@dataclasses.dataclass(frozen=True)
class JsonEditorConfig(BaseDataEditorConfig):
    default_value: Any = dataclasses.field(default_factory=dict)
    highlighter: Type[QJSONHighlighter] = QJSONHighlighter
    code_formatter: JsonFormatter = dataclasses.field(default_factory=JsonFormatter)

    @classmethod
    def target_widget_class(cls) -> Type["JsonEditor"]:
        return JsonEditor


class JsonEditor(BaseDataEditor):

    Self = TypeVar("Self", bound="JsonEditor")
    ConfigClass = JsonEditorConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: JsonEditorConfig,
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> Any:
        return json.loads(text)

    def from_data(self, data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=self._config.indent_size)
