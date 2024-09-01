from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils


@dataclasses.dataclass(frozen=True)
class BinStateSelectConfig(CommonParameterWidgetConfig):
    default_value: int | None = None

    state_on_text: str = "On"
    state_on_value: int = 1
    state_on_icon: utils.IconType = None
    state_off_text: str = "Off"
    state_off_value: int = 0
    state_off_icon: utils.IconType = None

    @classmethod
    def target_widget_class(cls) -> Type["BinStateSelect"]:
        return BinStateSelect


class BinStateSelect(CommonParameterWidget):

    Self = TypeVar("Self", bound="BinStateSelect")
    ConfigClass = BinStateSelectConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BinStateSelectConfig,
    ):
        self._value_widget: QComboBox | None = None
        self._config: BinStateSelectConfig = config
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QComboBox:
        if self._value_widget is None:
            self._value_widget = QComboBox(self)
            state_on_icon = utils.get_icon(self._config.state_on_icon) or QIcon()
            self._value_widget.addItem(
                state_on_icon, self._config.state_on_text, self._config.state_on_value
            )
            state_off_icon = utils.get_icon(self._config.state_off_icon) or QIcon()
            self._value_widget.addItem(
                state_off_icon,
                self._config.state_off_text,
                self._config.state_off_value,
            )
            self._value_widget.setEditable(False)

        return self._value_widget

    def set_value_to_widget(self, value: int):
        if value == self._config.state_on_value:
            self._value_widget.setCurrentText(self._config.state_on_text)
        else:
            self._value_widget.setCurrentText(self._config.state_off_text)

    def get_value_from_widget(self) -> int:
        current_data = self._value_widget.currentData(Qt.UserRole)
        if current_data == self._config.state_on_value:
            return self._config.state_on_value
        return self._config.state_off_value
