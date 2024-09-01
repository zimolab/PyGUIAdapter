from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, List, Any, Dict

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


@dataclasses.dataclass(frozen=True)
class ExclusiveChoiceSelectConfig(CommonParameterWidgetConfig):
    default_value: Any | None = None
    choices: Dict[str, Any] | List[Any] = dataclasses.field(default_factory=list)

    @classmethod
    def target_widget_class(cls) -> Type["ExclusiveChoiceSelect"]:
        return ExclusiveChoiceSelect


class ExclusiveChoiceSelect(CommonParameterWidget):

    Self = TypeVar("Self", bound="ExclusiveChoiceSelect")
    ConfigClass = ExclusiveChoiceSelectConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: ExclusiveChoiceSelectConfig,
    ):
        self._config: ExclusiveChoiceSelectConfig = config
        self._value_widget: QComboBox | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QComboBox(self)
            self._add_choices()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        for index in range(self._value_widget.count()):
            if self._value_widget.itemData(index, Qt.UserRole) == value:
                self._value_widget.setCurrentIndex(index)
                break

    def get_value_from_widget(self) -> Any:
        return self._value_widget.currentData(Qt.UserRole)

    def _add_choices(self):
        choices = self._config.choices
        assert isinstance(choices, list) or isinstance(choices, dict)
        if isinstance(choices, list):
            for choice in choices:
                self._value_widget.addItem(str(choice), choice)
            return

        if isinstance(choices, dict):
            for key, value in choices.items():
                self._value_widget.addItem(key, value)
            return
