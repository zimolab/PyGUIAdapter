from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget, QButtonGroup, QRadioButton, QVBoxLayout, QHBoxLayout

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


@dataclasses.dataclass(frozen=True)
class BoolBoxConfig(CommonParameterWidgetConfig):
    default_value: bool | None = False
    true_text: str = "True"
    false_text: str = "False"
    vertical: bool = True

    @classmethod
    def target_widget_class(cls) -> Type["BoolBox"]:
        return BoolBox


class BoolBox(CommonParameterWidget):

    Self = TypeVar("Self", bound="BoolBox")
    ConfigClass = BoolBoxConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BoolBoxConfig,
    ):
        self._value_widget: QWidget | None = None
        self._true_radio_button: QRadioButton | None = None
        self._false_radio_button: QRadioButton | None = None
        self._button_group: QButtonGroup | None = None

        self._config: BoolBoxConfig = config
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            if self._config.vertical:
                layout = QVBoxLayout()
            else:
                layout = QHBoxLayout()
            self._value_widget.setLayout(layout)

            self._true_radio_button = QRadioButton(
                self._config.true_text, self._value_widget
            )
            self._false_radio_button = QRadioButton(
                self._config.false_text, self._value_widget
            )
            self._button_group = QButtonGroup(self._value_widget)
            self._button_group.addButton(self._true_radio_button)
            self._button_group.addButton(self._false_radio_button)
            self._button_group.setExclusive(True)

            layout.addWidget(self._true_radio_button)
            layout.addWidget(self._false_radio_button)

        return self._value_widget

    def set_value_to_widget(self, value: bool):
        if value:
            self._true_radio_button.setChecked(True)
        else:
            self._false_radio_button.setChecked(True)

    def get_value_from_widget(self) -> bool:
        return self._true_radio_button.isChecked()
