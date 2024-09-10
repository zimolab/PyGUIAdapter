from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QDial, QLabel, QVBoxLayout

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


@dataclasses.dataclass(frozen=True)
class DialConfig(CommonParameterWidgetConfig):
    default_value: int | None = None
    min_value: int = 0
    max_value: int = 100
    notch_target: float | None = None
    notches_visible: bool = True
    wrapping: bool = False
    single_step: int = 1
    page_step: int | None = None
    tracking: bool = True
    inverted_controls: bool = False
    inverted_appearance: bool = False
    enable_value_label: bool = True
    prefix: str = ""
    suffix: str = ""
    min_height: int = 120

    @classmethod
    def target_widget_class(cls) -> Type["Dial"]:
        return Dial


class Dial(CommonParameterWidget):
    Self = TypeVar("Self", bound="Dial")
    ConfigClass = DialConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: DialConfig,
    ):
        self._config: DialConfig = config
        self._value_widget: QWidget | None = None
        self._dial: QDial | None = None
        self._label: QLabel | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._dial = QDial(self._value_widget)
            if self._config.min_height:
                self._value_widget.setMinimumHeight(self._config.min_height)

            layout = QVBoxLayout()
            self._value_widget.setLayout(layout)

            layout.addWidget(self._dial, 9)
            if self._config.enable_value_label:
                self._label = QLabel(self._value_widget)
                layout.addWidget(self._label, 1)
                self._dial.valueChanged.connect(self._on_value_changed)

            self._setup_widgets()

        return self._value_widget

    def set_value_to_widget(self, value: int):
        value = int(value)
        self._dial.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._dial.value()

    def _setup_widgets(self):
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

    def _on_value_changed(self, value: int):
        if self._label is None:
            return
        self._label.setText(f"{self._config.prefix}{value}{self._config.suffix}")
