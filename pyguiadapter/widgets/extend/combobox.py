from __future__ import annotations

import dataclasses
from typing import Type, List, Any, Dict

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget

_FIRST_ITEM = object()


@dataclasses.dataclass
class _DataWrap(object):
    value: Any


@dataclasses.dataclass(frozen=True)
class ComboBoxConfig(CommonParameterWidgetConfig):
    default_value: Any | None = _FIRST_ITEM
    choices: Dict[str, Any] | List[Any] = dataclasses.field(default_factory=list)
    editable: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["ComboBox"]:
        return ComboBox


class ComboBox(CommonParameterWidget):
    ConfigClass = ComboBoxConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: ComboBoxConfig,
    ):
        self._value_widget: QComboBox | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: ComboBoxConfig
        if self._value_widget is None:
            self._value_widget = QComboBox(self)
            if self._config.editable:
                self._value_widget.setEditable(True)
            self._add_choices()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        if value is _FIRST_ITEM:
            self._value_widget.setCurrentIndex(0)
            return
        for index in range(self._value_widget.count()):
            data = self._value_widget.itemData(index, Qt.UserRole)
            if isinstance(data, _DataWrap):
                data = data.value
            if data == value:
                self._value_widget.setCurrentIndex(index)
                break

    def get_value_from_widget(self) -> Any:
        data = self._value_widget.currentData(Qt.UserRole)
        if isinstance(data, _DataWrap):
            return data.value
        if data is not None:
            return data
        return self._value_widget.currentText()

    def _add_choices(self):
        self._config: ComboBoxConfig
        choices = self._config.choices
        assert isinstance(choices, list) or isinstance(choices, dict)
        if isinstance(choices, list):
            for choice in choices:
                self._value_widget.addItem(str(choice), _DataWrap(choice))
            return

        if isinstance(choices, dict):
            for key, value in choices.items():
                self._value_widget.addItem(key, _DataWrap(value))
            return
