from __future__ import annotations

import dataclasses
from typing import Type, Any, TypeVar, ForwardRef

from PySide2.QtWidgets import QWidget, QTextEdit

from ..common import CommonParameterWidget, CommonParameterWidgetConfig


@dataclasses.dataclass(frozen=True)
class TextEditConfig(CommonParameterWidgetConfig):

    @classmethod
    def target_widget_class(cls) -> Type["TextEdit"]:
        return TextEdit


class TextEdit(CommonParameterWidget):

    Self = TypeVar("Self", bound="TextEdit")
    ConfigClass = TextEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: TextEditConfig,
    ):
        self._config: TextEditConfig = config
        self._value_widget: QTextEdit | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QTextEdit:
        if self._value_widget is None:
            self._value_widget = QTextEdit(self)
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        self.value_widget.setPlainText(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.toPlainText()
