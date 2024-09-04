from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, Any

from qtpy.QtWidgets import QWidget, QDoubleSpinBox

from ...exceptions import ParameterValidationError
from ...widgets.common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)


@dataclasses.dataclass(frozen=True)
class FloatSpinBoxConfig(CommonParameterWidgetConfig):
    default_value: float = 0.0
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
