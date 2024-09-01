from __future__ import annotations

import dataclasses
from typing import Type, Any, TypeVar

from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QWidget, QLineEdit, QDoubleSpinBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...exceptions import ParameterValidationError


@dataclasses.dataclass(frozen=True)
class FloatSpinBoxConfig(CommonParameterWidgetConfig):
    min_value: float = -2147483648.0
    max_value: float = 2147483647.0
    step: int = 0.01
    decimals: int = 2
    prefix: str = ""
    suffix: str = ""

    @classmethod
    def target_widget_class(cls) -> Type["FloatSpinBox"]:
        return FloatSpinBox


class FloatSpinBox(CommonParameterWidget):

    Self = TypeVar("Self", bound="FloatSpinBox")
    ConfigClass = FloatSpinBoxConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: FloatSpinBoxConfig
    ):
        self._config: FloatSpinBoxConfig = config
        self._value_widget: QDoubleSpinBox | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QDoubleSpinBox:
        if self._value_widget is None:
            self._value_widget = QDoubleSpinBox(self)
            self._value_widget.setMinimum(self._config.min_value)
            self._value_widget.setMaximum(self._config.max_value)
            if self._config.step is not None and self._config.step > 0:
                self._value_widget.setSingleStep(self._config.step)
            if self._config.decimals is not None and self._config.decimals > 0:
                self._value_widget.setDecimals(self._config.decimals)
            self._value_widget.setPrefix(self._config.prefix or "")
            self._value_widget.setSuffix(self._config.suffix or "")
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        try:
            value = float(value)
        except ValueError as e:
            raise ParameterValidationError(self.parameter_name, str(e))
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> float:
        return self._value_widget.value()


@dataclasses.dataclass(frozen=True)
class FloatLineEditConfig(CommonParameterWidgetConfig):
    min_value: int = -2147483648.0
    max_value: int = 2147483647.0
    decimals: int = 2
    scientific_notation: bool = False
    fallback_value: int = 0.0

    @classmethod
    def target_widget_class(cls) -> Type["FloatLineEdit"]:
        return FloatLineEdit


class FloatLineEdit(CommonParameterWidget):

    Self = TypeVar("Self", bound="FloatLineEdit")
    ConfigClass = FloatLineEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: FloatLineEditConfig
    ):
        self._config: FloatLineEditConfig = config
        self._value_widget: QLineEdit | None = None
        self._validator: QDoubleValidator | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            self._value_widget = QLineEdit(self)
            self._validator = QDoubleValidator(
                self._config.min_value,
                self._config.max_value,
                self._config.decimals,
                self._value_widget,
            )
            if self._config.scientific_notation:
                notation = QDoubleValidator.ScientificNotation
            else:
                notation = QDoubleValidator.StandardNotation
            self._validator.setNotation(notation)
            self._value_widget.setValidator(self._validator)
            self._value_widget.setText(str(self._config.fallback_value))
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        if value == "":
            value = self._config.fallback_value
        self._value_widget.setText(str(value))

    def get_value_from_widget(self) -> float:
        value = self._value_widget.text()
        if not value:
            return self._config.fallback_value
        try:
            value = float(value)
        except ValueError as e:
            raise ParameterValidationError(self.parameter_name, str(e))
        else:
            return value
