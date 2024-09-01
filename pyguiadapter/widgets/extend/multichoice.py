from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, List, Any, Dict

from qtpy.QtWidgets import QWidget, QGridLayout, QCheckBox, QButtonGroup

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


class _CheckBox(QCheckBox):
    def __init__(self, parent: QWidget | None, user_data: Any):
        super().__init__(parent)
        self._user_data = user_data

    @property
    def user_data(self) -> Any:
        return self._user_data


@dataclasses.dataclass(frozen=True)
class MultiChoiceBoxConfig(CommonParameterWidgetConfig):
    default_value: List[Any] | None = None
    choices: List[Any] | Dict[str, Any] = dataclasses.field(default_factory=list)
    columns: int = 1

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
        self._button_layout: QGridLayout | None = None
        self._button_group: QButtonGroup | None = None
        self._config: MultiChoiceBoxConfig = config
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._button_layout = QGridLayout(self._value_widget)
            self._button_group = QButtonGroup(self._value_widget)
            self._button_group.setExclusive(False)
            self._value_widget.setLayout(self._button_layout)
            self._add_choices()

        return self._value_widget

    def set_value_to_widget(self, value: List[Any]):
        if not isinstance(value, list):
            value = [value]
        for btn in self._button_group.buttons():
            if btn.user_data in value:
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def get_value_from_widget(self) -> List[Any]:
        ret = []
        for btn in self._button_group.buttons():
            if btn.isChecked():
                ret.append(btn.user_data)
        return ret

    def _add_choices(self):
        assert isinstance(self._config.choices, list) or isinstance(
            self._config.choices, dict
        )
        cols = max(self._config.columns, 1)
        if isinstance(self._config.choices, list):
            for idx, choice in enumerate(self._config.choices):
                button = _CheckBox(self, choice)
                button.setText(str(choice))
                self._button_group.addButton(button)
                if idx % cols == 0:
                    self._button_layout.addWidget(button, idx // cols, 0)
                else:
                    self._button_layout.addWidget(button, idx // cols, idx % cols)

        if isinstance(self._config.choices, dict):
            for idx, (key, value) in enumerate(self._config.choices.items()):
                button = _CheckBox(self, value)
                button.setText(key)
                self._button_group.addButton(button)
                if idx % cols == 0:
                    self._button_layout.addWidget(button, idx // cols, 0)
                else:
                    self._button_layout.addWidget(button, idx // cols, idx % cols)
