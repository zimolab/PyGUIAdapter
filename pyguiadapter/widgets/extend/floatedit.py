from __future__ import annotations

import dataclasses
from typing import Type, Any

from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QWidget, QLineEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...exceptions import ParameterError


@dataclasses.dataclass(frozen=True)
class FloatLineEditConfig(CommonParameterWidgetConfig):
    default_value: float | None = 0.0
    min_value: float = -2147483648.0
    max_value: float = 2147483647.0
    decimals: int = 2
    scientific_notation: bool = False
    empty_value: float = 0.0

    @classmethod
    def target_widget_class(cls) -> Type["FloatLineEdit"]:
        return FloatLineEdit


class FloatLineEdit(CommonParameterWidget):
    ConfigClass = FloatLineEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: FloatLineEditConfig
    ):
        self._value_widget: QLineEdit | None = None
        self._validator: QDoubleValidator | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            config: FloatLineEditConfig = self.config
            self._value_widget = QLineEdit(self)
            self._validator = QDoubleValidator(
                config.min_value,
                config.max_value,
                config.decimals,
                self._value_widget,
            )
            if config.scientific_notation:
                notation = QDoubleValidator.ScientificNotation
            else:
                notation = QDoubleValidator.StandardNotation
            self._validator.setNotation(notation)
            self._value_widget.setValidator(self._validator)
            self._value_widget.setText(str(config.empty_value))
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        self._config: FloatLineEditConfig
        if value == "":
            value = self._config.empty_value
        self._value_widget.setText(str(value))

    def get_value_from_widget(self) -> float:
        self._config: FloatLineEditConfig
        value = self._value_widget.text()
        if not value:
            return self._config.empty_value
        try:
            value = float(value)
        except ValueError as e:
            raise ParameterError(self.parameter_name, str(e))
        else:
            return value
