from __future__ import annotations

import dataclasses
from typing import Any, TypeVar, Type

from qtpy.QtWidgets import QWidget, QLineEdit

from ..common import CommonParameterWidget, CommonParameterWidgetConfig
from ...paramwidget import BaseParameterWidget


@dataclasses.dataclass(frozen=True)
class LineEditConfig(CommonParameterWidgetConfig):
    @classmethod
    def target_widget_class(cls) -> Type[LineEdit]:
        return LineEdit


class LineEdit(CommonParameterWidget):
    Self = TypeVar("Self", bound="LineEdit")
    ConfigClass = LineEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: LineEditConfig
    ):
        self._config: LineEditConfig = config
        self._value_widget = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            self._value_widget = QLineEdit(self)
            self._value_widget.setObjectName(self.parameter_name)
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        self.value_widget.setText(str(value))

    def get_value_from_widget(self) -> str:
        return self.value_widget.text()
