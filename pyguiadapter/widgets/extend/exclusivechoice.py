from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, List, Any

import qtawesome
from qtpy.QtWidgets import QWidget, QGridLayout, QRadioButton, QButtonGroup

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils
from ...fn import ParameterInfo


class _ChoiceButton(QRadioButton):
    def __init__(self, parent: QWidget | None, user_data: Any):
        super().__init__(parent)
        self._user_data = user_data

    @property
    def user_data(self) -> Any:
        return self._user_data


@dataclasses.dataclass(frozen=True)
class ExclusiveChoiceBoxConfig(CommonParameterWidgetConfig):
    default_value: str | int | bool | None = None
    choices: List[str | int | bool] = dataclasses.field(default_factory=list)
    columns: int = 1
    show_type_icon: bool = True

    @classmethod
    def target_widget_class(cls) -> Type["ExclusiveChoiceBox"]:
        return ExclusiveChoiceBox


class ExclusiveChoiceBox(CommonParameterWidget):

    Self = TypeVar("Self", bound="ExclusiveChoiceBox")
    ConfigClass = ExclusiveChoiceBoxConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: ExclusiveChoiceBoxConfig,
    ):
        self._config: ExclusiveChoiceBoxConfig = config
        self._value_widget: QWidget | None = None
        self._button_group: QButtonGroup | None = None
        self._button_layout: QGridLayout | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._button_layout = QGridLayout()
            self._value_widget.setLayout(self._button_layout)
            self._button_group = QButtonGroup(self._value_widget)
            self._button_group.setExclusive(True)
            self._add_choices()
        return self._value_widget

    def set_value_to_widget(self, value: int | str | bool):
        for btn in self._button_group.buttons():
            assert isinstance(btn, _ChoiceButton)
            if btn.user_data == value:
                btn.setChecked(True)
                break

    def get_value_from_widget(self) -> int | str | bool | None:
        for btn in self._button_group.buttons():
            assert isinstance(btn, _ChoiceButton)
            if btn.isChecked():
                return btn.user_data
        return None

    def _add_choices(self):
        choices = utils.unique_list(self._config.choices)
        str_icon = qtawesome.icon("mdi6.code-string")
        int_icon = qtawesome.icon("msc.symbol-string")
        bool_icon = qtawesome.icon("ri.checkbox-multiple-line")
        cols = max(self._config.columns, 1)
        for idx, choice in enumerate(choices):
            btn = _ChoiceButton(self._value_widget, choice)
            btn.setText(str(choice))
            if self._config.show_type_icon:
                if isinstance(choice, str):
                    btn.setIcon(str_icon)
                elif isinstance(choice, bool):
                    btn.setIcon(bool_icon)
                else:
                    btn.setIcon(int_icon)
            self._button_group.addButton(btn)
            if idx % cols == 0:
                self._button_layout.addWidget(btn, idx // cols, 0)
            else:
                self._button_layout.addWidget(btn, idx // cols, idx % cols)

    @classmethod
    def after_process_config(
        cls,
        config: ExclusiveChoiceBoxConfig,
        parameter_name: str,
        parameter_info: ParameterInfo,
    ) -> ExclusiveChoiceBoxConfig:
        if not config.choices and len(parameter_info.type_args) > 0:
            config = dataclasses.replace(
                config, choices=parameter_info.type_args.copy()
            )
        return config
