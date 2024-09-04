from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout

from ..common import CommonParameterWidgetConfig, CommonParameterWidget

TickPosition = QSlider.TickPosition


@dataclasses.dataclass(frozen=True)
class SliderConfig(CommonParameterWidgetConfig):
    default_value: int | None = None
    min_value: int = 0
    max_value: int = 100
    single_step: int = 1
    page_step: int | None = None
    tick_interval: int | None = None
    tick_position: TickPosition = TickPosition.TicksBothSides
    tracking: bool = True
    inverted_controls: bool = False
    inverted_appearance: bool = False
    enable_value_label: bool = True
    prefix: str = ""
    suffix: str = ""

    @classmethod
    def target_widget_class(cls) -> Type["Slider"]:
        return Slider


class Slider(CommonParameterWidget):
    Self = TypeVar("Self", bound="Slider")
    ConfigClass = SliderConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: SliderConfig,
    ):
        self._config: SliderConfig = config
        self._value_widget: QWidget | None = None
        self._slider: QSlider | None = None
        self._label: QLabel | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._slider = QSlider(self._value_widget)

            layout = QVBoxLayout(self._value_widget)
            self._value_widget.setLayout(layout)

            layout.addWidget(self._slider)
            if self._config.enable_value_label:
                self._label = QLabel(self._value_widget)
                layout.addWidget(self._label)
                self._slider.valueChanged.connect(self._on_value_changed)

            self._setup_widgets()

        return self._value_widget

    def set_value_to_widget(self, value: int):
        value = int(value)
        self._slider.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._slider.value()

    def _setup_widgets(self):
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

    def _on_value_changed(self, value: int):
        if self._label is None:
            return
        self._label.setText(f"{self._config.prefix}{value}{self._config.suffix}")