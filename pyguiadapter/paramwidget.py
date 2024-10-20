"""
@Time    : 2024.10.20
@File    : paramwidget.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了参数控件基类和配置基类。
"""

import dataclasses
from abc import abstractmethod
from inspect import isclass
from typing import Any, Type, TypeVar, Optional

from qtpy.QtWidgets import QWidget

from .fn import ParameterInfo

DEFAULT_VALUE_DESCRIPTION = "use default value: {}"


@dataclasses.dataclass(frozen=True)
class BaseParameterWidgetConfig(object):
    """
    参数控件配置基类。提供了所有参数控件共有的可配置属性。
    """

    default_value: Any = None
    """控件的默认值。"""

    label: Optional[str] = None
    """控件的标签。若不指定此属性，则使用参数名作为标签。"""

    description: Optional[str] = None
    """控件的描述文本。若不指定此属性，则从尝试从函数的docstring中获取对应参数的描述文本。"""

    default_value_description: Optional[str] = DEFAULT_VALUE_DESCRIPTION
    """使用默认值复选框的描述文本。当default_value为None或开发者明确指定显示默认值复选框时，默认值复选框才会显示。"""

    group: Optional[str] = None
    """参数分组名称。为None时，参见将被添加到默认分组。"""

    stylesheet: Optional[str] = None
    """参数控件的样式表。"""

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseParameterWidget"]:
        """
        目标控件类，即本配置类适用的参数控件类。子类必须实现此方法。

        Returns:
            目标控件类
        """
        pass

    @classmethod
    def new(cls, **kwargs) -> "BaseParameterWidgetConfig":
        return cls(**kwargs)


_T = TypeVar("_T", bound=BaseParameterWidgetConfig)


class BaseParameterWidget(QWidget):
    """
    参数控件基类。定义了所有参数控件共有的接口。
    """

    ConfigClass: Type[_T] = NotImplemented
    """参数控件对应的配置类。必须为BaseParameterWidgetConfig的子类。必须在子类中实现。"""

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: BaseParameterWidgetConfig,
    ):
        """
        构造函数。

        Args:
            parent: 父控件
            parameter_name: 参数名
            config: 参数控件配置
        """
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
        """
        从控件获取参数值。子类必须实现此方法。

        Returns:
            参数值
        """
        pass

    @abstractmethod
    def set_value(self, value: Any) -> None:
        """
        设置参数值。子类必须实现此方法。

        Args:
            value: 参数值

        Returns:
            无返回值
        """
        pass

    @abstractmethod
    def build(self) -> "BaseParameterWidget":
        """
        构建参数控件。子类必须实现此方法。

        Returns:
            参数控件实例
        """
        pass

    def on_parameter_error(self, parameter_name: str, error: Any) -> None:
        """
        参数错误时回调。子类可重写此方法。

        Args:
            parameter_name: 参数名
            error: 错误信息

        Returns:
            无返回值
        """
        pass

    def on_clear_parameter_error(self, parameter_name: Optional[str]) -> None:
        """
        清除参数错误时回调。子类可重写此方法。

        Args:
            parameter_name: 参数名，若为None，表示清除所有参数错误。

        Returns:
            无返回值
        """
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
