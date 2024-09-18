from __future__ import annotations

import dataclasses
import inspect
from enum import Enum
from typing import Type, Tuple

from qtpy.QtCore import QSize
from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...fn import ParameterInfo
from ... import utils


@dataclasses.dataclass(frozen=True)
class EnumSelectConfig(CommonParameterWidgetConfig):
    default_value: Enum | str | int | None = 0
    enum_class: Type[Enum] | None = None
    icons: dict[Enum | str, utils.IconType] | None = None
    icon_size: Tuple[int, int] | QSize | None = None

    @classmethod
    def target_widget_class(cls) -> Type["EnumSelect"]:
        return EnumSelect


class EnumSelect(CommonParameterWidget):
    ConfigClass = EnumSelectConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: EnumSelectConfig,
    ):
        self._value_widget: QComboBox | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QComboBox:
        if self._value_widget is None:
            config: EnumSelectConfig = self.config
            self._value_widget = QComboBox(self)
            if config.icon_size:
                icon_size = config.icon_size
                if isinstance(icon_size, Tuple):
                    assert len(icon_size) == 2
                    icon_size = QSize(config.icon_size[0], config.icon_size[1])
                self._value_widget.setIconSize(icon_size)
            all_enums = config.enum_class.__members__
            for enum_name, enum_value in all_enums.items():
                self._add_item(enum_name, enum_value, config.icons)
        return self._value_widget

    def _add_item(
        self, name: str, value: Enum, icons: dict[Enum | str, utils.IconType] | None
    ):
        if not icons:
            self._value_widget.addItem(name, value)
            return

        icon = icons.get(name, None)
        if not icon:
            self._value_widget.addItem(name, value)
            return

        icon = utils.get_icon(icon)
        if not icon:
            self._value_widget.addItem(name, value)
            return

        self._value_widget.addItem(icon, name, value)

    def set_value_to_widget(self, value: Enum | str | int):
        if isinstance(value, int):
            self._value_widget.setCurrentIndex(value)
            return
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
    def _enum_type_mapping_rule(
        cls, parameter_info: ParameterInfo
    ) -> Type[EnumSelect] | None:
        if utils.is_subclass_of(parameter_info.type, Enum):
            return cls
        return None
