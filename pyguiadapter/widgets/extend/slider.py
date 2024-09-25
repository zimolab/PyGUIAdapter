import dataclasses
from typing import Type, Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout

from ..common import CommonParameterWidgetConfig, CommonParameterWidget

TickPosition = QSlider.TickPosition


@dataclasses.dataclass(frozen=True)
class SliderConfig(CommonParameterWidgetConfig):
    default_value: Optional[int] = 0
    min_value: int = 0
    max_value: int = 100
    single_step: int = 1
    page_step: Optional[int] = None
    tick_interval: Optional[int] = None
    tick_position: TickPosition = TickPosition.TicksBothSides
    tracking: bool = True
    inverted_controls: bool = False
    inverted_appearance: bool = False
    show_value_label: bool = True
    prefix: str = ""
    suffix: str = ""

    @classmethod
    def target_widget_class(cls) -> Type["Slider"]:
        return Slider


class Slider(CommonParameterWidget):
    ConfigClass = SliderConfig

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

    def set_value_to_widget(self, value: int):
        value = int(value)
        self._slider.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._slider.value()

    def _on_value_changed(self, value: int):
        self._config: SliderConfig
        if self._label is None:
            return
        self._label.setText(f"{self._config.prefix}{value}{self._config.suffix}")
