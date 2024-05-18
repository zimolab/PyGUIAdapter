import warnings
from typing import Any, Optional, List, Dict, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QTextCursor, QTextOption, QIcon
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDockWidget,
    QTextEdit,
)
from function2widgets.widget import BaseParameterWidget

from pyguiadapter.adapter.bundle import FunctionBundle
from pyguiadapter.adapter.executor import FunctionExecutor
from pyguiadapter.commons import get_param_widget_factory
from pyguiadapter.interact import upopup, uprint, ulogging
from pyguiadapter.progressbar_config import ProgressBarConfig
from pyguiadapter.ui.generated.ui_execution_window import Ui_ExecutionWindow
from pyguiadapter.ui.utils import (
    setup_textedit_stylesheet,
    set_textedit_text,
    clear_layout,
    hide_layout,
)
from .base import BaseExecutionWindow
from .config import DockWidgetState, DockConfig, ExecutionWindowConfig
from .constants import (
    BUSY_MSG,
    BUSY_DIALOG_TITLE,
    DOCK_SIZES,
    SOLE_WINDOW_SIZE,
    ParamInfoType,
)
from .context import ExecutionContext
from .exceptions import (
    SetParameterValueError,
    NoSuchParameterError,
    FunctionNotCancelableError,
    FunctionNotExecutingError,
)


class ExecutionWindow(BaseExecutionWindow):
    def __init__(
        self,
        func_bundle: FunctionBundle,
        config: ExecutionWindowConfig = None,
        callback_window_created: Callable[["ExecutionWindow"], None] = None,
        parent=None,
    ):

        super().__init__(parent=parent)

        self._func_bundle = func_bundle
        self._config = config or ExecutionWindowConfig()
        self._callback_window_created = callback_window_created

        self._ui = Ui_ExecutionWindow()

        self._param_widgets: List[BaseParameterWidget] = []
        self._layout_param_widgets = QVBoxLayout()

        self._executor: Optional[FunctionExecutor] = None
        self._execution_ctx: ExecutionContext = ExecutionContext(self)

        self._setup_ui()
        self._setup_param_widgets()
        self.window_config = config

        self._upopup = upopup.UPopup(self)
        uprint.set_print_destination(self.append_output)
        uprint.set_update_progress_destination(self.update_progressbar)
        uprint.set_update_progressbar_config_destination(self.update_progressbar_config)
        upopup.set_current_window(self)

        self._register_ctx_callable("show_document_dock", self.show_document_dock)
        self._register_ctx_callable("show_output_dock", self.show_output_dock)
        self._register_ctx_callable("hide_document_dock", self.hide_document_dock)
        self._register_ctx_callable("hide_output_dock", self.hide_output_dock)
        self._register_ctx_callable(
            "is_document_dock_visible", self.is_document_dock_visible
        )
        self._register_ctx_callable(
            "is_output_dock_visible", self.is_output_dock_visible
        )

        if self._callback_window_created is not None:
            self._callback_window_created(self)

    @property
    def popup(self) -> upopup.UPopup:
        return self._upopup

    @property
    def window_config(self) -> ExecutionWindowConfig:
        return self._config

    @window_config.setter
    def window_config(self, config: ExecutionWindowConfig):
        if not isinstance(config, ExecutionWindowConfig):
            raise TypeError(f"config must be ExecutionWindowConfig, got {type(config)}")
        self._config = config
        self._config.apply_basic_configs(self)
        # apply some configs defined in the function bundle
        if self._func_bundle.window_title is not None:
            self.setWindowTitle(self._func_bundle.window_title)
        if self._func_bundle.window_icon is not None:
            try:
                icon = QIcon(self._func_bundle.window_icon)
            except BaseException as e:
                warnings.warn(
                    self.tr(f"failed to load icon {self._func_bundle.window_icon}: {e}")
                )
            else:
                self.setWindowIcon(icon)

    def is_func_executing(self):
        return self._executor is not None and self._executor.isRunning()

    def get_func(self) -> Callable:
        return self._func_bundle.func_obj

    def is_func_cancelable(self) -> bool:
        return self._func_bundle.cancelable

    def clear_output(self, force: bool = False):
        if self.is_func_executing() and not force:
            self._alert_busy()
            return
        self._ui.textedit_output.clear()

    def cancel_executing(self):
        if not self._func_bundle.cancelable:
            raise FunctionNotCancelableError("function is not cancelable")
        if not self.is_func_executing():
            raise FunctionNotExecutingError("function is not executing now")
        self._cancel_executing()

    def append_output(self, text: str, html: bool = False):
        if text and not html:
            self._ui.textedit_output.insertPlainText(text)
            return
        cursor: QTextCursor = self._ui.textedit_output.textCursor()
        if text:
            cursor.insertHtml(f"<div>{text}</div>")
        cursor.insertHtml("<br>")
        self._ui.textedit_output.ensureCursorVisible()
        self._ui.textedit_output.moveCursor(QTextCursor.MoveOperation.End)

    def update_progressbar(
        self, current_value: int, progress_info: Optional[str] = None
    ):
        if not self._func_bundle.enable_progressbar:
            warnings.warn("progressbar is not enabled")
            return
        self._ui.progressbar.setValue(current_value)
        if progress_info is None:
            return
        self._ui.label_progressbar_info.setText(progress_info)

    def update_progressbar_config(self, progressbar_config: ProgressBarConfig):
        if not progressbar_config:
            return
        self._ui.progressbar.setRange(
            progressbar_config.min_value, progressbar_config.max_value
        )

        self._ui.progressbar.setInvertedAppearance(
            progressbar_config.inverted_appearance is True
        )

        self._ui.label_progressbar_info.setVisible(
            progressbar_config.show_progressbar_info is True
        )

        self._ui.progressbar.setTextVisible(
            progressbar_config.show_progress_text is True
        )

        if progressbar_config.progress_text_format:
            self._ui.progressbar.setFormat(progressbar_config.progress_text_format)

        if progressbar_config.progress_text_centered is True:
            self._ui.progressbar.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_params_info(self) -> Dict[str, ParamInfoType]:
        return {
            p.name: (p.typename, p.type_extras)
            for p in self._func_bundle.func_info.parameters
        }

    def get_param_values(self) -> Dict[str, Any]:
        return {
            param_widget.parameter_name: param_widget.get_value()
            for param_widget in self._param_widgets
        }

    def get_param_value(self, param_name: str) -> Any:
        param_widget = None
        for widget in self._param_widgets:
            if widget.parameter_name == param_name:
                param_widget = widget
        if param_widget:
            raise NoSuchParameterError(f"no such parameter {param_name}")
        return param_widget.get_value()

    def set_param_value(self, param_name: str, value: Any):
        param_widget = None
        for widget in self._param_widgets:
            if widget.parameter_name == param_name:
                param_widget = widget
        if param_widget:
            raise NoSuchParameterError(f"no such parameter {param_name}")
        return param_widget.set_value(value)

    def set_param_values(
        self, param_values: Dict[str, Any], ignore_exception: bool = False
    ):
        # if self.is_func_executing():
        #     self._alert_busy()
        #     return
        for widget in self._param_widgets:
            param_name = widget.parameter_name
            if param_name not in param_values:
                continue
            arg = param_values[param_name]
            try:
                widget.set_value(arg)
            except BaseException as e:
                msg = self.tr(f"failed to set value for parameter {param_name}: {e}")
                if not ignore_exception:
                    raise SetParameterValueError(msg) from e
                else:
                    warnings.warn(msg)

    @property
    def execution_context(self) -> Any:
        return self._execution_ctx

    def execute_function(self):
        if self.is_func_executing():
            self._alert_busy()
            return
        if self._executor is not None:
            self._executor.deleteLater()
            self._executor = None
        arguments = self.get_param_values()
        self._executor = FunctionExecutor(
            func_bundle=self._func_bundle, arguments=arguments
        )
        self._executor.started.connect(self._on_func_started)
        self._executor.finished.connect(self._on_func_finished)
        self._executor.exception_occurred.connect(self._on_func_error)
        self._executor.result_ready.connect(self._on_func_result)
        self._before_func_execute()
        self._executor.start()

    def closeEvent(self, event: QCloseEvent):
        if self.is_func_executing():
            self._alert_busy()
            event.ignore()
            return

        self._close_all_docks()
        clear_layout(self._layout_param_widgets)
        self._cleanup_param_widgets()
        event.accept()

    def _before_func_execute(self):
        self._ui.button_execute.setEnabled(False)
        self._ui.button_clear.setEnabled(False)
        if self._ui.checkbox_autoclear.isChecked():
            self.clear_output()

    def _on_func_started(self):
        if self._func_bundle.cancelable:
            self._ui.button_cancel.setEnabled(True)

        if self.window_config.print_func_start_msg:
            if self.window_config.func_start_msg:
                msg = self.window_config.func_start_msg.format(
                    self._func_bundle.func_obj.__name__
                )
                self.ulogging_info(msg)

    def _on_func_finished(self):
        if self._func_bundle.cancelable:
            self._ui.button_cancel.setEnabled(False)

        if self._executor is not None:
            self._executor.deleteLater()
            self._executor = None
        self._ui.button_clear.setEnabled(True)
        self._ui.button_execute.setEnabled(True)
        if self.window_config.print_func_finish_msg:
            if self.window_config.func_finish_msg:
                msg = self.window_config.func_finish_msg.format(
                    self._func_bundle.func_obj.__name__
                )
                self.ulogging_info(msg)

    def _on_func_error(self, error: BaseException):
        if self.window_config.print_func_error:
            if self.window_config.func_error_msg:
                msg = self.window_config.func_error_msg.format(str(error))
                self.ulogging_critical(msg)

        if self.window_config.show_func_error_dialog:
            if self.window_config.func_error_dialog_msg:
                title = self.window_config.func_error_dialog_title
                msg = self.window_config.func_error_dialog_msg.format(str(error))
                self.show_critical_dialog(title=title, message=msg)

    def _on_func_result(self, result: Any):
        result = str(result)
        if self.window_config.print_func_result:
            if self.window_config.func_result_msg:
                msg = self.window_config.func_result_msg.format(result)
                self.ulogging_info(msg)

        if self.window_config.show_func_result_dialog:
            if self.window_config.func_result_dialog_msg:
                title = self.window_config.func_result_dialog_title
                msg = self.window_config.func_result_dialog_msg.format(result)
                self.show_info_dialog(title=title, message=msg)

    def _setup_ui(self):
        self._ui.setupUi(self)

        self._layout_param_widgets.setParent(self._ui.scrollarea_content)
        self._ui.scrollarea_content.setLayout(self._layout_param_widgets)

        if self.window_config.param_groupbox_title is not None:
            self._ui.groupbox_params.setTitle(self.window_config.param_groupbox_title)

        if self.window_config.autoclear_checkbox_text is not None:
            self._ui.checkbox_autoclear.setText(
                self.window_config.autoclear_checkbox_text
            )
        self._ui.checkbox_autoclear.setChecked(
            self.window_config.autoclear_output is True
        )

        if self.window_config.execute_button_text is not None:
            self._ui.button_execute.setText(self.window_config.execute_button_text)

        if self.window_config.cancel_button_text is not None:
            self._ui.button_cancel.setText(self.window_config.cancel_button_text)
        if self._func_bundle.cancelable:
            self._ui.button_cancel.show()
            self._ui.button_cancel.setEnabled(False)
            self._ui.button_cancel.clicked.connect(self._cancel_executing)
        else:
            self._ui.button_cancel.hide()
            self._ui.button_cancel.setEnabled(False)

        if self.window_config.clear_button_text is not None:
            self._ui.button_clear.setText(self.window_config.clear_button_text)

        self._setup_docks()
        self._set_func_document()
        self._setup_output_widget()
        self._setup_document_widget()
        self._clear_actions()
        self._setup_menus()
        self._setup_toolbar()
        self._setup_progressbar()

        self._ui.button_clear.clicked.connect(self.clear_output)
        self._ui.button_execute.clicked.connect(self.execute_function)

    def _alert_busy(self):
        self.show_warning_dialog(title=BUSY_DIALOG_TITLE, message=BUSY_MSG)

    def _setup_param_widgets(self):
        self._cleanup_param_widgets()
        clear_layout(self._layout_param_widgets)
        factory = get_param_widget_factory()
        # create param widgets
        try:
            for param_info in self._func_bundle.func_info.parameters:
                param_widget = factory.create_widget_for_parameter(param_info)
                self._param_widgets.append(param_widget)
        except BaseException as e:
            self._cleanup_param_widgets()
            raise e
        # add param widgets to layout
        for widget in self._param_widgets:
            widget.setParent(self._ui.scrollarea_content)
            self._layout_param_widgets.addWidget(widget)
        spacer = QSpacerItem(
            40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._layout_param_widgets.addSpacerItem(spacer)

    def _cleanup_param_widgets(self):
        for widget in self._param_widgets:
            widget.deleteLater()
        self._param_widgets.clear()

    def _setup_docks(self):
        if self.window_config.tabify_docks:
            self._tabify_docks()
        docks = (self._ui.dockwidget_document, self._ui.dockwidget_output)
        self.resizeDocks(docks, DOCK_SIZES, Qt.Orientation.Horizontal)

        self._setup_dock(
            self._ui.dockwidget_document, self.window_config.document_dock_config
        )
        self._setup_dock(
            self._ui.dockwidget_output, self.window_config.output_dock_config
        )

        if self._all_docks_closed() or self._all_docks_floating():
            self.resize(*SOLE_WINDOW_SIZE)

    def _tabify_docks(self):
        docks = [self._ui.dockwidget_document, self._ui.dockwidget_output]
        if self.window_config.tabify_docks:
            self.tabifyDockWidget(*docks)

    def _all_docks_closed(self):
        return (
            self._ui.dockwidget_document.isVisible()
            and self._ui.dockwidget_output.isVisible()
        )

    def _all_docks_floating(self):
        return (
            self._ui.dockwidget_document.isFloating()
            and self._ui.dockwidget_output.isFloating()
        )

    def _close_all_docks(self):
        self._ui.dockwidget_document.close()
        self._ui.dockwidget_output.close()

    @staticmethod
    def _setup_dock(dockwidget: QDockWidget, config: DockConfig):
        if config.title is not None:
            dockwidget.setWindowTitle(config.title)
        if config.state == DockWidgetState.Hidden:
            dockwidget.close()
        elif config.state == DockWidgetState.Floating:
            dockwidget.setFloating(True)
            dockwidget.resize(*config.floating_size)
        else:
            dockwidget.show()

    def _set_func_document(self):
        text = self._func_bundle.display_document
        text_format = self._func_bundle.document_format
        set_textedit_text(
            self._ui.textedit_document,
            text,
            text_format,
            goto_start=self._func_bundle.goto_document_start,
        )

    def _setup_output_widget(self):
        setup_textedit_stylesheet(
            self._ui.textedit_output,
            bg_color=self.window_config.output_bg_color,
            text_color=self.window_config.output_text_color,
            font_family=self.window_config.output_font_family,
            font_size=self.window_config.output_font_size,
        )
        self._ui.textedit_output.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._ui.textedit_output.setReadOnly(True)

    def _setup_document_widget(self):
        setup_textedit_stylesheet(
            self._ui.textedit_document,
            bg_color=self.window_config.document_bg_color,
            text_color=self.window_config.document_text_color,
            font_family=self.window_config.document_font_family,
            font_size=self.window_config.document_font_size,
        )
        self._ui.textedit_document.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._ui.textedit_document.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self._ui.textedit_document.setReadOnly(True)
        self._ui.textedit_document.setOpenExternalLinks(True)

    def _clear_actions(self):
        self._actions.clear()

    def _setup_menus(self):
        self._ui.menubar.clear()
        if not self.window_config.enable_menubar_actions or not self._func_bundle.menus:
            self._ui.menubar.hide()
            return
        self._ui.menubar.show()
        self._create_menus(self._ui.menubar, self._func_bundle.menus)

    def _setup_toolbar(self):
        self._ui.toolbar.clear()
        if (
            not self.window_config.enable_toolbar_actions
            or not self._func_bundle.toolbar_actions
        ):
            self._ui.toolbar.hide()
            return
        self._ui.toolbar.show()
        self._create_toolbar_actions(
            self._ui.toolbar, self._func_bundle.toolbar_actions
        )

    def _setup_progressbar(self):
        if not self._func_bundle.enable_progressbar:
            hide_layout(self._ui.layout_progressbar)
            return
        config = self._func_bundle.progressbar_config or ProgressBarConfig()
        self.update_progressbar_config(config)

    def _cancel_executing(self):
        if not self.is_func_executing():
            title = self.tr("Info")
            msg = self.tr("function is not executing!")
            self.show_info_dialog(title=title, message=msg)
            return
        if self._executor is not None:
            self._executor.cancel_requested.emit()

    def ulogging_info(self, message: str):
        ulogging.info(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )

    def ulogging_critical(self, message):
        ulogging.critical(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )

    def ulogging_fatal(self, message):
        ulogging.fatal(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )

    def ulogging_debug(self, message):
        ulogging.debug(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )

    def ulogging_warning(self, message):
        ulogging.warning(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )

    def show_document_dock(self):
        self._ui.dockwidget_document.show()

    def show_output_dock(self):
        self._ui.dockwidget_output.show()

    def hide_document_dock(self):
        self._ui.dockwidget_document.hide()

    def hide_output_dock(self):
        self._ui.dockwidget_output.hide()

    def is_document_dock_visible(self):
        return self._ui.dockwidget_document.isVisible()

    def is_output_dock_visible(self):
        return self._ui.dockwidget_output.isVisible()
