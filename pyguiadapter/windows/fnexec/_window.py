from typing import Tuple, Literal, Dict, Union, Type, Any, List, Optional, cast

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from ._base import (
    BaseFnExecuteWindow,
    DEFAULT_EXECUTOR_CLASS,
    FnExecuteWindowConfig,
)
from ._document_area import DocumentArea
from ._operation_area import OperationArea
from ._output_area import OutputArea, ProgressBarConfig
from ._parameter_area import ParameterArea
from ...adapter import ucontext
from ...bundle import FnBundle
from ...exceptions import FunctionExecutingError, ParameterError
from ...executor import BaseFunctionExecutor
from ...fn import FnInfo
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
)
from ...utils import messagebox, get_icon, get_traceback


class FnExecuteWindow(BaseFnExecuteWindow):
    def __init__(self, parent: Optional[QWidget], bundle: FnBundle):
        self._bundle: FnBundle = bundle

        self._center_widget: Optional[QWidget] = None

        self._operation_area: Optional[OperationArea] = None
        self._parameter_area: Optional[ParameterArea] = None
        self._document_area: Optional[DocumentArea] = None
        self._output_area: Optional[OutputArea] = None

        self._document_dock: Optional[QDockWidget] = None
        self._output_dock: Optional[QDockWidget] = None

        super().__init__(
            parent,
            bundle.window_config,
            bundle.window_listener,
            bundle.window_toolbar,
            bundle.window_menus,
        )

        executor_class = self._bundle.fn_info.executor or DEFAULT_EXECUTOR_CLASS
        # noinspection PyTypeChecker
        self._executor = executor_class(self, self)
        self.add_parameters(self._bundle.widget_configs)
        # noinspection PyProtectedMember
        ucontext._current_window_created(self)

    @property
    def current_executor(self) -> BaseFunctionExecutor:
        return self._executor

    def update_progressbar_config(self, config: Union[ProgressBarConfig, dict, None]):
        if isinstance(config, dict):
            config = ProgressBarConfig(**config)
        self._output_area.update_progressbar_config(config)

    def show_progressbar(self):
        self._output_area.show_progressbar()

    def hide_progressbar(self):
        self._output_area.hide_progressbar()
        self._output_area.scroll_to_bottom()

    def update_progress(self, current_value: int, message: Optional[str] = None):
        self._output_area.update_progress(current_value, message)

    def append_output(
        self, text: str, html: bool = False, scroll_to_bottom: bool = True
    ):
        self._output_area.append_output(text, html)
        if scroll_to_bottom:
            self._output_area.scroll_to_bottom()

    def clear_output(self):
        self._output_area.clear_output()

    def set_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        self._document_area.set_document(document, document_format)

    def add_parameter(
        self,
        parameter_name: str,
        config: Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig],
    ) -> BaseParameterWidget:
        return self._parameter_area.add_parameter(parameter_name, config)

    def add_parameters(
        self,
        configs: Dict[str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]],
    ):
        return self._parameter_area.add_parameters(configs)

    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        self._parameter_area.remove_parameter(parameter_name, safe_remove=safe_remove)

    def clear_parameters(self):
        self._parameter_area.clear_parameters()

    def get_parameter_value(self, parameter_name: str) -> Any:
        return self._parameter_area.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        return self._parameter_area.get_parameter_values()

    def set_parameter_value(
        self, parameter_name: str, value: Any, ignore_unknown_parameter: bool = True
    ):
        self._parameter_area.set_parameter_value(
            parameter_name, value, ignore_unknown_parameter
        )

    def set_parameter_values(self, values: Dict[str, Any]) -> List[str]:
        return self._parameter_area.set_parameter_values(values)

    def _create_ui(self):
        super()._create_ui()

        self._center_widget = QWidget(self)
        # noinspection PyArgumentList
        layout_main = QVBoxLayout()
        self._center_widget.setLayout(layout_main)
        self.setCentralWidget(self._center_widget)

        config: FnExecuteWindowConfig = cast(FnExecuteWindowConfig, self._config)

        parameter_area_layout = QVBoxLayout()
        layout_main.addLayout(parameter_area_layout)

        self._parameter_area = ParameterArea(self._center_widget, config, self._bundle)
        parameter_area_layout.addWidget(self._parameter_area)

        self._operation_area = OperationArea(self._center_widget, config)
        self._operation_area.set_cancel_button_visible(self._bundle.fn_info.cancelable)
        self._operation_area.sig_execute_requested.connect(
            self._on_execute_button_clicked
        )
        self._operation_area.sig_clear_requested.connect(self._on_clear_button_clicked)
        self._operation_area.sig_cancel_requested.connect(
            self._on_cancel_button_clicked
        )
        parameter_area_layout.addWidget(self._operation_area)

        self._document_dock = QDockWidget(self)
        self._document_area = DocumentArea(
            self._document_dock, config.document_browser_config
        )
        self._document_dock.setWidget(self._document_area)

        self._output_dock = QDockWidget(self)
        self._output_area = OutputArea(self._output_dock, config.output_browser_config)
        self._output_dock.setWidget(self._output_area)

    # noinspection PyUnresolvedReferences
    def apply_configs(self):
        super().apply_configs()

        self._config: FnExecuteWindowConfig
        fn_info = self._bundle.fn_info

        if self._config.title is None:
            title = fn_info.display_name or ""
        else:
            title = self._config.title
        icon = self._config.icon or fn_info.icon
        icon = get_icon(icon) or QIcon()
        self.setWindowTitle(title)
        self.setWindowIcon(icon)

        self._operation_area.apply_config()
        self._output_area.apply_config()

        self._document_dock.setWindowTitle(self._config.document_dock_title)
        self._document_dock.setVisible(self._config.show_document_dock)
        self._document_dock.setFloating(self._config.document_dock_floating)
        self.set_document(fn_info.document, fn_info.document_format)
        self.addDockWidget(self._config.document_dock_position, self._document_dock)

        # create the dock widget and output area
        self._output_dock.setWindowTitle(self._config.output_dock_title)
        self._output_dock.setVisible(self._config.show_output_dock)
        self._output_dock.setFloating(self._config.output_dock_floating)
        self.addDockWidget(self._config.output_dock_position, self._output_dock)

        if self._config.tabify_docks:
            self.tabifyDockWidget(self._document_dock, self._output_dock)

        # resize the docks
        current_width = self.width()
        current_height = self.height()
        output_dock_ratio = self._config.output_dock_ratio
        output_dock_ratio = min(max(output_dock_ratio, 0.1), 1.0)
        dock_height = int(current_height * output_dock_ratio)
        document_dock_ratio = min(max(self._config.document_dock_ratio, 0.1), 1.0)
        dock_width = int(current_width * document_dock_ratio)
        self.resizeDocks([self._output_dock], [dock_height], Qt.Vertical)
        self.resizeDocks(
            [self._document_dock],
            [dock_width],
            Qt.Horizontal,
        )

    def set_output_dock_visible(self, visible: bool):
        self._config: FnExecuteWindowConfig
        self._config.show_output_dock = visible
        self._output_dock.setVisible(visible)

    def set_document_dock_visible(self, visible: bool):
        self._config: FnExecuteWindowConfig
        self._config.show_document_dock = visible
        self._document_dock.setVisible(visible)

    def set_document_dock_floating(self, floating: bool):
        self._config: FnExecuteWindowConfig
        self._config.document_dock_floating = floating
        self._document_dock.setFloating(floating)

    def set_output_dock_floating(self, floating: bool):
        self._config: FnExecuteWindowConfig
        self._config.output_dock_floating = floating
        self._output_dock.setFloating(floating)

    def tabify_docks(self, tabify: bool):
        self._config: FnExecuteWindowConfig
        self._config.tabify_docks = tabify
        if tabify:
            self.tabifyDockWidget(self._document_dock, self._output_dock)

    def before_execute(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        super().before_execute(fn_info, arguments)
        if self._operation_area.is_clear_checkbox_checked():
            self.clear_output()
        self._operation_area.set_execute_button_enabled(False)
        self._operation_area.set_clear_button_enabled(False)
        self._operation_area.set_cancel_button_enabled(False)
        self._parameter_area.clear_validation_error(None)

    def on_execute_start(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_start(fn_info, arguments)
        self._operation_area.set_cancel_button_enabled(True)

    def on_execute_finish(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_finish(fn_info, arguments)
        self._operation_area.set_execute_button_enabled(True)
        self._operation_area.set_clear_button_enabled(True)
        self._operation_area.set_cancel_button_enabled(False)

    def on_execute_result(
        self, fn_info: FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        self._config: FnExecuteWindowConfig
        if callable(self._bundle.on_execute_result):
            self._bundle.on_execute_result(result, arguments.copy())
            return

        result_str = self._config.function_result_message.format(result)

        if self._config.print_function_result:
            self.append_output(result_str, scroll_to_bottom=True)

        if self._config.show_function_result:
            messagebox.show_info_message(
                self, result_str, title=self._config.result_dialog_title
            )

    def on_execute_error(
        self, fn_info: FnInfo, arguments: Dict[str, Any], error: Exception
    ):

        self._config: FnExecuteWindowConfig
        if isinstance(error, ParameterError):
            self._parameter_area.process_param_error(error)
            del error
            return

        if callable(self._bundle.on_execute_error):
            self._bundle.on_execute_error(error, arguments.copy())
            del error
            return

        error_type = type(error).__name__
        error_msg = self._config.function_error_message.format(error_type, str(error))
        if self._config.print_function_error:
            if not self._config.show_error_traceback:
                self.append_output(error_msg, scroll_to_bottom=True)
            else:
                self.append_output(get_traceback(error) + "\n", scroll_to_bottom=True)

        if self._config.show_function_error:
            if not self._config.show_error_traceback:
                messagebox.show_critical_message(
                    self, error_msg, title=self._config.error_dialog_title
                )
            else:
                messagebox.show_exception_messagebox(
                    self, exception=error, title=self._config.error_dialog_title
                )
        del error

    def _on_close(self) -> bool:
        self._config: FnExecuteWindowConfig
        if self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
            return False
        return super()._on_close()

    def _on_cleanup(self):
        super()._on_cleanup()
        self._parameter_area.clear_parameters()

    def _on_destroy(self):
        super()._on_destroy()
        # noinspection PyProtectedMember
        ucontext._current_window_destroyed()

    def _on_cancel_button_clicked(self):
        self._config: FnExecuteWindowConfig
        if not self._bundle.fn_info.cancelable:
            messagebox.show_warning_message(
                self, self._config.uncancelable_function_message
            )
            return
        if not self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_not_executing_message
            )
        else:
            self._executor.try_cancel()

    def _on_execute_button_clicked(self):
        self._config: FnExecuteWindowConfig
        if self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
            return
        try:
            arguments = self.get_parameter_values()
        except FunctionExecutingError:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
        except ParameterError as e:
            self._parameter_area.process_param_error(e)
        else:
            self._executor.execute(self._bundle.fn_info, arguments)

    # noinspection PyMethodMayBeStatic
    def _on_clear_button_clicked(self):
        self._config: FnExecuteWindowConfig
        if self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
            pass
        self.clear_output()
