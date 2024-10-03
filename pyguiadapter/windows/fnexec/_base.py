import dataclasses
from abc import abstractmethod
from typing import Tuple, Dict, Union, Type, Optional

from qtpy.QtCore import QSize, Qt

from ._output_area import ProgressBarConfig, OutputBrowserConfig
from .._docbrowser import DocumentBrowserConfig
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
BottomDockWidgetArea = Qt.DockWidgetArea.BottomDockWidgetArea
TopDockWidgetArea = Qt.DockWidgetArea.TopDockWidgetArea
LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea


@dataclasses.dataclass
class FnExecuteWindowConfig(BaseWindowConfig):
    title: Optional[str] = None
    size: Union[Tuple[int, int], QSize] = DEFAULT_WINDOW_SIZE

    execute_button_text: str = "Execute"

    cancel_button_text: str = "Cancel"

    show_clear_button: bool = True
    clear_button_text: str = "Clear"

    show_clear_checkbox: bool = True
    clear_checkbox_text: str = "clear output"

    show_output_dock: bool = True
    output_dock_title: str = "Output"
    output_dock_ratio: float = 0.30
    output_dock_floating: bool = False
    output_dock_position: DockWidgetArea = BottomDockWidgetArea

    show_document_dock: bool = True
    document_dock_title: str = "Document"
    document_dock_ratio: float = 0.60
    document_dock_floating: bool = False
    document_dock_position: DockWidgetArea = RightDockWidgetArea

    tabify_docks: bool = False

    progressbar_config: Optional[ProgressBarConfig] = None
    output_browser_config: OutputBrowserConfig = dataclasses.field(
        default_factory=OutputBrowserConfig
    )
    document_browser_config: Optional[DocumentBrowserConfig] = dataclasses.field(
        default_factory=DocumentBrowserConfig
    )
    default_parameter_group_name: str = "Main Parameters"
    default_parameter_group_icon: IconType = None
    parameter_group_icons: Dict[str, IconType] = dataclasses.field(default_factory=dict)
    enable_auto_clear: bool = True
    print_function_result: bool = True
    show_function_result: bool = False
    print_function_error: bool = True
    show_function_error: bool = True
    show_error_traceback: bool = True

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
