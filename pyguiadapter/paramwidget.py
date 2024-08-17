from __future__ import annotations

import dataclasses
from abc import abstractmethod
from inspect import isclass
from typing import Any, Type, TypeVar

from qtpy.QtWidgets import QWidget


DEFAULT_VALUE_DESCRIPTION = "Use default value({})"


@dataclasses.dataclass(frozen=True)
class BaseParameterWidgetConfig(object):
    default_value: Any
    label: str | None = None
    description: str | None = None
    default_value_description: str | None = DEFAULT_VALUE_DESCRIPTION
    stylesheet: str | None = None

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type[BaseParameterWidget]:
        pass

    @classmethod
    def new(cls, **kwargs) -> BaseParameterWidgetConfig:
        return cls(**kwargs)


class BaseParameterWidget(QWidget):
    Self = TypeVar("Self", bound="BaseParameterWidget")
    ConfigClass: Type[BaseParameterWidgetConfig]

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BaseParameterWidgetConfig,
    ):
        super().__init__(parent)
        self._config = config

        self.__parameter_name = parameter_name
        self.__default_value = self._config.default_value
        self.__label = self._config.label
        self.__description = self._config.description
        self.__default_value_description = self._config.default_value_description

        if self._config.stylesheet:
            self.setStyleSheet(self._config.stylesheet)

    @property
    def parameter_name(self) -> str:
        return self.__parameter_name

    @property
    def default_value(self) -> Any:
        return self.__default_value

    @property
    def label(self) -> str:
        if not self.__label:
            return self.parameter_name
        return self.__label

    @label.setter
    def label(self, value: str):
        self.__label = value

    @property
    def description(self) -> str:
        return self.__description or ""

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def default_value_description(self) -> str:
        return self.__default_value_description or ""

    @default_value_description.setter
    def default_value_description(self, value: str):
        self.__default_value_description = value

    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def set_value(self, value: Any):
        pass

    @abstractmethod
    def build(self):
        pass

    @classmethod
    def new(cls, parent: QWidget | None, config: BaseParameterWidgetConfig) -> Self:
        return cls(parent, config).build()


def is_parameter_widget_class(o: Any) -> bool:
    return isclass(o) and issubclass(o, BaseParameterWidget)
