from __future__ import annotations

import dataclasses
from typing import Tuple, Literal, Dict, Union, Type, Any, List

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from ._docarea import FnDocumentArea
from ._outputarea import (
    ProgressBarConfig,
    OutputBrowserConfig,
    FnExecuteOutputArea,
)
from ._paramarea import FnParameterArea, FnParameterGroupBox
from .._docbrowser import DocumentBrowserConfig
from ... import bundle as bd
from ... import utils, fn
from ...adapter import ucontext
from ...exceptions import FunctionExecutingError, ParameterError
from ...executor import ExecuteStateListener, BaseFunctionExecutor
from ...executors import ThreadFunctionExecutor
from ...fn import ParameterInfo
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    is_parameter_widget_class,
)
from ...widgets.common import CommonParameterWidgetConfig
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
    function_result: str = "function result: {}"
    function_error: str = "{}: {}"
    parameter_error: str = "{}: {}"


@dataclasses.dataclass
class FnExecuteWindowConfig(BaseWindowConfig):
    title: str = ""
    size: Tuple[int, int] | QSize = DEFAULT_WINDOW_SIZE
    output_dock_ratio: float = 0.3
    document_dock_ratio: float = 0.65
    show_output_dock: bool = True
    output_dock_floating: bool = False
    output_dock_position: DockWidgetArea = Qt.BottomDockWidgetArea
    show_document_dock: bool = True
    document_dock_floating: bool = False
    document_dock_position: DockWidgetArea = Qt.RightDockWidgetArea
    tabify_docks: bool = False

    progressbar: ProgressBarConfig | None = None
    output_config: OutputBrowserConfig = dataclasses.field(
        default_factory=OutputBrowserConfig
    )
    document_config: DocumentBrowserConfig | None = dataclasses.field(
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
class FnExecuteWindow(BaseWindow, ExecuteStateListener):
    def __init__(self, parent: QWidget | None, bundle: bd.FnBundle):
        self._bundle = bundle

        self._center_widget: QWidget | None = None
        self._parameters_area: FnParameterArea | None = None
        self._document_area: FnDocumentArea | None = None
        self._output_area: FnExecuteOutputArea | None = None
        self._document_dock: QDockWidget | None = None
        self._output_dock: QDockWidget | None = None

        super().__init__(parent, bundle.window_config)

        executor_class = self._bundle.fn_info.executor or DEFAULT_EXECUTOR_CLASS
        # noinspection PyTypeChecker
        self._executor = executor_class(self, self)

        self.add_parameters(self._bundle.param_widget_configs)

        # noinspection PyProtectedMember
        ucontext._current_window_created(self)

    @property
    def window_config(self) -> FnExecuteWindowConfig:
        return self._bundle.window_config

    @property
    def widget_texts(self) -> WidgetTexts:
        return self.window_config.widget_texts

    @property
    def message_texts(self) -> MessageTexts:
        return self.window_config.message_texts

    @property
    def current_executor(self) -> BaseFunctionExecutor:
        return self._executor

    def update_progressbar_config(self, config: ProgressBarConfig | None):
        self._output_area.update_progressbar_config(config)

    def show_progressbar(self):
        self._output_area.show_progressbar()

    def hide_progressbar(self):
        self._output_area.hide_progressbar()

    def update_progress(self, current_value: int, message: str | None = None):
        self._output_area.update_progress(current_value, message)

    def append_output(self, text: str, html: bool = False):
        self._output_area.append_output(text, html)

    def clear_output(self):
        self._output_area.clear_output()

    def update_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        self._document_area.update_document(document, document_format)

    def add_parameter(
        self, parameter_name: str, config: ParameterWidgetType
    ) -> BaseParameterWidget:
        param_info = self._bundle.fn_info.parameters.get(parameter_name)
        widget_class, widget_config = self._get_widget_class_and_config(
            parameter_name, param_info, config
        )

        try:
            widget = self._param_groups.add_parameter(
                parameter_name, widget_class, widget_config
            )
            if isinstance(widget_config, CommonParameterWidgetConfig):
                # apply set_default_value_on_init
                # set_value() may raise exceptions, we need to catch ParameterValidationError of them
                # typically, this kind of exception is not fatal, it unnessessary to exit the whole program
                # when this kind of exception raised
                if widget_config.set_default_value_on_init:
                    widget.set_value(widget_config.default_value)
        except ParameterError as e:
            self._process_param_error(e)
        except Exception as e:
            # any other exceptions are seen as fatal and will cause the whole program to exit
            utils.show_exception_message(
                self,
                exception=e,
                message=f"An fatal error occurred when creating widget for parameter '{parameter_name}':",
                title="Fatal",
            )
            exit(-1)
        else:
            return widget

    def add_parameters(self, configs: Dict[str, ParameterWidgetType]):
        for parameter_name, config in configs.items():
            self.add_parameter(parameter_name, config)

    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        self._param_groups.remove_parameter(parameter_name, safe_remove=safe_remove)

    def clear_parameters(self):
        self._param_groups.clear_parameters()
        self._param_groups.add_default_group()

    def get_parameter_value(self, parameter_name: str) -> Any:
        return self._param_groups.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        return self._param_groups.get_parameter_values()

    def set_parameter_value(
        self, parameter_name: str, value: Any, ignore_unknown_parameter: bool = True
    ):
        self._param_groups.set_parameter_value(
            parameter_name, value, ignore_unknown_parameter=ignore_unknown_parameter
        )

    def set_parameter_values(self, values: Dict[str, Any]) -> List[str]:
        return self._param_groups.set_parameter_values(values)

    @staticmethod
    def _get_widget_class_and_config(
        param_name: str, param_info: ParameterInfo, config: ParameterWidgetType
    ) -> Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]:
        if isinstance(config, tuple):
            assert len(config) == 2
            assert is_parameter_widget_class(config[0])
            assert isinstance(config[1], (BaseParameterWidgetConfig, dict))
            widget_class, widget_config = config
        elif isinstance(config, BaseParameterWidgetConfig):
            widget_class = config.target_widget_class()
            widget_config = config
        else:
            raise ValueError(f"invalid type of config: {type(config)}")

        if not isinstance(widget_config, (dict, BaseParameterWidgetConfig)):
            raise ValueError(f"invalid type of config: {type(config)}")

        if isinstance(widget_config, dict):
            widget_config = widget_class.ConfigClass.new(**widget_config)

        if widget_config.description is None or widget_config.description == "":
            if param_info.description is not None and param_info.description != "":
                widget_config = dataclasses.replace(
                    widget_config, description=param_info.description
                )

        widget_config = widget_class.after_process_config(
            widget_config, param_name, param_info
        )
        return widget_class, widget_config

    # noinspection PyUnresolvedReferences
    def _setup_ui(self):
        super()._setup_ui()

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
        # noinspection PyArgumentList
        _layout_main = QVBoxLayout(self._center_widget)
        self.setCentralWidget(self._center_widget)

        # create the area for parameter widgets
        self._parameters_area = FnParameterArea(self._center_widget, window_config)
        _layout_main.addWidget(self._parameters_area)
        if fn_info.cancelable:
            self._parameters_area.show_cancel_button()
        else:
            self._parameters_area.hide_cancel_button()
        if window_config.show_clear_button:
            self._parameters_area.show_clear_button()
        else:
            self._parameters_area.hide_clear_button()
        self._parameters_area.enable_auto_clear(window_config.enable_auto_clear)
        self._parameters_area.execute_button_clicked.connect(
            self._on_execute_button_clicked
        )
        self._parameters_area.clear_button_clicked.connect(
            self._on_clear_button_clicked
        )
        self._parameters_area.cancel_button_clicked.connect(
            self._on_cancel_button_clicked
        )

        # create the dock widget and document area
        self._document_dock = QDockWidget(self)
        self._document_dock.setWindowTitle(widget_texts.document_dock_title)
        self._document_area = FnDocumentArea(
            self._document_dock, window_config.document_config
        )
        self._document_dock.setWidget(self._document_area)
        self.addDockWidget(
            self.window_config.document_dock_position, self._document_dock
        )
        self._document_dock.setFloating(self.window_config.document_dock_floating)
        # display the document content
        self.update_document(fn_info.document, fn_info.document_format)
        if self.window_config.show_document_dock:
            self._document_dock.show()
        else:
            self._document_dock.hide()

        # create the dock widget and output area
        self._output_dock = QDockWidget(self)
        self._output_dock.setWindowTitle(widget_texts.output_dock_title)
        self._output_area = FnExecuteOutputArea(
            self._output_dock,
            progressbar_config=window_config.progressbar,
            output_browser_config=window_config.output_config,
        )
        self._output_dock.setWidget(self._output_area)
        self.addDockWidget(self.window_config.output_dock_position, self._output_dock)

        if self.window_config.tabify_docks:
            self.tabifyDockWidget(self._document_dock, self._output_dock)

        if window_config.progressbar is None:
            self.hide_progressbar()
        else:
            self.show_progressbar()
        if self.window_config.show_output_dock:
            self._output_dock.show()
        else:
            self._output_dock.hide()

        # resize the docks
        current_width = self.width()
        current_height = self.height()
        output_dock_ratio = window_config.output_dock_ratio
        output_dock_ratio = min(max(output_dock_ratio, 0.1), 1.0)
        dock_height = int(current_height * output_dock_ratio)
        document_dock_ratio = min(max(window_config.document_dock_ratio, 0.1), 1.0)
        dock_width = int(current_width * document_dock_ratio)
        self.resizeDocks([self._output_dock], [dock_height], Qt.Vertical)
        self.resizeDocks(
            [self._document_dock],
            [dock_width],
            Qt.Horizontal,
        )

        self._output_dock.setFloating(self.window_config.output_dock_floating)

    def before_execute(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        super().before_execute(fn_info, arguments)
        if self._parameters_area.is_auto_clear_enabled:
            self.clear_output()
        self._parameters_area.enable_clear_button(False)
        self._parameters_area.enable_execute_button(False)

        self._parameters_area.parameter_groups.clear_validation_error(None)

    def on_execute_start(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_start(fn_info, arguments)
        self._parameters_area.enable_cancel_button(True)

    def on_execute_finish(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_finish(fn_info, arguments)
        self._parameters_area.enable_clear_button(True)
        self._parameters_area.enable_execute_button(True)
        self._parameters_area.enable_cancel_button(False)

    def on_execute_result(
        self, fn_info: fn.FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        if callable(self._bundle.on_execute_result):
            self._bundle.on_execute_result(result, arguments.copy())
            return

        result_str = self.message_texts.function_result.format(result)

        if self.window_config.print_function_result:
            self.append_output(result_str)

        if self.window_config.show_function_result:
            utils.show_info_message(
                self, result_str, title=self.widget_texts.result_dialog_title
            )

    def on_execute_error(
        self, fn_info: fn.FnInfo, arguments: Dict[str, Any], error: Exception
    ):

        if isinstance(error, ParameterError):
            self._process_param_error(error)
            del error
            return

        if callable(self._bundle.on_execute_error):
            self._bundle.on_execute_error(error, arguments.copy())
            del error
            return

        error_type = type(error).__name__
        error_msg = self.message_texts.function_error.format(error_type, str(error))
        if self.window_config.print_function_error:
            if not self.window_config.show_error_traceback:
                self.append_output(error_msg)
            else:
                self.append_output(utils.get_traceback(error))

        if self.window_config.show_function_error:
            if not self.window_config.show_error_traceback:
                utils.show_critical_message(
                    self,
                    error_msg,
                    title=self.widget_texts.universal_error_dialog_title,
                )
            else:
                utils.show_exception_message(
                    self,
                    exception=error,
                    title=self.widget_texts.universal_error_dialog_title,
                )
        del error

    def _on_close(self) -> bool:
        if self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_executing)
            return False
        return super()._on_close()

    def _on_cleanup(self):
        super()._on_cleanup()
        self._parameters_area.parameter_groups.clear_parameters()

    def _on_destroy(self):
        super()._on_destroy()
        # noinspection PyProtectedMember
        ucontext._current_window_destroyed()

    def _on_cancel_button_clicked(self):
        if not self._bundle.fn_info.cancelable:
            utils.show_warning_message(self, self.message_texts.function_not_cancelable)
            return
        if not self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_not_executing)
        else:
            self._executor.try_cancel()

    def _on_execute_button_clicked(self):
        if self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_executing)
            return
        try:
            arguments = self.get_parameter_values()
        except FunctionExecutingError:
            utils.show_warning_message(self, self.message_texts.function_executing)
        except ParameterError as e:
            self._process_param_error(e)
        else:
            self._executor.execute(self._bundle.fn_info, arguments)

    # noinspection PyMethodMayBeStatic
    def _on_clear_button_clicked(self):
        if self._executor.is_executing:
            utils.show_warning_message(self, self.message_texts.function_executing)
            pass
        self.clear_output()

    def _process_param_error(self, e: ParameterError):
        self._param_groups.notify_validation_error(e.parameter_name, e.message)
        msg = self.message_texts.parameter_error.format(e.parameter_name, e.message)
        utils.show_critical_message(
            self, msg, title=self.widget_texts.parameter_error_dialog_title
        )
        self._param_groups.scroll_to_parameter(e.parameter_name)
        del e

    @property
    def _param_groups(self) -> FnParameterGroupBox:
        return self._parameters_area.parameter_groups
