import dataclasses
from abc import abstractmethod
from typing import Tuple, Dict, Union, Type, Optional, Literal

from qtpy.QtCore import QSize, Qt

from ._output_area import OutputBrowserConfig
from ..document_browser import DocumentBrowserConfig
from ...exceptions import ParameterError
from ...executor import ExecuteStateListener
from ...executors import ThreadFunctionExecutor
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
)
from ...utils import IconType
from ...window import BaseWindow, BaseWindowConfig

DEFAULT_WINDOW_SIZE = (1024, 768)

DEFAULT_EXECUTOR_CLASS = ThreadFunctionExecutor

ParameterWidgetType = Union[
    Tuple[Type[BaseParameterWidget], Union[BaseParameterWidgetConfig, dict]],
    BaseParameterWidgetConfig,
]

DockWidgetArea = Qt.DockWidgetArea
NoDockWidgetArea = Qt.DockWidgetArea.NoDockWidgetArea
BottomDockWidgetArea = Qt.DockWidgetArea.BottomDockWidgetArea
TopDockWidgetArea = Qt.DockWidgetArea.TopDockWidgetArea
LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea
DockWidgetAreas = Union[DockWidgetArea, int]
AllDockWidgetAreas = Qt.AllDockWidgetAreas


# noinspection SpellCheckingInspection
@dataclasses.dataclass(frozen=True)
class FnExecuteWindowConfig(BaseWindowConfig):
    title: Optional[str] = None
    size: Union[Tuple[int, int], QSize] = DEFAULT_WINDOW_SIZE

    execute_button_text: str = "Execute"

    cancel_button_text: str = "Cancel"

    clear_button_visible: bool = True
    clear_button_text: str = "Clear"

    clear_checkbox_visible: bool = True
    clear_checkbox_checked: bool = True
    clear_checkbox_text: str = "clear output"

    statusbar_visible: bool = False

    initial_docks_state: Literal["auto", "tabified"] = "auto"

    output_dock_visible: bool = True
    output_dock_title: str = "Output"
    output_dock_floating: bool = False
    output_dock_initial_area: DockWidgetArea = BottomDockWidgetArea
    output_dock_initial_size: Tuple[Optional[int], Optional[int]] = (None, 230)

    document_dock_visible: bool = True
    document_dock_title: str = "Document"
    document_dock_floating: bool = False
    document_dock_initial_area: DockWidgetArea = RightDockWidgetArea
    document_dock_initial_size: Tuple[Optional[int], Optional[int]] = (614, None)

    output_browser_config: Optional[OutputBrowserConfig] = None
    document_browser_config: Optional[DocumentBrowserConfig] = None

    default_parameter_group_name: str = "Main Parameters"
    default_parameter_group_icon: IconType = None
    parameter_group_icons: Dict[str, IconType] = dataclasses.field(default_factory=dict)

    disable_widgets_on_execute: bool = False

    print_function_result: bool = True
    show_function_result: bool = False
    print_function_error: bool = True
    show_function_error: bool = True
    function_error_traceback: bool = True

    error_dialog_title: str = "Error"
    result_dialog_title: str = "Result"
    parameter_error_message: str = "{}: {}"
    function_result_message: str = "function result: {}\n"
    function_error_message: str = "{}: {}\n"
    function_executing_message: str = "A function is executing now!"
    uncancelable_function_message: str = "The function is not cancelable!"
    function_not_executing_message: str = "No function is executing now!"


# noinspection SpellCheckingInspection
class BaseFnExecuteWindow(BaseWindow, ExecuteStateListener):
    @abstractmethod
    def _create_ui(self):
        pass

    @abstractmethod
    def update_progressbar_config(self, config):
        pass

    @abstractmethod
    def show_progressbar(self):
        pass

    @abstractmethod
    def hide_progressbar(self):
        pass

    @abstractmethod
    def update_progress(self, current_value, message):
        pass

    @abstractmethod
    def append_output(self, text, html, scroll_to_bottom):
        pass

    @abstractmethod
    def clear_output(self):
        pass

    @abstractmethod
    def set_document(self, document, document_format):
        pass

    @abstractmethod
    def add_parameter(self, parameter_name, config):
        pass

    @abstractmethod
    def add_parameters(self, configs):
        pass

    @abstractmethod
    def remove_parameter(self, parameter_name, safe_remove):
        pass

    @abstractmethod
    def clear_parameters(self):
        pass

    @abstractmethod
    def get_parameter_value(self, parameter_name):
        pass

    @abstractmethod
    def get_parameter_values(self):
        pass

    @abstractmethod
    def set_parameter_value(self, parameter_name, value):
        pass

    @abstractmethod
    def set_parameter_values(self, values):
        pass

    @abstractmethod
    def set_output_dock_property(self, title, visible, floating, area):
        pass

    @abstractmethod
    def set_document_dock_property(self, title, visible, floating, area):
        pass

    @abstractmethod
    def set_allowed_dock_areas(self, areas):
        pass

    @abstractmethod
    def set_output_dock_visible(self, visible):
        pass

    @abstractmethod
    def is_output_dock_visible(self):
        pass

    @abstractmethod
    def set_document_dock_visible(self, visible):
        pass

    @abstractmethod
    def is_document_dock_visible(self):
        pass

    @abstractmethod
    def set_document_dock_floating(self, floating):
        pass

    @abstractmethod
    def is_document_dock_floating(self):
        pass

    @abstractmethod
    def set_output_dock_floating(self, floating):
        pass

    @abstractmethod
    def is_output_dock_floating(self):
        pass

    @abstractmethod
    def set_document_dock_title(self, title):
        pass

    @abstractmethod
    def get_document_dock_title(self):
        pass

    @abstractmethod
    def set_output_dock_title(self, title):
        pass

    @abstractmethod
    def get_output_dock_title(self):
        pass

    @abstractmethod
    def set_document_dock_area(self, area):
        pass

    @abstractmethod
    def get_document_dock_area(self):
        pass

    @abstractmethod
    def set_output_dock_area(self, area):
        pass

    @abstractmethod
    def get_output_dock_area(self):
        pass

    @abstractmethod
    def resize_document_dock(self, size):
        pass

    @abstractmethod
    def resize_output_dock(self, size):
        pass

    @abstractmethod
    def tabify_docks(self):
        pass

    @abstractmethod
    def set_statusbar_visible(self, visible):
        pass

    @abstractmethod
    def is_statusbar_visible(self):
        pass

    @abstractmethod
    def show_statusbar_message(self, message, timeout):
        pass

    @abstractmethod
    def clear_statusbar_message(self):
        pass

    @abstractmethod
    def set_execute_button_text(self, text):
        pass

    @abstractmethod
    def set_cancel_button_text(self, text):
        pass

    @abstractmethod
    def set_clear_button_text(self, text):
        pass

    @abstractmethod
    def set_clear_checkbox_text(self, text):
        pass

    @abstractmethod
    def set_clear_button_visible(self, visible):
        pass

    @abstractmethod
    def set_clear_checkbox_visible(self, visible):
        pass

    @abstractmethod
    def set_clear_checkbox_checked(self, checked):
        pass

    @abstractmethod
    def is_clear_checkbox_checked(self):
        pass

    @abstractmethod
    def is_function_executing(self) -> bool:
        pass

    @abstractmethod
    def is_function_cancelable(self) -> bool:
        pass

    @abstractmethod
    def process_parameter_error(self, e: ParameterError):
        pass

    @abstractmethod
    def get_parameter_names(self):
        pass

    @abstractmethod
    def get_parameter_names_of(self, group_name):
        pass

    @abstractmethod
    def get_document_dock_size(self):
        pass

    @abstractmethod
    def get_output_dock_size(self):
        pass

    @abstractmethod
    def disable_parameter_widgets(self, disabled):
        pass
