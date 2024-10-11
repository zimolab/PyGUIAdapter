from abc import abstractmethod
from typing import Dict, Any, List, Tuple, Type, Optional

from qtpy.QtCore import Signal
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget, QToolBox

from ....paramwidget import BaseParameterWidget, BaseParameterWidgetConfig


class BaseParameterPage(QWidget):
    def __init__(self, parent: "BaseParameterGroupBox", group_name: str):
        assert isinstance(parent, BaseParameterGroupBox)
        self._parent: BaseParameterGroupBox = parent
        self._group_name = group_name
        super().__init__(parent)

    def parent(self) -> "BaseParameterGroupBox":
        return super().parent()

    @property
    def group_name(self) -> str:
        return self._group_name

    @abstractmethod
    def scroll_to(self, parameter_name: str, x: int = 50, y: int = 50):
        pass

    @abstractmethod
    def upsert_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
        index: Optional[int] = None,
    ) -> BaseParameterWidget:
        pass

    @abstractmethod
    def insert_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
        index: int = -1,
    ) -> BaseParameterWidget:
        pass

    @abstractmethod
    def update_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
    ) -> BaseParameterWidget:
        pass

    @abstractmethod
    def get_parameter_widget(
        self, parameter_name: str
    ) -> Optional[BaseParameterWidget]:
        pass

    @abstractmethod
    def has_parameter_widget(self, parameter_name: str) -> bool:
        pass

    @abstractmethod
    def remove_parameter_widget(self, parameter_name: str):
        pass

    @abstractmethod
    def clear_parameter_widgets(self):
        pass

    @abstractmethod
    def parameter_count(self) -> int:
        pass

    @abstractmethod
    def get_parameter_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_parameter_value(self, parameter_name: str) -> Any:
        pass

    @abstractmethod
    def set_parameter_value(self, parameter_name: str, value: Any):
        pass

    @abstractmethod
    def get_parameter_values(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def set_parameter_values(self, values: Dict[str, Any]):
        pass

    def disable_parameter_widgets(self, disabled: bool):
        pass

    # noinspection SpellCheckingInspection
    @abstractmethod
    def _add_to_scrollarea(self, widget: BaseParameterWidget, index: int):
        pass


class BaseParameterGroupBox(QToolBox):

    sig_parameter_error = Signal(str, object)
    sig_clear_parameter_error = Signal(object)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    @abstractmethod
    def upsert_parameter_group(self, group_name: Optional[str]) -> BaseParameterPage:
        pass

    @abstractmethod
    def add_default_group(self) -> BaseParameterPage:
        pass

    @abstractmethod
    def has_parameter_group(self, group_name: Optional[str]) -> bool:
        pass

    @abstractmethod
    def _get_parameter_group(
        self, group_name: Optional[str]
    ) -> Optional[BaseParameterPage]:
        pass

    @abstractmethod
    def remove_parameter_group(self, group_name: Optional[str]):
        pass

    @abstractmethod
    def get_parameter_group_names(self) -> List[str]:
        pass

    @abstractmethod
    def _get_parameter_group_of(
        self, parameter_name: str
    ) -> Optional[BaseParameterPage]:
        pass

    @abstractmethod
    def has_parameter(self, parameter_name: str) -> bool:
        pass

    @abstractmethod
    def add_parameter(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
    ) -> BaseParameterWidget:
        pass

    @abstractmethod
    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        pass

    @abstractmethod
    def clear_parameters(self):
        pass

    @abstractmethod
    def get_parameter_value(self, parameter_name: str) -> Any:
        pass

    @abstractmethod
    def get_parameter_values(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_parameter_values_of(self, group_name: Optional[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_parameter_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_parameter_names_of(self, group_name: str) -> List[str]:
        pass

    @abstractmethod
    def set_parameter_value(self, parameter_name: str, value: Any):
        pass

    @abstractmethod
    def set_parameter_values(self, params: Dict[str, Any]):
        pass

    @abstractmethod
    def active_parameter_group(self, group_name: Optional[str]) -> bool:
        pass

    @abstractmethod
    def scroll_to_parameter(self, parameter_name: str, x: int = 50, y: int = 50):
        pass

    def notify_parameter_error(self, parameter_name: str, error: Any):
        # noinspection PyUnresolvedReferences
        self.sig_parameter_error.emit(parameter_name, error)

    def clear_parameter_error(self, parameter_name: Optional[str]):
        # noinspection PyUnresolvedReferences
        self.sig_clear_parameter_error.emit(parameter_name)

    @abstractmethod
    def disable_parameter_widgets(self, disabled: bool):
        pass

    @abstractmethod
    def _get_group_and_widget(
        self, parameter_name: str
    ) -> Tuple[Optional[BaseParameterPage], Optional[BaseParameterWidget]]:
        pass

    @abstractmethod
    def _remove_group(self, group: BaseParameterPage):
        pass

    @abstractmethod
    def _group_name(self, name: Optional[str]) -> str:
        pass

    @abstractmethod
    def _group_icon(self, group_name: Optional[str]) -> QIcon:
        pass


class BaseParameterArea(QWidget):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

    @property
    @abstractmethod
    def parameter_groupbox(self) -> BaseParameterGroupBox:
        pass

    @abstractmethod
    def add_parameter(
        self,
        parameter_name: str,
        config: Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig],
    ) -> BaseParameterWidget:
        pass

    def add_parameters(
        self,
        configs: Dict[str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]],
    ):
        for parameter_name, config in configs.items():
            self.add_parameter(parameter_name, config)

    @abstractmethod
    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        pass

    @abstractmethod
    def clear_parameters(self):
        pass

    @abstractmethod
    def get_parameter_value(self, parameter_name: str) -> Any:
        pass

    @abstractmethod
    def get_parameter_values(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def set_parameter_value(self, parameter_name: str, value: Any):
        pass

    @abstractmethod
    def set_parameter_values(self, params: Dict[str, Any]) -> List[str]:
        pass

    @abstractmethod
    def has_parameter(self, parameter_name):
        pass

    @abstractmethod
    def get_parameter_group_names(self):
        pass

    @abstractmethod
    def get_parameter_names(self):
        pass

    @abstractmethod
    def get_parameter_names_of(self, group_name):
        pass

    @abstractmethod
    def activate_parameter_group(self, group_name):
        pass

    @abstractmethod
    def get_parameter_values_of(self, group_name):
        pass

    @abstractmethod
    def scroll_to_parameter(self, parameter_name: str, x: int = 50, y: int = 50):
        pass

    @abstractmethod
    def clear_parameter_error(self, parameter_name):
        pass

    @abstractmethod
    def process_parameter_error(self, e):
        pass

    @abstractmethod
    def disable_parameter_widgets(self, disabled: bool):
        pass
