import dataclasses
from typing import Type, Optional, Union, Any

from qtpy.QtWidgets import QWidget, QDoubleSpinBox

from ...exceptions import ParameterError
from ...utils import type_check
from ...widgets.common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)


@dataclasses.dataclass(frozen=True)
class FloatSpinBoxConfig(CommonParameterWidgetConfig):
    default_value: Optional[float] = 0.0
    min_value: float = -2147483648.0
    max_value: float = 2147483647.0
    step: Optional[float] = 1.0
    decimals: Optional[int] = 2
    prefix: str = ""
    suffix: str = ""

    @classmethod
    def target_widget_class(cls) -> Type["FloatSpinBox"]:
        return FloatSpinBox


class FloatSpinBox(CommonParameterWidget):
    ConfigClass: Type[FloatSpinBoxConfig] = FloatSpinBoxConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: FloatSpinBoxConfig
    ):
        self._value_widget: Optional[QDoubleSpinBox] = None
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

    def check_value_type(self, value: Any):
        if value == "":
            return
        type_check(value, (float, int), allow_none=True)

    def set_value_to_widget(self, value: Union[float, int, str]):
        if value == "":
            self._value_widget.setValue(0.0)
        value = float(value)
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> float:
        return self._value_widget.value()
