import dataclasses
from typing import Tuple, Dict, Union, Type, Optional

from qtpy.QtCore import QSize, Qt

from ._outputarea import (
    ProgressBarConfig,
    OutputBrowserConfig,
)
from .._docbrowser import DocumentBrowserConfig
from ... import utils
from ...executor import ExecuteStateListener
from ...executors import ThreadFunctionExecutor
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
)
from ...window import BaseWindow, BaseWindowConfig

DEFAULT_WINDOW_SIZE = (1024, 768)
DEFAULT_EXECUTOR_CLASS = ThreadFunctionExecutor

ParameterWidgetType = Union[
    Tuple[Type[BaseParameterWidget], Union[BaseParameterWidgetConfig, dict]],
    BaseParameterWidgetConfig,
]

DockWidgetArea = Qt.DockWidgetArea


@dataclasses.dataclass
class WidgetTexts(object):
    document_dock_title: str = "Document"
    output_dock_title: str = "Output"
    execute_button_text: str = "Execute"
    clear_button_text: str = "Clear"
    cancel_button_text: str = "Cancel"
    clear_checkbox_text: str = "Clear output"
    result_dialog_title: str = "Result"
    universal_error_dialog_title: str = "Error"
    parameter_error_dialog_title: str = "Parameter Error"


@dataclasses.dataclass
class MessageTexts(object):
    function_executing: str = "function is executing now"
    function_not_executing: str = "function is not executing now"
    function_not_cancelable: str = "function is not cancelable"
    function_result: str = "function result: {}\n"
    function_error: str = "{}: {}\n"
    parameter_error: str = "{}: {}"


@dataclasses.dataclass
class FnExecuteWindowConfig(BaseWindowConfig):
    title: str = ""
    size: Union[Tuple[int, int], QSize] = DEFAULT_WINDOW_SIZE
    output_dock_ratio: float = 0.30
    document_dock_ratio: float = 0.60
    show_output_dock: bool = True
    output_dock_floating: bool = False
    output_dock_position: DockWidgetArea = Qt.BottomDockWidgetArea
    show_document_dock: bool = True
    document_dock_floating: bool = False
    document_dock_position: DockWidgetArea = Qt.RightDockWidgetArea
    tabify_docks: bool = False

    progressbar: Optional[ProgressBarConfig] = None
    output_config: OutputBrowserConfig = dataclasses.field(
        default_factory=OutputBrowserConfig
    )
    document_config: Optional[DocumentBrowserConfig] = dataclasses.field(
        default_factory=DocumentBrowserConfig
    )
    default_parameter_group_name: str = "Main Parameters"
    default_parameter_group_icon: utils.IconType = None
    parameter_group_icons: Dict[str, utils.IconType] = dataclasses.field(
        default_factory=dict
    )
    show_clear_button: bool = True
    enable_auto_clear: bool = True
    print_function_result: bool = True
    show_function_result: bool = False
    print_function_error: bool = True
    show_function_error: bool = True
    show_error_traceback: bool = True

    widget_texts: WidgetTexts = dataclasses.field(default_factory=WidgetTexts)
    message_texts: MessageTexts = dataclasses.field(default_factory=MessageTexts)


# noinspection SpellCheckingInspection
class BaseFnExecuteWindow(BaseWindow, ExecuteStateListener):
    pass
