import dataclasses
import warnings
from typing import Type, Optional, Union, Any

from qtpy.QtWidgets import QWidget, QSpinBox

from ...exceptions import ParameterError
from ...utils import type_check
from ...widgets.common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)


@dataclasses.dataclass(frozen=True)
class IntSpinBoxConfig(CommonParameterWidgetConfig):
    default_value: Optional[int] = 0
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
    ConfigClass: Type[IntSpinBoxConfig] = IntSpinBoxConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: IntSpinBoxConfig
    ):
        self._value_widget: Optional[QSpinBox] = None
        super().__init__(parent, parameter_name, config)

        assert config.max_value >= config.min_value

    @property
    def value_widget(self) -> QSpinBox:
        if self._value_widget is None:
            config: IntSpinBoxConfig = self.config
            self._value_widget = QSpinBox(self)
            self._value_widget.setMaximum(config.max_value)
            self._value_widget.setMinimum(config.min_value)
            self._value_widget.setSingleStep(config.step)
            self._value_widget.setPrefix(config.prefix or "")
            self._value_widget.setSuffix(config.suffix or "")
            if config.display_integer_base > 1:
                self._value_widget.setDisplayIntegerBase(config.display_integer_base)
            else:
                warnings.warn(
                    f"invalid display_integer_base value, this will be ignored: {config.display_integer_base}"
                )
        return self._value_widget

    def check_value_type(self, value: Any):
        if value == "":
            return
        type_check(value, (int, bool), allow_none=True)

    def set_value_to_widget(self, value: Union[int, bool]):
        if value == "":
            self._value_widget.setValue(0)
            return
        value = int(value)
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._value_widget.value()
