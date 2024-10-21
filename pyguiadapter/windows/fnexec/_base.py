import dataclasses
from abc import abstractmethod
from typing import Tuple, Dict, Union, Type, Optional, Literal, Any, Callable

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
from ...window import (
    BaseWindow,
    BaseWindowConfig,
    BaseWindowEventListener,
)

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
    """窗口标题。"""

    size: Union[Tuple[int, int], QSize] = (800, 600)
    """窗口大小。"""

    execute_button_text: str = "Execute"
    """执行按钮文本。"""

    cancel_button_text: str = "Cancel"
    """取消按钮文本。"""

    clear_button_text: str = "Clear"
    """清除按钮文本。"""

    clear_button_visible: bool = True
    """是否显示清除按钮。"""

    clear_checkbox_text: str = "clear output"
    """清除选项框文本。"""

    clear_checkbox_visible: bool = True
    """是否显示清除选项框。"""

    clear_checkbox_checked: bool = True
    """是否将清除选项框设置为选中状态。"""

    statusbar_visible: bool = False
    """是否显示窗口状态栏"""

    initial_docks_state: Literal["auto", "tabified"] = "auto"
    """停靠窗口的初始状态。可选`auto`或`tabified`。当指定为`tabified`时，停靠窗口将组合成一个`Tab`组件，每个停靠窗口都将以`Tab页`的形式出现。"""

    output_dock_visible: bool = True
    """是否显示`Output停靠窗口`。"""

    output_dock_title: str = "Output"
    """`Output停靠窗口`的标题。"""

    output_dock_floating: bool = False
    """是否使`Output停靠窗口`处于悬浮状态。"""

    output_dock_initial_area: DockWidgetArea = BottomDockWidgetArea
    """`Output停靠窗口`的初始停靠区域。"""

    output_dock_initial_size: Tuple[Optional[int], Optional[int]] = (None, 150)
    """`Output停靠窗口`的初始大小，格式为`(width, height)`，可以只设置其中一个维度，另一个不需要设置的维度置为`None`即可。"""

    document_dock_visible: bool = True
    """是否显示`Document停靠窗口`。"""

    document_dock_title: str = "Document"
    """`Document停靠窗口`的标题。"""

    document_dock_floating: bool = False
    """是否使`Document停靠窗口`处于悬浮状态。"""

    document_dock_initial_area: DockWidgetArea = RightDockWidgetArea
    """`Document停靠窗口`的初始停靠区域。"""

    document_dock_initial_size: Tuple[Optional[int], Optional[int]] = (450, None)
    """`Document停靠窗口`的初始大小，格式为`(width, height)`，可以只设置其中一个维度，另一个不需要设置的维度置为`None`即可。"""

    output_browser_config: Optional[OutputBrowserConfig] = None
    """`输出浏览器`的配置。"""

    document_browser_config: Optional[DocumentBrowserConfig] = None
    """`文档浏览器`的配置。"""

    default_parameter_group_name: str = "Main Parameters"
    """默认函数参数分组的名称。"""

    default_parameter_group_icon: IconType = None
    """默认函数参数分组的图标。"""

    parameter_group_icons: Dict[str, IconType] = dataclasses.field(default_factory=dict)
    """除默认函数参数分组外其他函数参数分组的图标"""

    disable_widgets_on_execute: bool = False
    """是否在函数执行期间使参数控件处于不可输入状态。"""

    print_function_result: bool = True
    """是否在`输出浏览器`中打印函数调用结果。"""

    show_function_result: bool = False
    """是否弹窗显示函数调用结果。"""

    print_function_error: bool = True
    """是否在`输出浏览器`中打印函数执行过程中发生的异常和错误。"""

    show_function_error: bool = True
    """是否弹窗显示函数执行过程中发生的异常和错误。"""

    function_error_traceback: bool = True
    """在打印或弹窗显示函数执行过程中发生的异常时，是否显示异常的回溯信息。"""

    error_dialog_title: str = "Error"
    """错误信息弹窗的标题。"""

    result_dialog_title: str = "Result"
    """函数调用结果弹窗的标题。"""

    parameter_error_message: str = "{}: {}"
    """`ParameterError`类型异常的消息模板，模板第一个变量（`{}`）为`参数名称`，第二个变量(`{}`)为`异常的消息（message）`。"""

    function_result_message: str = "function result: {}\n"
    """函数调用结果的消息模板，模板变量（`{}`）为函数的返回值。"""

    function_error_message: str = "{}: {}\n"
    """函数异常或错误的消息模板，模板第一个变量（`{}`）为`异常的类型`，第二个变量(`{}`)为`异常的消息（message）`。"""

    function_executing_message: str = "A function is executing now!"
    """提示消息，用以提示“函数正在执行”。"""

    uncancelable_function_message: str = "The function is not cancelable!"
    """提示消息，用以提示“当前函数为不可取消的函数”。"""

    function_not_executing_message: str = "No function is executing now!"
    """提示消息，用以提示“当前函数未处于执行状态”。"""


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
    def has_parameter(self, parameter_name) -> bool:
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

    @abstractmethod
    def get_parameter_values_of(self, group_name):
        pass

    @abstractmethod
    def try_cancel_execution(self):
        pass


class FnExecuteWindowEventListener(BaseWindowEventListener):
    def on_execute_start(self, window: BaseFnExecuteWindow) -> None:
        """
        在函数执行开始时回调。

        Args:
            window: 当前窗口实例

        Returns:
            无返回值
        """
        pass

    def on_execute_result(self, window: BaseFnExecuteWindow, result: Any) -> bool:
        """
        在函数执行成功（函数返回）时回调。

        Args:
            window: 当前窗口实例
            result: 函数的返回值

        Returns:
            如果返回`True`，则允许`PyGUIAdapter`执行默认的后续操作，比如打印函数结果或弹窗显示函数结果等，否则阻止执行默认操作。默认返回`True`。
        """
        return True

    def on_execute_error(self, window: BaseFnExecuteWindow, error: Exception) -> bool:
        """
        在函数执行失败（函数抛出异常）时回调。

        Args:
            window: 当前窗口实例
            error: 函数抛出的异常

        Returns:
            如果返回`True`，则允许`PyGUIAdapter`执行默认的后续操作，比如打印函数异常或弹窗显示函数异常等，否则阻止执行默认操作。默认返回`True`。
        """
        return True

    def on_execute_finish(self, window: BaseFnExecuteWindow) -> None:
        """
        在函数执行结束时回调，无论函数执行是否成功，该回调函数都会被调用。

        Args:
            window: 当前窗口实例

        Returns:
            无返回值
        """
        pass


class SimpleFnExecuteWindowEventListener(FnExecuteWindowEventListener):
    """
    一个简单的`FnExecuteWindowEventListener`实现，方便不喜欢子类化方式的开发者使用。
    """

    def __init__(
        self,
        on_create: Callable[[BaseFnExecuteWindow], None] = None,
        on_show: Callable[[BaseFnExecuteWindow], None] = None,
        on_hide: Callable[[BaseFnExecuteWindow], None] = None,
        on_close: Callable[[BaseFnExecuteWindow], bool] = None,
        on_destroy: Callable[[BaseFnExecuteWindow], None] = None,
        on_execute_start: Callable[[BaseFnExecuteWindow], None] = None,
        on_execute_result: Callable[[BaseFnExecuteWindow, Any], bool] = None,
        on_execute_error: Callable[[BaseFnExecuteWindow, Exception], bool] = None,
        on_execute_finish: Callable[[BaseFnExecuteWindow], None] = None,
    ):
        """
        构造函数。

        Args:
            on_create: `on_create`回调函数
            on_show:  `on_show`回调函数
            on_hide:  `on_hide`回调函数
            on_close:  `on_close`回调函数
            on_destroy: `on_destroy`回调函数
            on_execute_start: `on_execute_start`回调函数
            on_execute_result: `on_execute_result`回调函数
            on_execute_error:  `on_execute_error`回调函数
            on_execute_finish:  `on_execute_finish`回调函数
        """
        self._on_create = on_create
        self._on_show = on_show
        self._on_hide = on_hide
        self._on_close = on_close
        self._on_destroy = on_destroy
        self._on_execute_start = on_execute_start
        self._on_execute_result = on_execute_result
        self._on_execute_error = on_execute_error
        self._on_execute_finish = on_execute_finish

    def on_create(self, window: BaseFnExecuteWindow) -> None:
        if self._on_create is not None:
            return self._on_create(window)
        return super().on_create(window)

    def on_show(self, window: BaseFnExecuteWindow) -> None:
        if self._on_show is not None:
            return self._on_show(window)
        return super().on_show(window)

    def on_hide(self, window: BaseFnExecuteWindow) -> None:
        if self._on_hide is not None:
            return self._on_hide(window)
        return super().on_hide(window)

    def on_close(self, window: BaseFnExecuteWindow) -> bool:
        if self._on_close is not None:
            return self._on_close(window)
        return super().on_close(window)

    def on_destroy(self, window: BaseFnExecuteWindow) -> None:
        if self._on_destroy is not None:
            return self._on_destroy(window)
        super().on_destroy(window)

    def on_execute_start(self, window: BaseFnExecuteWindow) -> None:
        if self._on_execute_start is not None:
            return self._on_execute_start(window)
        return super().on_execute_start(window)

    def on_execute_result(self, window: BaseFnExecuteWindow, result: Any) -> bool:
        if self._on_execute_result is not None:
            return self._on_execute_result(window, result)
        return super().on_execute_result(window, result)

    def on_execute_error(self, window: BaseFnExecuteWindow, error: Exception) -> bool:
        if self._on_execute_error is not None:
            return self._on_execute_error(window, error)
        return super().on_execute_error(window, error)

    def on_execute_finish(self, window: BaseFnExecuteWindow) -> None:
        if self._on_execute_finish is not None:
            return self._on_execute_finish(window)
        return super().on_execute_finish(window)
