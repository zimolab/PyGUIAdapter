from __future__ import annotations

import dataclasses
import threading
from dbm.dumb import error
from typing import Tuple, Literal, Dict, Union, Type, Any, List

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from ._docarea import FnDocumentArea
from ._logarea import (
    ProgressBarConfig,
    LogOutputConfig,
    FnExecuteLogOutputArea,
)
from ._paramarea import FnParameterArea
from .._docbrowser import DocumentBrowserConfig
from ... import utils, fn
from ...adapter import ucontext
from ...bundle import FnBundle
from ...executor import ExecuteStateListener, AlreadyExecutingError
from ...executors import ThreadedFunctionExecutor
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    is_parameter_widget_class,
)
from ...window import BaseWindow, BaseWindowConfig

DEFAULT_WINDOW_SIZE = (1024, 768)
DEFAULT_EXECUTOR_CLASS = ThreadedFunctionExecutor

ParameterWidgetType = Union[
    Tuple[Type[BaseParameterWidget], Union[BaseParameterWidgetConfig, dict]],
    BaseParameterWidgetConfig,
]


@dataclasses.dataclass
class WidgetTexts(object):
    document_dock_title: str = "Document"
    log_output_dock_title: str = "Log Output"
    execute_button_text: str = "Execute"
    clear_button_text: str = "Clear"
    cancel_button_text: str = "Cancel"
    clear_checkbox_text: str = "Clear log output"


@dataclasses.dataclass
class MessageTexts(object):
    function_is_executing: str = "function is executing now"
    function_not_executing: str = "function is not executing now"
    function_not_cancelable: str = "function is not cancelable"


@dataclasses.dataclass
class FnExecuteWindowConfig(BaseWindowConfig):
    title: str = ""
    size: Tuple[int, int] | QSize = DEFAULT_WINDOW_SIZE
    log_output_dock_ratio: float = 0.3
    document_dock_ratio: float = 0.65
    progressbar: ProgressBarConfig | None = None
    log_output: LogOutputConfig = dataclasses.field(default_factory=LogOutputConfig)
    document_browser: DocumentBrowserConfig | None = dataclasses.field(
        default_factory=DocumentBrowserConfig
    )
    default_parameter_group_name: str = "Main Parameters"
    default_parameter_group_icon: utils.IconType = None
    parameter_group_icons: Dict[str, utils.IconType] = dataclasses.field(
        default_factory=dict
    )
    show_clear_button: bool = True
    enable_auto_clear: bool = True

    widget_texts: WidgetTexts = dataclasses.field(default_factory=WidgetTexts)
    message_texts: MessageTexts = dataclasses.field(default_factory=MessageTexts)


# noinspection SpellCheckingInspection
class FnExecuteWindow(BaseWindow, ExecuteStateListener):
    def __init__(self, parent: QWidget | None, bundle: FnBundle):
        self._bundle = bundle
        self._process_cancelable_function()
        super().__init__(parent, bundle.window_config)

        executor_class = self._bundle.fn_info.executor or DEFAULT_EXECUTOR_CLASS
        # noinspection PyTypeChecker
        self._executor = executor_class(self, self)

        ucontext.window_created(self)

        self.add_parameters(self._bundle.parameter_widget_configs)

    @property
    def window_config(self) -> FnExecuteWindowConfig:
        return self._bundle.window_config

    @property
    def widget_texts(self) -> WidgetTexts:
        return self.window_config.widget_texts

    @property
    def message_texts(self) -> MessageTexts:
        return self.window_config.message_texts

    def update_progressbar_config(self, config: ProgressBarConfig | None):
        self._area_log.update_progressbar_config(config)

    def show_progressbar(self):
        self._area_log.show_progressbar()

    def hide_progressbar(self):
        self._area_log.hide_progressbar()

    def update_progress(self, current_value: int, message: str | None = None):
        self._area_log.update_progress(current_value, message)

    def append_log(self, log_text: str, html: bool = False):
        self._area_log.append_log_output(log_text, html)

    def clear_log(self):
        self._area_log.clear_log_output()

    def update_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        self._area_document.set_fn_document(document, document_format)

    def add_parameter(self, parameter_name: str, config: ParameterWidgetType):
        if isinstance(config, tuple):
            assert len(config) == 2
            assert is_parameter_widget_class(config[0])
            assert isinstance(config[1], (BaseParameterWidgetConfig, dict))
            widget_class, widget_config = config
        elif isinstance(config, BaseParameterWidgetConfig):
            widget_class = config.target_widget_class()
            widget_config = config
        else:
            raise TypeError(f"Invalid type for widget_config: {type(config)}")

        if isinstance(widget_config, dict):
            widget_config = widget_class.ConfigClass.new(**widget_config)

        groupbox = self._area_parameters.parameter_group_box
        groupbox.add_parameter(parameter_name, widget_class, widget_config)

    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        groupbox = self._area_parameters.parameter_group_box
        groupbox.remove_parameter(parameter_name, safe_remove=safe_remove)

    def clear_parameters(self):
        groupbox = self._area_parameters.parameter_group_box
        groupbox.clear_parameters()
        groupbox.add_default_group()

    def get_parameter_value(self, parameter_name: str) -> Any:
        groupbox = self._area_parameters.parameter_group_box
        return groupbox.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        groupbox = self._area_parameters.parameter_group_box
        return groupbox.get_parameter_values()

    def set_parameter_value(
        self, parameter_name: str, value: Any, ignore_unknown_parameter: bool = True
    ):
        groupbox = self._area_parameters.parameter_group_box
        groupbox.set_parameter_value(
            parameter_name, value, ignore_unknown_parameter=ignore_unknown_parameter
        )

    def set_parameter_values(self, values: Dict[str, Any]) -> List[str]:
        groupbox = self._area_parameters.parameter_group_box
        return groupbox.set_parameter_values(values)

    def add_parameters(self, configs: Dict[str, ParameterWidgetType]):
        for parameter_name, config in configs.items():
            self.add_parameter(parameter_name, config)

    # noinspection PyUnresolvedReferences
    def _update_ui(self):
        super()._update_ui()

        fn_info = self._bundle.fn_info
        window_config = self.window_config
        widget_texts = self.widget_texts

        # set title and icon
        title = self._config.title or fn_info.display_name
        icon = self._config.icon or fn_info.icon
        icon = utils.get_icon(icon) or QIcon()
        self.setWindowTitle(title)
        self.setWindowIcon(icon)

        # central widget and layout
        self._center_widget = QWidget(self)
        self._vlayout_main = QVBoxLayout(self._center_widget)
        self.setCentralWidget(self._center_widget)

        # create the area for parameter widgets
        self._area_parameters = FnParameterArea(self._center_widget, window_config)
        self._vlayout_main.addWidget(self._area_parameters)
        if fn_info.cancelable:
            self._area_parameters.show_cancel_button()
        else:
            self._area_parameters.hide_cancel_button()
        if window_config.show_clear_button:
            self._area_parameters.show_clear_button()
        else:
            self._area_parameters.hide_clear_button()
        self._area_parameters.enable_auto_clear(window_config.enable_auto_clear)
        self._area_parameters.execute_button_clicked.connect(
            self._on_execute_button_clicked
        )
        self._area_parameters.clear_button_clicked.connect(
            self._on_clear_button_clicked
        )
        self._area_parameters.cancel_button_clicked.connect(
            self._on_cancel_button_clicked
        )

        # create the dock widget and document area
        self._dockwidget_document = QDockWidget(self)
        self._dockwidget_document.setWindowTitle(widget_texts.document_dock_title)
        self._area_document = FnDocumentArea(
            self._dockwidget_document, window_config.document_browser
        )
        self._dockwidget_document.setWidget(self._area_document)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockwidget_document)
        # display the document content
        self.update_document(fn_info.document, fn_info.document_format)

        # create the dock widget and log output area
        self._dockwidget_log_output = QDockWidget(self)
        self._dockwidget_log_output.setWindowTitle(widget_texts.log_output_dock_title)
        self._area_log = FnExecuteLogOutputArea(
            self._dockwidget_log_output,
            progressbar_config=window_config.progressbar,
            log_output_config=window_config.log_output,
        )
        self._dockwidget_log_output.setWidget(self._area_log)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._dockwidget_log_output)
        if window_config.progressbar is None:
            self.hide_progressbar()
        else:
            self.show_progressbar()

        # resize the docks
        current_width = self.width()
        current_height = self.height()
        log_output_dock_ratio = window_config.log_output_dock_ratio
        log_output_dock_ratio = min(max(log_output_dock_ratio, 0.1), 1.0)
        dock_height = int(current_height * log_output_dock_ratio)
        document_dock_ratio = min(max(window_config.document_dock_ratio, 0.1), 1.0)
        dock_width = int(current_width * document_dock_ratio)
        self.resizeDocks([self._dockwidget_log_output], [dock_height], Qt.Vertical)
        self.resizeDocks(
            [self._dockwidget_document],
            [dock_width],
            Qt.Horizontal,
        )

    def before_execute(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        super().before_execute(fn_info, arguments)
        print("thread", threading.current_thread())
        print("before_execute")
        print()

        self._area_parameters.enable_execute_button(False)

    def on_execute_start(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_start(fn_info, arguments)
        print("thread", threading.current_thread())
        print("on_execute_start")
        print()
        self._area_parameters.enable_cancel_button(True)

    def on_execute_finish(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_finish(fn_info, arguments)
        print("thread", threading.current_thread())
        print("on_execute_finish")
        print()
        self._area_parameters.enable_execute_button(True)
        self._area_parameters.enable_cancel_button(False)

    def on_execute_result(
        self, fn_info: fn.FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        super().on_execute_result(fn_info, arguments, result)
        print("thread", threading.current_thread())
        print("on_execute_result", result)
        print()

    def on_execute_error(
        self, fn_info: fn.FnInfo, arguments: Dict[str, Any], exception: Exception
    ) -> None:
        super().on_execute_error(fn_info, arguments, exception)
        print("thread", threading.current_thread())
        print("on_execute_error", error)
        print()

    def _on_close(self) -> bool:
        if self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_is_executing)
            return False
        return super()._on_close()

    def _on_destroy(self):
        super()._on_destroy()
        ucontext.window_closed(self)

    def _on_cancel_button_clicked(self):
        if not self._bundle.fn_info.is_cancelable():
            utils.show_warning_message(self, self.message_texts.function_not_cancelable)
            return
        if not self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_not_executing)
        else:
            self._executor.try_cancel()

    def _on_execute_button_clicked(self):
        if self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_is_executing)
            return
        try:
            arguments = self.get_parameter_values()
            self._executor.execute(self._bundle.fn_info, arguments)
        except AlreadyExecutingError:
            utils.show_warning_message(self, self.message_texts.function_is_executing)

    # noinspection PyMethodMayBeStatic
    def _on_clear_button_clicked(self):
        print("_on_clear_button_clicked")
        pass

    def _process_cancelable_function(self):
        fn_info = self._bundle.fn_info
        if not fn_info.is_cancelable():
            return
        cancel_event_param_name = self._bundle.fn_info.cancel_event_parameter_name
        widget_configs = self._bundle.parameter_widget_configs
        widget_configs.pop(cancel_event_param_name, None)
