from __future__ import annotations

import dataclasses
from typing import Type, Any, TypeVar

from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import QWidget, QLineEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...exceptions import ParameterError


@dataclasses.dataclass(frozen=True)
class IntLineEditConfig(CommonParameterWidgetConfig):
    default_value: int | None = 0
    min_value: int = -2147483648
    max_value: int = 2147483647
    fallback_value: int = 0

    @classmethod
    def target_widget_class(cls) -> Type["IntLineEdit"]:
        return IntLineEdit


class IntLineEdit(CommonParameterWidget):

    Self = TypeVar("Self", bound="IntLineEdit")
    ConfigClass = IntLineEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: IntLineEditConfig
    ):
        self._config: IntLineEditConfig = config
        self._validator: QIntValidator | None = None
        self._value_widget: QLineEdit | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            self._value_widget = QLineEdit(self)
            self._validator = QIntValidator(
                self._config.min_value, self._config.max_value, self._value_widget
            )
            self._value_widget.setValidator(self._validator)
            self._value_widget.setText(str(self._config.fallback_value))
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        if value == "":
            value = self._config.fallback_value
        self._value_widget.setText(str(value))

    def get_value_from_widget(self) -> int:
        value = self._value_widget.text()
        if not value:
            return self._config.fallback_value
        try:
            value = int(value)
        except ValueError as e:
            raise ParameterError(self.parameter_name, str(e))
        else:
            return value
