import dataclasses
import enum
from typing import Any, Tuple, Callable, Optional, List, Dict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QTextCursor, QTextOption
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDockWidget,
    QMessageBox,
    QApplication,
    QTextEdit,
)
from function2widgets.widget import BaseParameterWidget

from pyguiadapter.adapter.bundle import FunctionBundle
from pyguiadapter.adapter.executor import FunctionExecutor
from pyguiadapter.commons import clear_layout, get_widget_factory
from pyguiadapter.interact import uprint, upopup, ulogging
from pyguiadapter.interact.upopup import UPopup
from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.generated.ui_execution_window import Ui_ExecutionWindow
from pyguiadapter.ui.styles import (
    DEFAULT_OUTPUT_BG_COLOR,
    DEFAULT_OUTPUT_TEXT_COLOR,
    DEFAULT_OUTPUT_FONT_FAMILY,
    DEFAULT_OUTPUT_FONT_SIZE,
    DEFAULT_DOCUMENT_BG_COLOR,
    DEFAULT_DOCUMENT_TEXT_COLOR,
    DEFAULT_DOCUMENT_FONT_FAMILY,
    DEFAULT_DOCUMENT_FONT_SIZE,
)
from pyguiadapter.ui.utils import setup_textedit_stylesheet, set_textedit_text

FUNC_RESULT_MSG = QApplication.tr("function result: {}")
FUNC_RESULT_DIALOG_TITLE = QApplication.tr("Function Result")
FUNC_START_MSG = QApplication.tr("function execution started")
FUNC_FINISH_MSG = QApplication.tr("function execution finished")
FUNC_ERROR_MSG = QApplication.tr("function execution error: {}")
FUNC_ERROR_DIALOG_TITLE = QApplication.tr("Function Execution Error")
BUSY_MSG = QApplication.tr("A function is already running!")
BUSY_DIALOG_TITLE = QApplication.tr("Busy")

DOCK_SIZES = (460, 460)

SOLE_WINDOW_SIZE = (460, 600)


class DockWidgetState(enum.Enum):
    Shown = 0
    Hidden = 1
    Floating = 3


@dataclasses.dataclass
class DockConfig(object):
    title: Optional[str] = None
    state: DockWidgetState = DockWidgetState.Shown
    floating_size: Tuple[int, int] = dataclasses.field(default=(400, 600))


@dataclasses.dataclass
class ExecutionWindowConfig(WindowConfig):

    tabify_docks: bool = True
    output_dock_config: DockConfig = DockConfig()
    document_dock_config: DockConfig = DockConfig()

    autoclear_output: bool = True

    param_groupbox_title: Optional[str] = None
    autoclear_checkbox_text: Optional[str] = None
    execute_button_text: Optional[str] = None
    clear_button_text: Optional[str] = None
    cancel_button_text: Optional[str] = None

    output_font_family: str = DEFAULT_OUTPUT_FONT_FAMILY
    output_font_size: int = DEFAULT_OUTPUT_FONT_SIZE
    output_bg_color: str = DEFAULT_OUTPUT_BG_COLOR
    output_text_color: str = DEFAULT_OUTPUT_TEXT_COLOR

    document_font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
    document_font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    document_bg_color: str = DEFAULT_DOCUMENT_BG_COLOR
    document_text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR

    print_func_result: bool = True
    func_result_msg: str = FUNC_RESULT_MSG
    show_func_result_dialog: bool = True
    func_result_dialog_title: str = FUNC_RESULT_DIALOG_TITLE
    func_result_dialog_msg: str = FUNC_RESULT_MSG

    print_func_start_msg: bool = True
    func_start_msg: str = FUNC_START_MSG

    print_func_finish_msg: bool = True
    func_finish_msg: str = FUNC_FINISH_MSG

    show_func_error_dialog: bool = True
    func_error_dialog_title: str = FUNC_ERROR_DIALOG_TITLE
    func_error_dialog_msg: str = FUNC_ERROR_MSG
    print_func_error: bool = True
    func_error_msg: str = FUNC_ERROR_MSG

    timestamp: bool = True
    timestamp_pattern: str = "%Y-%m-%d %H:%M:%S"


class ExecutionWindow(QMainWindow):
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

        self._setup_ui()
        self._setup_param_widgets()
        self.window_config = config

        self._upopup = UPopup(self)
        uprint.set_print_destination(self.append_output)
        upopup.set_current_window(self)

        if self._callback_window_created is not None:
            self._callback_window_created(self)

    @property
    def popup(self) -> UPopup:
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

    def clear_output(self, force: bool = False):
        if self._is_busy() and not force:
            self._alert_busy()
            return
        self._ui.textedit_output.clear()

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

    def set_param_values(
        self, arguments: Dict[str, Any], ignore_exceptions: bool = False
    ):
        if self._is_busy():
            self._alert_busy()
            return
        for widget in self._param_widgets:
            param_name = widget.parameter_name
            if param_name not in arguments:
                continue
            arg = arguments[param_name]
            try:
                widget.set_value(arg)
            except BaseException as e:
                msg = QApplication.tr(f"can not set parameter '{param_name}'!\n\n  {e}")
                QMessageBox.critical(self, QApplication.tr("Error"), msg)
                if not ignore_exceptions:
                    break

    def execute_function(self):
        if self._is_busy():
            self._alert_busy()
            return
        if self._executor is not None:
            self._executor.deleteLater()
            self._executor = None
        arguments = self._get_arguments()
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
        if self._is_busy():
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
                self._ulogging_info(msg)

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
                self._ulogging_info(msg)

    def _on_func_error(self, error: BaseException):
        if self.window_config.print_func_error:
            if self.window_config.func_error_msg:
                msg = self.window_config.func_error_msg.format(str(error))
                self._ulogging_error(msg)

        if self.window_config.show_func_error_dialog:
            if self.window_config.func_error_dialog_msg:
                title = self.window_config.func_error_dialog_title
                msg = self.window_config.func_error_dialog_msg.format(str(error))
                QMessageBox.critical(self, title, msg)

    def _on_func_result(self, result: Any):
        result = str(result)
        if self.window_config.print_func_result:
            if self.window_config.func_result_msg:
                msg = self.window_config.func_result_msg.format(result)
                self._ulogging_info(msg)

        if self.window_config.show_func_result_dialog:
            if self.window_config.func_result_dialog_msg:
                title = self.window_config.func_result_dialog_title
                msg = self.window_config.func_result_dialog_msg.format(result)
                QMessageBox.information(self, title, msg)

    def _setup_ui(self):
        self._ui.setupUi(self)

        self._layout_param_widgets.setParent(self._ui.scrollarea_content)
        self._ui.scrollarea_content.setLayout(self._layout_param_widgets)

        if self.window_config.param_groupbox_title is not None:
            self._ui.groupbox_params.setWindowTitle(
                self.window_config.param_groupbox_title
            )

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
            self._ui.button_cancel.clicked.connect(self._on_cancel_requested)
        else:
            self._ui.button_cancel.hide()
            self._ui.button_cancel.setEnabled(False)

        if self.window_config.clear_button_text is not None:
            self._ui.button_clear.setText(self.window_config.clear_button_text)

        self._setup_docks()
        self._set_func_document()
        self._setup_output_widget()
        self._setup_document_widget()

        self._ui.button_clear.clicked.connect(self.clear_output)
        self._ui.button_execute.clicked.connect(self.execute_function)

    def _is_busy(self):
        return self._executor is not None and self._executor.isRunning()

    def _alert_busy(self):
        QMessageBox.warning(self, BUSY_DIALOG_TITLE, BUSY_MSG)

    def _setup_param_widgets(self):
        self._cleanup_param_widgets()
        clear_layout(self._layout_param_widgets)
        self._create_param_widgets()
        self._add_param_widgets()

    def _create_param_widgets(self):
        factory = get_widget_factory()
        try:
            for param_info in self._func_bundle.func_info.parameters:
                param_widget = factory.create_widget_for_parameter(param_info)
                self._param_widgets.append(param_widget)
        except BaseException as e:
            self._cleanup_param_widgets()
            raise e

    def _add_param_widgets(self):
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

    def _get_arguments(self) -> Dict[str, Any]:
        return {
            param_widget.parameter_name: param_widget.get_value()
            for param_widget in self._param_widgets
        }

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
        set_textedit_text(self._ui.textedit_document, text, text_format)

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

    def _on_cancel_requested(self):
        if not self._is_busy():
            msg = self.tr("No function is in execution now!")
            title = self.tr("Info")
            QMessageBox.information(self, title, msg)
            return
        if self._executor is not None:
            self._executor.cancel_requested.emit()

    def _ulogging_info(self, message: str):
        ulogging.info(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )

    def _ulogging_error(self, message):
        ulogging.critical(
            message,
            timestamp=self.window_config.timestamp,
            timestamp_pattern=self.window_config.timestamp_pattern,
        )
