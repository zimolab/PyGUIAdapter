import dataclasses
from abc import abstractmethod
from typing import Tuple, Dict, Union, Type, Optional, Literal

from qtpy.QtCore import QSize, Qt

from ._output_area import OutputBrowserConfig
from ..document_browser import DocumentBrowserConfig
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
DockWidgetAreas = Qt.DockWidgetAreas
AllDockWidgetAreas = Qt.AllDockWidgetAreas
NoDockWidgetArea = Qt.DockWidgetArea.NoDockWidgetArea
BottomDockWidgetArea = Qt.DockWidgetArea.BottomDockWidgetArea
TopDockWidgetArea = Qt.DockWidgetArea.TopDockWidgetArea
LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea


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
