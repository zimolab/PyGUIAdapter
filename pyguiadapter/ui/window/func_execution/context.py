import warnings
from typing import Dict, Any, Optional, List, Callable

from PyQt6.QtCore import QObject

from pyguiadapter.ui.utils import (
    get_open_file_path,
    get_open_file_paths,
    get_open_directory_path,
    get_save_file_path,
)
from .base import BaseExecutionWindow
from .constants import ParamInfoType
from .exceptions import NotCallableError, NoSuchParameterError


class ExecutionContext(QObject):
    def __init__(self, parent: BaseExecutionWindow):
        super().__init__(parent)
        self._window = parent

    def get_func(self) -> Callable:
        return self._window.get_func()

    def get_param_value(self, param_name: str) -> Any:
        try:
            value = self._window.get_param_value(param_name)
            return value
        except NoSuchParameterError as e:
            self.show_critical_dialog(str(e))
        except BaseException as e:
            msg = self.tr(f"Error: {e}")
            self._window.show_critical_dialog(msg)

    def get_param_values(self) -> Dict[str, Any]:
        return self._window.get_param_values()

    def get_params_info(self) -> Dict[str, ParamInfoType]:
        return self._window.get_params_info()

    def set_param_value(self, param_name: str, value: Any):
        self._window.set_param_value(param_name, value)

    def set_param_values(
        self, param_values: Dict[str, Any], ignore_exceptions: bool = False
    ):
        self._window.set_param_values(param_values, ignore_exceptions)

    def show_info_dialog(self, message: str, *, title: str = None):
        self._window.show_info_dialog(message, title=title)

    def show_warning_dialog(self, message: str, *, title: str = None):
        self._window.show_warning_dialog(message, title=title)

    def show_critical_dialog(self, message: str, *, title: str = None):
        self._window.show_critical_dialog(message, title=title)

    def show_question_dialog(self, message: str, *, title: str = None) -> bool:
        return self._window.show_question_dialog(message, title=title)

    def clear_output(self):
        self._window.clear_output()

    def get_open_file_path(
        self,
        title: str = None,
        directory: str = None,
        filters: str = None,
        initial_filter: str = None,
    ) -> Optional[str]:
        return get_open_file_path(
            self._window, title, directory, filters, initial_filter
        )

    def get_open_file_paths(
        self,
        title: str = None,
        directory: str = None,
        filters: str = None,
        initial_filter: str = None,
    ) -> Optional[List[str]]:
        return get_open_file_paths(
            self._window, title, directory, filters, initial_filter
        )

    def get_save_file_path(
        self,
        title: Optional[str] = None,
        directory: Optional[str] = None,
        filters: Optional[str] = None,
        initial_filter: Optional[str] = None,
    ) -> Optional[str]:

        return get_save_file_path(
            self._window, title, directory, filters, initial_filter
        )

    def get_open_directory_path(
        self, title: str, directory: str = None
    ) -> Optional[str]:
        return get_open_directory_path(self._window, title, directory)

    def run_on_ui_thread(self, func: Callable, *args, **kwargs):
        if not callable(func):
            raise NotCallableError("func must be callable")
        self._window.run_on_ui_thread_requested.emit(func, args, kwargs)

    def get_window(self) -> BaseExecutionWindow:
        return self._window

    def logging_info(self, message: str):
        self._window.ulogging_info(message)

    def logging_debug(self, message: str):
        self._window.ulogging_debug(message)

    def logging_warning(self, message: str):
        self._window.ulogging_warning(message)

    def logging_critical(self, message: str):
        self._window.ulogging_critical(message)

    def logging_fatal(self, message: str):
        self._window.ulogging_fatal(message)

    def invoke(self, method_name: str, *args, **kwargs) -> Any:
        return self._window.on_context_invoke(method_name, *args, **kwargs)
