from typing import Dict, Any

from .base import BaseExecutionWindow


class ExecutionContext(object):
    def __init__(self, window: BaseExecutionWindow):
        self._window = window

    def get_func(self) -> callable:
        return self._window.get_func()

    def get_param_values(self) -> Dict[str, Any]:
        return self._window.get_param_values()

    def get_params_info(self) -> Dict[str, Any]:
        return self._window.get_params_info()

    def set_param_value(self, param_name: str, value: Any):
        self._window.set_param_value(param_name, value)

    def set_param_values(self, param_values: Dict[str, Any]):
        self._window.set_param_values(param_values)

    def show_info_dialog(self, message: str, *, title: str = None):
        self._window.show_info_dialog(message, title=title)
