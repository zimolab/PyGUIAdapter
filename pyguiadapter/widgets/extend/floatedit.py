import dataclasses
from typing import Type, Any, Optional

from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QWidget, QLineEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...exceptions import ParameterError
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class FloatLineEditConfig(CommonParameterWidgetConfig):
    """FloatLineEdit的配置类。"""

    default_value: Optional[float] = 0.0
    """控件的默认值"""

    min_value: float = -2147483648.0
    """最小值"""

    max_value: float = 2147483647.0
    """最大值"""

    decimals: int = 2
    """小数点后位数"""

    scientific_notation: bool = False
    """是否使用科学计数法"""

    placeholder: str = ""
    """占位符文本"""

    clear_button: bool = False
    """是否显示清除按钮"""

    empty_value: Optional[float] = 0.0
    """输入框为空时的默认值，若设置为None则表示不允许输入空值，用户输入空值，获取和设置值时会抛出ParameterError"""

    @classmethod
    def target_widget_class(cls) -> Type["FloatLineEdit"]:
        return FloatLineEdit


class FloatLineEdit(CommonParameterWidget):
    ConfigClass = FloatLineEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: FloatLineEditConfig,
    ):
        self._value_widget: Optional[QLineEdit] = None
        self._validator: Optional[QDoubleValidator] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            config: FloatLineEditConfig = self.config
            self._value_widget = QLineEdit(self)
            if config.placeholder:
                self._value_widget.setPlaceholderText(config.placeholder)
            if config.clear_button:
                self._value_widget.setClearButtonEnabled(True)
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

    def check_value_type(self, value: Any):
        if value == "":
            return
        type_check(value, (float, int), allow_none=True)

    def set_value_to_widget(self, value: Any):
        self._config: FloatLineEditConfig
        if value == "":
            if self._config.empty_value is None:
                raise ParameterError(
                    parameter_name=self.parameter_name,
                    message="empty value is not allowed",
                )
            value = self._config.empty_value
        self._value_widget.setText(str(value))

    def get_value_from_widget(self) -> float:
        self._config: FloatLineEditConfig
        value = self._value_widget.text().strip()
        if value == "":
            if self._config.empty_value is None:
                raise ParameterError(
                    parameter_name=self.parameter_name,
                    message="empty value is not allowed",
                )
            return self._config.empty_value
        try:
            value = float(value)
        except Exception as e:
            raise ValueError(f"not a float: {e}") from e
        else:
            return value
