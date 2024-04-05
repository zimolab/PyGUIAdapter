import warnings
from typing import Dict, Any, Optional, List, Callable

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QDialog, QMessageBox

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
        try:
            self._window.set_param_value(param_name, value)
        except NoSuchParameterError:
            warnings.warn(f"No such parameter: {param_name}")
        except BaseException as e:
            msg = self.tr(f"Error: {e}")
            self._window.show_critical_dialog(msg)

    def set_param_values(
        self, param_values: Dict[str, Any], ignore_exceptions: bool = False
    ):
        try:
            self._window.set_param_values(param_values, ignore_exceptions)
        except BaseException as e:
            self._window.show_critical_dialog(str(e))

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
