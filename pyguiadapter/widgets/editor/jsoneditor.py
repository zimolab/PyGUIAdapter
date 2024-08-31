from __future__ import annotations

import dataclasses
import json
import warnings
from typing import Type, TypeVar, Any

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ..common import CommonParameterWidget, CommonParameterWidgetConfig
from ...exceptions import ParameterValidationError


@dataclasses.dataclass(frozen=True)
class JsonEditorConfig(CommonParameterWidgetConfig):
    default_value: Any = dataclasses.field(default_factory=dict)
    font_size: int = 14
    indent_size: int = 2
    editor_min_height: int = 245
    standalone_editor: bool = False
    standalone_editor_button_text: str = "Edit"
    standalone_editor_title = "Any Editor"

    @classmethod
    def target_widget_class(cls) -> Type["JsonEditor"]:
        return JsonEditor


class JsonEditor(CommonParameterWidget):

    Self = TypeVar("Self", bound="AnyEditor")
    ConfigClass = JsonEditorConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: JsonEditorConfig,
    ):
        self._config: JsonEditorConfig = config
        self._value_widget: QWidget | None = None
        self._inline_editor: QCodeEditor | None = None
        self._standalone_editor_button: QPushButton | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QCodeEditor:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            layout = QVBoxLayout(self._value_widget)
            self._value_widget.setLayout(layout)

            self._inline_editor = QCodeEditor(self._value_widget)
            layout.addWidget(self._inline_editor)

            if self._config.standalone_editor:
                self._standalone_editor_button = QPushButton(self._value_widget)
                layout.addWidget(self._standalone_editor_button)

            self._setup_value_widget()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        try:
            indent_size = (
                self._config.indent_size if self._config.indent_size > 0 else 4
            )
            json_str = self._to_json_str(value, indent_size)
        except Exception as e:
            raise ParameterValidationError(
                parameter_name=self.parameter_name, message=str(e)
            )
        else:
            self._inline_editor.setPlainText(json_str)

    def get_value_from_widget(self) -> Any:
        try:
            obj = self._from_json_str(self._inline_editor.toPlainText())
        except Exception as e:
            raise ParameterValidationError(
                parameter_name=self.parameter_name, message=str(e)
            )
        else:
            return obj

    def _edit_in_standalone_editor(self):
        pass

    @staticmethod
    def _from_json_str(json_str: str) -> Any:
        return json.loads(json_str)

    @staticmethod
    def _to_json_str(obj: Any, indent_size: int) -> str:
        json_str = json.dumps(obj, indent=indent_size, ensure_ascii=False)
        return json_str

    def _setup_value_widget(self):
        highlighter = QJSONHighlighter()
        self._inline_editor.setHighlighter(highlighter)
        if self._config.font_size >= 0:
            self._inline_editor.setFontSize(self._config.font_size)
        else:
            warnings.warn(f"invalid font size: {self._config.font_size}")

        if self._config.indent_size >= 0:
            self._inline_editor.setDefaultIndent(self._config.indent_size)
            self._inline_editor.setTabReplace(True)
            self._inline_editor.setTabReplaceSize(self._config.indent_size)

        if self._config.editor_min_height > 0:
            self._inline_editor.setMinimumHeight(self._config.editor_min_height)

        if self._standalone_editor_button is not None:
            self._standalone_editor_button.setText(
                self._config.standalone_editor_button_text
            )
            self._standalone_editor_button.clicked.connect(
                self._edit_in_standalone_editor
            )
