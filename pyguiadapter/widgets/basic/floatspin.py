from __future__ import annotations

import dataclasses
from typing import Type

from qtpy.QtWidgets import QWidget, QDoubleSpinBox

from ...exceptions import ParameterError
from ...widgets.common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)


@dataclasses.dataclass(frozen=True)
class FloatSpinBoxConfig(CommonParameterWidgetConfig):
    default_value: float | None = 0.0
    min_value: float = -2147483648.0
    max_value: float = 2147483647.0
    step: float | None = None
    decimals: int | None = None
    prefix: str = ""
    suffix: str = ""

    @classmethod
    def target_widget_class(cls) -> Type["FloatSpinBox"]:
        return FloatSpinBox


class FloatSpinBox(CommonParameterWidget):
    ConfigClass: Type[FloatSpinBoxConfig] = FloatSpinBoxConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: FloatSpinBoxConfig
    ):
        self._value_widget: QDoubleSpinBox | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QDoubleSpinBox:
        if self._value_widget is None:
            config: FloatSpinBoxConfig = self.config
            self._value_widget = QDoubleSpinBox(self)
            self._value_widget.setMinimum(config.min_value)
            self._value_widget.setMaximum(config.max_value)
            step = config.step
            if step is not None and step > 0:
                self._value_widget.setSingleStep(step)

            decimals = config.decimals
            if decimals is not None and decimals > 0:
                self._value_widget.setDecimals(decimals)

            self._value_widget.setPrefix(config.prefix or "")
            self._value_widget.setSuffix(config.suffix or "")
        return self._value_widget

    def set_value_to_widget(self, value: float | int | str):
        try:
            value = float(value)
        except ValueError as e:
            raise ParameterError(self.parameter_name, str(e))
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> float:
        return self._value_widget.value()
