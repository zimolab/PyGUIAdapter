from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, Any

from qtpy.QtWidgets import QWidget, QSpinBox

from ...exceptions import ParameterError
from ...widgets.common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)


@dataclasses.dataclass(frozen=True)
class IntSpinBoxConfig(CommonParameterWidgetConfig):
    default_value: int = 0
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
        self._value_widget: QSpinBox | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QSpinBox:
        if self._value_widget is None:
            self._value_widget = QSpinBox(self)
            self._value_widget.setMinimum(self._config.min_value)
            self._value_widget.setMaximum(self._config.max_value)
            self._value_widget.setSingleStep(self._config.step)
            self._value_widget.setPrefix(self._config.prefix or "")
            self._value_widget.setSuffix(self._config.suffix or "")
            if self._config.display_integer_base > 0:
                self._value_widget.setDisplayIntegerBase(
                    self._config.display_integer_base
                )
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        try:
            value = int(value)
        except ValueError as e:
            raise ParameterError(self.parameter_name, str(e))
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._value_widget.value()
