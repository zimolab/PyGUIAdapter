from typing import Optional, Any, Union, Sequence, Tuple, Type
import dataclasses

from qtpy.QtWidgets import QDoubleSpinBox, QSpinBox, QComboBox, QWidget, QHBoxLayout

from ...widgets.common import CommonParameterWidget, CommonParameterWidgetConfig

QuantityType = Tuple[Union[int, float], Optional[str]]


@dataclasses.dataclass(frozen=True)
class QuantityBoxConfig(CommonParameterWidgetConfig):
    # (quantity, unit)
    default_value: Optional[QuantityType] = (0, None)
    """默认值。格式为 `(quantity, unit)`。quantity代表数量，可以为 int 或 float。unit代表单位，可以为 None 或 str，如果为 None，则表示使用默认单位，即units中的第一个元素。"""

    quantity_type: Union[Type[int], Type[float]] = float
    """quantity的类型，可以为 int 或 float。"""

    units: Sequence[str] = ()
    """可选的单位列表。"""

    max_value: Union[int, float, None] = None
    """quantity的最大值。"""

    min_value: Union[int, float, None] = None
    """quantity的最小值。"""

    decimals: Optional[int] = 2
    """quantity的小数位数。仅在 quantity_type 为 float 时有效。"""

    step: Union[int, float, None] = None
    """单次调整的步长。"""

    @classmethod
    def target_widget_class(cls) -> Type["QuantityBox"]:
        return QuantityBox


class _QuantityWidget(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget],
        config: QuantityBoxConfig,
    ):
        super().__init__(parent)

        if not config.units:
            raise RuntimeError("units cannot be empty")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self._quantity_spin: Union[QDoubleSpinBox, QSpinBox]
        if config.quantity_type == int:
            self._quantity_spin = QSpinBox(self)
            self._setup_int_quantity(config)
        else:
            self._quantity_spin = QDoubleSpinBox(self)
            self._setup_float_quantity(config)
        layout.addWidget(self._quantity_spin, 9)

        self._unit_combo = QComboBox(self)
        for unit in config.units:
            self._unit_combo.addItem(unit)
        layout.addWidget(self._unit_combo, 1)

        initial_quantity, initial_unit = config.default_value
        if initial_unit is None:
            initial_unit = config.units[0]

        self._config = config

        self.set_quantity((initial_quantity, initial_unit))

    def get_quantity(self) -> QuantityType:
        return (
            self._config.quantity_type(self._quantity_spin.value()),
            self._unit_combo.currentText(),
        )

    def set_quantity(self, quantity: QuantityType) -> None:
        quantity_value, unit_text = quantity
        quantity_value = self._config.quantity_type(quantity_value)
        self._quantity_spin.setValue(quantity_value)
        if not unit_text:
            return
        self._unit_combo.setCurrentText(unit_text)

    def _setup_int_quantity(self, config: QuantityBoxConfig):
        spin_box: QSpinBox = self._quantity_spin

        if config.max_value is not None:
            spin_box.setMaximum(int(config.max_value))

        if config.min_value is not None:
            spin_box.setMinimum(int(config.min_value))

        if config.step is not None:
            spin_box.setSingleStep(int(config.step))

    def _setup_float_quantity(self, config: QuantityBoxConfig):
        double_spin_box: QDoubleSpinBox = self._quantity_spin
        if config.max_value is not None:
            double_spin_box.setMaximum(config.max_value)
        if config.min_value is not None:
            double_spin_box.setMinimum(config.min_value)
        if config.decimals is not None:
            double_spin_box.setDecimals(config.decimals)
        if config.step is not None:
            double_spin_box.setSingleStep(config.step)


class QuantityBox(CommonParameterWidget):

    ConfigClass = QuantityBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: QuantityBoxConfig,
    ):
        self._value_widget: Optional[_QuantityWidget] = None

        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: QuantityBoxConfig
        if self._value_widget is None:
            self._value_widget = _QuantityWidget(self, self._config)
        return self._value_widget

    def check_value_type(self, value: Any):
        self._config: QuantityBoxConfig
        if (
            not isinstance(value, tuple)
            or len(value) != 2
            or not isinstance(value[0], self._config.quantity_type)
            or not isinstance(value[1], (type(None), str))
        ):
            raise TypeError(
                f"value should be a tuple of ({self._config.quantity_type.__name__}, str | None), but got {value}"
            )

    def set_value_to_widget(self, value: QuantityType) -> None:
        self._value_widget.set_quantity(value)

    def get_value_from_widget(self) -> QuantityType:
        return self._value_widget.get_quantity()


IntQuantityType = Tuple[int, Optional[str]]


@dataclasses.dataclass(frozen=True)
class IntQuantityBoxConfig(QuantityBoxConfig):
    """IntQuantityBox的配置类。"""

    # (quantity, unit)
    default_value: Optional[IntQuantityType] = (0, None)
    """默认值。格式为 `(quantity, unit)`。quantity代表数量。unit代表单位，可以为 None 或 str，如果为 None，则表示使用默认单位，即units中的第一个元素。"""

    quantity_type = int

    units: Sequence[str] = ()
    """可选的单位列表。"""

    max_value: Optional[int] = 2147483647
    """quantity的最大值。"""

    min_value: Optional[int] = -2147483648
    """quantity的最小值。"""

    decimals: Optional[int] = None

    step: Optional[int] = 1
    """单次调整的步长。"""

    @classmethod
    def target_widget_class(cls) -> Type["IntQuantityBox"]:
        return IntQuantityBox


class IntQuantityBox(QuantityBox):
    ConfigClass = IntQuantityBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: IntQuantityBoxConfig,
    ):
        config = dataclasses.replace(config, quantity_type=int)
        super().__init__(parent, parameter_name, config)


FloatQuantityType = Tuple[float, Optional[str]]


@dataclasses.dataclass(frozen=True)
class FloatQuantityBoxConfig(QuantityBoxConfig):
    """FloatQuantityBox的配置类。"""

    # (quantity, unit)
    default_value: Optional[FloatQuantityType] = (0.0, None)
    """默认值。格式为 `(quantity, unit)`。quantity代表数量。unit代表单位，可以为 None 或 str，如果为 None，则表示使用默认单位，即units中的第一个元素。"""

    quantity_type = float

    units: Sequence[str] = ()
    """可选的单位列表。"""

    max_value: Optional[float] = 2147483647.0
    """quantity的最大值。"""

    min_value: Optional[float] = -2147483648.0
    """quantity的最小值。"""

    decimals: Optional[int] = 2
    """quantity的小数位数。"""

    step: Optional[float] = 0.01
    """单次调整的步长。"""

    @classmethod
    def target_widget_class(cls) -> Type["FloatQuantityBox"]:
        return FloatQuantityBox


class FloatQuantityBox(QuantityBox):
    ConfigClass = FloatQuantityBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: FloatQuantityBoxConfig,
    ):
        config = dataclasses.replace(config, quantity_type=float)
        super().__init__(parent, parameter_name, config)
