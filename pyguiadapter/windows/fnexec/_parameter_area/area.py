import dataclasses
import traceback
from typing import Optional, Any, Dict, List, Tuple, Type

from qtpy.QtWidgets import QWidget, QVBoxLayout

from .base import BaseParameterArea, BaseParameterGroupBox
from .group import ParameterGroupBox
from .._base import FnExecuteWindowConfig
from ....bundle import FnBundle
from ....exceptions import ParameterError
from ....fn import ParameterInfo
from ....paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    is_parameter_widget_class,
)
from ....utils import messagebox
from ....widgets import CommonParameterWidgetConfig


class ParameterArea(BaseParameterArea):
    def __init__(
        self, parent: QWidget, config: FnExecuteWindowConfig, bundle: FnBundle
    ):
        super().__init__(parent)
        self._config: FnExecuteWindowConfig = config
        self._bundle: FnBundle = bundle
        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self._groupbox: Optional[BaseParameterGroupBox] = ParameterGroupBox(
            self, self._config
        )
        self._groupbox.add_default_group()
        self._layout.addWidget(self._groupbox)
        self.setLayout(self._layout)

    @property
    def parameter_groupbox(self) -> BaseParameterGroupBox:
        return self._groupbox

    def add_parameter(
        self,
        parameter_name: str,
        config: Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig],
    ) -> BaseParameterWidget:
        if parameter_name.strip() == "":
            raise ValueError("parameter name cannot be empty.")
        param_info = self._bundle.fn_info.parameters.get(parameter_name)
        widget_class, widget_config = self._process_config(
            parameter_name, param_info, config
        )

        try:
            widget = self._groupbox.add_parameter(
                parameter_name, widget_class, widget_config
            )
            if isinstance(widget_config, CommonParameterWidgetConfig):
                # apply set_default_value_on_init
                # set_value() may raise exceptions, we need to catch ParameterValidationError of them
                # typically, this kind of exception is not fatal, it unnecessary to exit the whole program
                # when this kind of exception raised
                if widget_config.set_default_value_on_init:
                    widget.set_value(widget_config.default_value)
        except ParameterError as e:
            # self.process_parameter_error(e)
            # return None
            raise e
        except Exception as e:
            # any other exceptions are seen as fatal and will cause the whole program to exit
            traceback.print_exc()
            messagebox.show_exception_messagebox(
                self,
                message=f"cannot create parameter widget for parameter '{parameter_name}':",
                exception=e,
                title=self._config.error_dialog_title,
            )
            exit(-1)
        else:
            return widget

    def remove_parameter(
        self, parameter_name: str, ignore_unknown_parameter: bool = True
    ):
        self._groupbox.remove_parameter(
            parameter_name, ignore_unknown_parameter=ignore_unknown_parameter
        )

    def clear_parameters(self):
        self._groupbox.clear_parameters()
        self._groupbox.add_default_group()

    def has_parameter(self, parameter_name: str) -> bool:
        return self._groupbox.has_parameter(parameter_name)

    def get_parameter_group_names(self) -> List[str]:
        return self._groupbox.get_parameter_group_names()

    def get_parameter_names(self) -> List[str]:
        return self._groupbox.get_parameter_names()

    def get_parameter_names_of(self, group_name: str) -> List[str]:
        return self._groupbox.get_parameter_names_of(group_name)

    def activate_parameter_group(self, group_name: Optional[str]) -> bool:
        return self._groupbox.active_parameter_group(group_name)

    def scroll_to_parameter(
        self,
        parameter_name: str,
        x: int = 50,
        y: int = 50,
        highlight_effect: bool = False,
    ):
        self._groupbox.scroll_to_parameter(parameter_name, x, y, highlight_effect)

    def get_parameter_value(self, parameter_name: str) -> Any:
        return self._groupbox.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        return self._groupbox.get_parameter_values()

    def set_parameter_value(self, parameter_name: str, value: Any):
        self._groupbox.set_parameter_value(parameter_name=parameter_name, value=value)

    def clear_parameter_error(self, parameter_name: Optional[str]):
        self._groupbox.clear_parameter_error(parameter_name)

    def set_parameter_values(self, params: Dict[str, Any]) -> List[str]:
        return self._groupbox.set_parameter_values(params)

    def get_parameter_values_of(self, group_name: Optional[str]) -> Dict[str, Any]:
        return self._groupbox.get_parameter_values_of(group_name)

    def process_parameter_error(self, e: ParameterError):
        self._groupbox.notify_parameter_error(e.parameter_name, e.message)
        msg = self._config.parameter_error_message.format(e.parameter_name, e.message)
        messagebox.show_critical_message(
            self, message=msg, title=self._config.error_dialog_title
        )
        self._groupbox.scroll_to_parameter(e.parameter_name)
        del e

    def disable_parameter_widgets(self, disabled: bool):
        self._groupbox.disable_parameter_widgets(disabled)

    @staticmethod
    def _process_config(
        param_name: str,
        param_info: ParameterInfo,
        config: Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig],
    ) -> Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]:
        assert isinstance(config, tuple) and len(config) == 2
        assert is_parameter_widget_class(config[0])
        assert isinstance(config[1], BaseParameterWidgetConfig)
        widget_class, widget_config = config
        # try to get description from parameter info if it is empty in widget_config
        if widget_config.description is None or widget_config.description == "":
            if param_info.description is not None and param_info.description != "":
                widget_config = dataclasses.replace(
                    widget_config, description=param_info.description
                )
        widget_config = widget_class.on_post_process_config(
            widget_config, param_name, param_info
        )
        return widget_class, widget_config
