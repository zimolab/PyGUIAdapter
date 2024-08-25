from __future__ import annotations

import dataclasses
from typing import Type, Any, TypeVar

from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import QSpinBox, QWidget, QLineEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...exceptions import ParameterValidationError


@dataclasses.dataclass(frozen=True)
class IntSpinBoxConfig(CommonParameterWidgetConfig):
    min_value: int = -2147483648
    max_value: int = 2147483647
    step: int = 1
    prefix: str = ""
    suffix: str = ""
    display_integer_base: int = 10

    @classmethod
    def target_widget_class(cls) -> Type["IntSpinBox"]:
        return IntSpinBox


class IntSpinBox(CommonParameterWidget):

    Self = TypeVar("Self", bound="IntSpinBox")
    ConfigClass = IntSpinBoxConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: IntSpinBoxConfig
    ):
        self._config: IntSpinBoxConfig = config
        super().__init__(parent, parameter_name, config)

        self._value_widget: QSpinBox = QSpinBox(self)
        self._value_widget.setMinimum(self._config.min_value)
        self._value_widget.setMaximum(self._config.max_value)
        self._value_widget.setSingleStep(self._config.step)
        self._value_widget.setPrefix(self._config.prefix or "")
        self._value_widget.setSuffix(self._config.suffix or "")
        if self._config.display_integer_base > 0:
            self._value_widget.setDisplayIntegerBase(self._config.display_integer_base)

    @property
    def value_widget(self) -> QSpinBox:
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        try:
            value = int(value)
        except ValueError as e:
            raise ParameterValidationError(self.parameter_name, str(e))
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._value_widget.value()


@dataclasses.dataclass(frozen=True)
class IntLineEditConfig(CommonParameterWidgetConfig):
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
        super().__init__(parent, parameter_name, config)

        self._value_widget: QLineEdit = QLineEdit(self)
        self._validator = QIntValidator(
            self._config.min_value, self._config.max_value, self._value_widget
        )
        self._value_widget.setValidator(self._validator)
        self._value_widget.setText(str(self._config.fallback_value))

    @property
    def value_widget(self) -> QLineEdit:
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
            raise ParameterValidationError(self.parameter_name, str(e))
        else:
            return value
