import dataclasses
from typing import Type, Optional, Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check

TickPosition = QSlider.TickPosition


@dataclasses.dataclass(frozen=True)
class SliderConfig(CommonParameterWidgetConfig):
    """Slider的配置类"""

    default_value: Optional[int] = 0
    """控件的默认值"""

    min_value: int = 0
    """最小值"""

    max_value: int = 100
    """最大值"""

    single_step: int = 1
    """单次滑动的步长"""

    page_step: Optional[int] = None
    """PageUp/PageDown按键按下时调整的步长"""

    tick_interval: Optional[int] = None
    """刻度间隔"""

    tick_position: TickPosition = TickPosition.TicksBothSides
    """刻度位置"""

    tracking: bool = True
    """是否跟踪鼠标"""

    inverted_controls: bool = False
    """是否启用反转控制"""

    inverted_appearance: bool = False
    """是否显示反转外观"""

    show_value_label: bool = True
    """是否显示值标签"""

    prefix: str = ""
    """值前缀"""

    suffix: str = ""
    """值后缀"""

    @classmethod
    def target_widget_class(cls) -> Type["Slider"]:
        return Slider


class Slider(CommonParameterWidget):
    ConfigClass = SliderConfig

    NoTicks = TickPosition.NoTicks
    """刻度位置：不显示刻度"""

    TickBothSides = TickPosition.TicksBothSides
    """刻度位置：两侧显示刻度"""

    TicksAbove = TickPosition.TicksAbove
    """刻度位置：上方显示刻度"""

    TicksBelow = TickPosition.TicksBelow
    """刻度位置：下方显示刻度"""

    TicksLeft = TickPosition.TicksLeft
    """刻度位置：左侧显示刻度"""

    TicksRight = TickPosition.TicksRight
    """刻度位置：右侧显示刻度"""

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: SliderConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._slider: Optional[QSlider] = None
        self._label: Optional[QLabel] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: SliderConfig
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._slider = QSlider(self._value_widget)

            layout = QVBoxLayout()
            self._value_widget.setLayout(layout)

            layout.addWidget(self._slider)
            if self._config.show_value_label:
                self._label = QLabel(self._value_widget)
                layout.addWidget(self._label)
                # noinspection PyUnresolvedReferences
                self._slider.valueChanged.connect(self._on_value_changed)

            self._slider.setOrientation(Qt.Horizontal)
            self._slider.setMinimum(self._config.min_value)
            self._slider.setMaximum(self._config.max_value)
            self._slider.setSingleStep(self._config.single_step)
            if self._config.page_step is not None:
                self._slider.setPageStep(self._config.page_step)
            if self._config.tick_interval is not None:
                self._slider.setTickInterval(self._config.tick_interval)
            self._slider.setTickPosition(self._config.tick_position)
            self._slider.setTracking(self._config.tracking)
            self._slider.setInvertedControls(self._config.inverted_controls)
            self._slider.setInvertedAppearance(self._config.inverted_appearance)

            if self._label is not None:
                self._label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self._on_value_changed(self._slider.value())
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (int, bool), allow_none=True)

    def set_value_to_widget(self, value: Any):
        try:
            self._slider.setValue(int(value))
        except Exception as e:
            raise ValueError(f"not a int: {type(value)}") from e

    def get_value_from_widget(self) -> int:
        return self._slider.value()

    def _on_value_changed(self, value: int):
        self._config: SliderConfig
        if self._label is None:
            return
        self._label.setText(f"{self._config.prefix}{value}{self._config.suffix}")
