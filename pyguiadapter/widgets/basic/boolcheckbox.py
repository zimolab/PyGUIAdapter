from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget, QCheckBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


@dataclasses.dataclass(frozen=True)
class BoolCheckBoxConfig(CommonParameterWidgetConfig):
    default_value: bool | None = False
    checkbox_text: str = "enable {}"

    @classmethod
    def target_widget_class(cls) -> Type["BoolCheckBox"]:
        return BoolCheckBox


class BoolCheckBox(CommonParameterWidget):

    Self = TypeVar("Self", bound="BoolCheckBox")
    ConfigClass = BoolCheckBoxConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BoolCheckBoxConfig,
    ):
        self._value_widget: QCheckBox | None = None
        self._config: BoolCheckBoxConfig = config
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QCheckBox:
        if self._value_widget is None:
            self._value_widget = QCheckBox(self)
            self._value_widget.setText(
                self._config.checkbox_text.format(self.parameter_name)
            )
            self._value_widget.setTristate(False)
        return self._value_widget

    def set_value_to_widget(self, value: bool):
        self._value_widget.setChecked(value is True)

    def get_value_from_widget(self) -> bool:
        return self._value_widget.isChecked()
