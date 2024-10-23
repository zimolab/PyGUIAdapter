import dataclasses
import inspect
from enum import Enum

from qtpy.QtCore import QSize
from qtpy.QtWidgets import QWidget, QComboBox
from typing import Type, Tuple, Union, Optional, Dict, Any

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...fn import ParameterInfo
from ...utils import IconType, get_icon, get_size, is_subclass_of, type_check


@dataclasses.dataclass(frozen=True)
class EnumSelectConfig(CommonParameterWidgetConfig):
    """EnumSelect的配置类"""

    default_value: Union[Enum, str, int, None] = 0
    """默认的枚举值，可以为枚举类对象、枚举对象的名称或者是选项的索引"""

    icons: Optional[Dict[Union[Enum, str], IconType]] = None
    """选项的图标，需提供枚举对象（或枚举对象的名称）到图标的映射"""

    icon_size: Union[int, Tuple[int, int], QSize, None] = None
    """选项图标的大小"""

    enum_class: Optional[Type[Enum]] = None

    @classmethod
    def target_widget_class(cls) -> Type["EnumSelect"]:
        return EnumSelect


class EnumSelect(CommonParameterWidget):
    ConfigClass = EnumSelectConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: EnumSelectConfig,
    ):
        self._value_widget: Optional[QComboBox] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QComboBox:
        if self._value_widget is None:
            config: EnumSelectConfig = self.config
            self._value_widget = QComboBox(self)
            icon_size = get_size(config.icon_size)
            if icon_size:
                self._value_widget.setIconSize(icon_size)
            all_enums = config.enum_class.__members__
            for enum_name, enum_value in all_enums.items():
                self._add_item(enum_name, enum_value, config.icons)
        return self._value_widget

    def _add_item(
        self,
        name: str,
        value: Enum,
        icons: Optional[Dict[Union[Enum, str], IconType]],
    ):
        if not icons:
            self._value_widget.addItem(name, value)
            return

        icon = icons.get(name, None)
        if not icon:
            icon = icons.get(value, None)

        if not icon:
            self._value_widget.addItem(name, value)
            return

        icon = get_icon(icon)
        if icon:
            self._value_widget.addItem(icon, name, value)
            return
        self._value_widget.addItem(name, value)

    def check_value_type(self, value: Any):
        self._config: EnumSelectConfig
        type_check(value, (str, int, self._config.enum_class), allow_none=True)

    def set_value_to_widget(self, value: Union[Enum, str, int]):
        if isinstance(value, int):
            if value < 0 or value >= self._value_widget.count():
                raise ValueError(f"invalid index: {value}")
            self._value_widget.setCurrentIndex(value)
            return
        if isinstance(value, Enum):
            self._value_widget.setCurrentText(value.name)
            return
        if isinstance(value, str):
            self._config: EnumSelectConfig
            if value not in self._config.enum_class.__members__:
                raise ValueError(f"invalid enum name: {value}")
            self._value_widget.setCurrentText(value)
            return

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
    ) -> Optional[Type["EnumSelect"]]:
        if is_subclass_of(parameter_info.type, Enum):
            return cls
        return None
