import dataclasses
from typing import Type, Optional, Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QDial, QLabel, QVBoxLayout

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class DialConfig(CommonParameterWidgetConfig):
    """Dial的配置类。"""

    default_value: Optional[int] = 0
    """控件的默认值"""

    min_value: int = 0
    """最小值"""

    max_value: int = 100
    """最大值"""

    notch_target: Optional[float] = None
    """缺口之间的目标像素数"""

    notches_visible: bool = True
    """是否显示缺口"""

    wrapping: bool = False
    """是否循环"""

    single_step: int = 1
    """单次调整的步长"""

    page_step: Optional[int] = None
    """使用PageUp/PageDown键时调整的步长"""

    tracking: bool = True
    """是否跟踪鼠标"""

    inverted_controls: bool = False
    """是否启用反转控制"""

    inverted_appearance: bool = False
    """是否启用反转外观"""

    show_value_label: bool = True
    """是否显示值标签"""

    prefix: str = ""
    """值标签的前缀"""

    suffix: str = ""
    """值标签的后缀"""

    height: Optional[int] = 120
    """控件的高度"""

    width: Optional[int] = None
    """控件的宽度"""

    @classmethod
    def target_widget_class(cls) -> Type["Dial"]:
        return Dial


class Dial(CommonParameterWidget):
    ConfigClass = DialConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: DialConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._dial: Optional[QDial] = None
        self._label: Optional[QLabel] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: DialConfig
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._dial = QDial(self._value_widget)

            if self._config.height:
                self._value_widget.setFixedHeight(self._config.height)
            if self._config.width:
                self._value_widget.setFixedWidth(self._config.width)

            layout = QVBoxLayout()
            self._value_widget.setLayout(layout)

            layout.addWidget(self._dial, 9)
            if self._config.show_value_label:
                self._label = QLabel(self._value_widget)
                layout.addWidget(self._label, 1)
                # noinspection PyUnresolvedReferences
                self._dial.valueChanged.connect(self._on_value_changed)

            self._dial.setOrientation(Qt.Horizontal)
            self._dial.setMinimum(self._config.min_value)
            self._dial.setMaximum(self._config.max_value)
            self._dial.setSingleStep(self._config.single_step)
            if self._config.page_step is not None:
                self._dial.setPageStep(self._config.page_step)

            self._dial.setTracking(self._config.tracking)
            self._dial.setInvertedControls(self._config.inverted_controls)
            self._dial.setInvertedAppearance(self._config.inverted_appearance)

            if self._config.notch_target is not None:
                self._dial.setNotchTarget(self._config.notch_target)

            self._dial.setNotchesVisible(self._config.notches_visible)
            self._dial.setWrapping(self._config.wrapping)

            if self._label is not None:
                self._label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self._on_value_changed(self._dial.value())
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (int,), allow_none=True)

    def set_value_to_widget(self, value: Any):
        value = int(value)
        self._dial.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._dial.value()

    def _on_value_changed(self, value: int):
        self._config: DialConfig
        if self._label is None:
            return
        self._label.setText(f"{self._config.prefix}{value}{self._config.suffix}")
