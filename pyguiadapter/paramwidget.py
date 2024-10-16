import dataclasses
from abc import abstractmethod
from inspect import isclass
from typing import Any, Type, TypeVar, Optional

from qtpy.QtWidgets import QWidget

from .fn import ParameterInfo

DEFAULT_VALUE_DESCRIPTION = "use default value: {}"


@dataclasses.dataclass(frozen=True)
class BaseParameterWidgetConfig(object):
    default_value: Any = None
    label: Optional[str] = None
    description: Optional[str] = None
    default_value_description: Optional[str] = DEFAULT_VALUE_DESCRIPTION
    group: Optional[str] = None
    stylesheet: Optional[str] = None

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseParameterWidget"]:
        pass

    @classmethod
    def new(cls, **kwargs) -> "BaseParameterWidgetConfig":
        return cls(**kwargs)


_T = TypeVar("_T", bound=BaseParameterWidgetConfig)


class BaseParameterWidget(QWidget):
    ConfigClass: Type[_T] = NotImplemented

    def __init__(
        self,
        parent: Optional[QWidget],
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
        if self.__default_value_description is None:
            return DEFAULT_VALUE_DESCRIPTION
        return self.__default_value_description

    @default_value_description.setter
    def default_value_description(self, value: str):
        self.__default_value_description = value

    @property
    def config(self) -> _T:
        return self._config

    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def set_value(self, value: Any):
        pass

    @abstractmethod
    def build(self):
        pass

    def on_parameter_error(self, parameter_name: str, error: Any):
        pass

    def on_clear_parameter_error(self, parameter_name: Optional[str]):
        pass

    @classmethod
    def new(
        cls,
        parent: Optional[QWidget],
        parameter_name: str,
        config: BaseParameterWidgetConfig,
    ):
        return cls(parent, parameter_name, config).build()

    # noinspection PyUnusedLocal
    @classmethod
    def on_post_process_config(
        cls,
        config: BaseParameterWidgetConfig,
        parameter_name: str,
        parameter_info: ParameterInfo,
    ) -> BaseParameterWidgetConfig:
        return config


def is_parameter_widget_class(o: Any) -> bool:
    return o is not None and isclass(o) and issubclass(o, BaseParameterWidget)
