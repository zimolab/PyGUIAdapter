from __future__ import annotations

import dataclasses
import json
import warnings
from abc import abstractmethod
from trace import Trace
from typing import Type, TypeVar, Any

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ..common import CommonParameterWidget, CommonParameterWidgetConfig
from ...exceptions import ParameterValidationError


@dataclasses.dataclass(frozen=True)
class BaseEditorConfig(CommonParameterWidgetConfig):

    standalone_editor: bool = False
    standalone_editor_configs

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseEditor"]:
        pass


class BaseEditor(CommonParameterWidget):
    Self = TypeVar("Self", bound="BaseEditor")
    ConfigClass = BaseEditorConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BaseEditorConfig,
    ):
        self._config: BaseEditorConfig = config
        self._value_widget: QWidget | None = None
        self._editor: QCodeEditor | None = None
        self._standalone_editor_button: QPushButton | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._editor = QCodeEditor(self._value_widget)
            self._standalone_editor_button = QPushButton(self._value_widget)

            layout = QVBoxLayout(self._value_widget)
            layout.addWidget(self._editor)
            layout.addWidget(self._standalone_editor_button)

        return self._value_widget

    def set_value_to_widget(self, value: Any):
        pass

    def get_value_from_widget(self) -> Any:
        pass
