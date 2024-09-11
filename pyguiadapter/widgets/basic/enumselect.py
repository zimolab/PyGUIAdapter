from __future__ import annotations

import dataclasses
import inspect
from enum import Enum
from typing import TypeVar, Type

from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...fn import ParameterInfo


@dataclasses.dataclass(frozen=True)
class EnumSelectConfig(CommonParameterWidgetConfig):
    default_value: Enum | None = None
    enum_class: Type[Enum] | None = None

    @classmethod
    def target_widget_class(cls) -> Type["EnumSelect"]:
        return EnumSelect


class EnumSelect(CommonParameterWidget):
    Self = TypeVar("Self", bound="EnumSelect")
    ConfigClass = EnumSelectConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: EnumSelectConfig,
    ):
        self._value_widget: QComboBox | None = None
        self._config: EnumSelectConfig = config
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QComboBox:
        if self._value_widget is None:
            self._value_widget = QComboBox(self)
            all_enums = self._config.enum_class.__members__
            for enum_name, enum_value in all_enums.items():
                self._value_widget.addItem(enum_name, enum_value)
        return self._value_widget

    def set_value_to_widget(self, value: Enum | str):
        if isinstance(value, Enum):
            value = value.name
        self._value_widget.setCurrentText(value)

    def get_value_from_widget(self) -> Enum:
        return self._value_widget.currentData()

    @classmethod
    def on_post_process_config(
        cls,
        config: EnumSelectConfig,
        parameter_name: str,
        parameter_info: ParameterInfo,
    ) -> EnumSelectConfig:
        if inspect.isclass(config.enum_class) and issubclass(config.enum_class, Enum):
            return config
        assert inspect.isclass(parameter_info.type) and issubclass(
            parameter_info.type, Enum
        )
        return dataclasses.replace(config, enum_class=parameter_info.type)

    @classmethod
    def _rule_map_enum_type(
        cls, parameter_info: ParameterInfo
    ) -> Type[EnumSelect] | None:
        param_type = parameter_info.type
        if issubclass(param_type, Enum):
            return cls
        return None
