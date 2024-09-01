from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, List

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget, QHBoxLayout, QCheckBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils


@dataclasses.dataclass(frozen=True)
class MultiChoiceBoxConfig(CommonParameterWidgetConfig):
    default_value: List[str] | None = None

    @classmethod
    def target_widget_class(cls) -> Type["MultiChoiceBox"]:
        return MultiChoiceBox


class MultiChoiceBox(CommonParameterWidget):

    Self = TypeVar("Self", bound="MultiChoiceBox")
    ConfigClass = MultiChoiceBoxConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: MultiChoiceBoxConfig,
    ):
        self._value_widget: QWidget | None = None
        self._config: MultiChoiceBoxConfig = config
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            pass
        return self._value_widget

    def set_value_to_widget(self, value: list):
        pass

    def get_value_from_widget(self) -> list:
        pass
