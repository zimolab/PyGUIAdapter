import dataclasses

from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import QWidget, QLineEdit
from typing import Type, Any, Optional

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class IntLineEditConfig(CommonParameterWidgetConfig):
    default_value: Optional[int] = 0
    min_value: int = -2147483648
    max_value: int = 2147483647
    empty_value: int = 0

    @classmethod
    def target_widget_class(cls) -> Type["IntLineEdit"]:
        return IntLineEdit


class IntLineEdit(CommonParameterWidget):
    ConfigClass = IntLineEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: IntLineEditConfig
    ):
        self._validator: Optional[QIntValidator] = None
        self._value_widget: Optional[QLineEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        self._config: IntLineEditConfig
        if self._value_widget is None:
            self._value_widget = QLineEdit(self)
            self._validator = QIntValidator(
                self._config.min_value, self._config.max_value, self._value_widget
            )
            self._value_widget.setValidator(self._validator)
            self._value_widget.setText(str(self._config.empty_value))
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        self._config: IntLineEditConfig
        if value == "":
            value = self._config.empty_value
        self._value_widget.setText(str(value))

    def check_value_type(self, value: Any):
        if value == "":
            return
        type_check(value, (int,), allow_none=True)

    def get_value_from_widget(self) -> int:
        self._config: IntLineEditConfig
        value = self._value_widget.text()
        if not value:
            return self._config.empty_value
        try:
            value = int(value)
        except Exception as e:
            raise ValueError(f"not a int: {e}") from e
        else:
            return value
