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
from pyguiadapter.ui.utils import setup_text_edit_stylesheet, set_text_edit_text


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

    parameters_groupbox_title: Optional[str] = None
    auto_clear_checkbox_text: Optional[str] = None
    execute_button_text: Optional[str] = None
    clear_button_text: Optional[str] = None

    output_font_family: str = DEFAULT_OUTPUT_FONT_FAMILY
    output_font_size: int = DEFAULT_OUTPUT_FONT_SIZE
    output_bg_color: str = DEFAULT_OUTPUT_BG_COLOR
    output_text_color: str = DEFAULT_OUTPUT_TEXT_COLOR

    document_font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
    document_font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    document_bg_color: str = DEFAULT_DOCUMENT_BG_COLOR
    document_text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR

    auto_clear_output: bool = True

    print_function_result: bool = True
    function_result_message: str = QApplication.tr("Function result returned: {}")
    show_function_result_dialog: bool = True
    function_result_dialog_title: str = QApplication.tr("Function Result")
    function_result_dialog_message: str = QApplication.tr(
        "Function result returned: {}"
    )

    print_function_started_info: bool = True
    function_started_message: str = QApplication.tr("Start to execute function...")

    print_function_finished_info: bool = True
    function_finished_message: str = QApplication.tr("Function finished.")

    show_function_error_dialog: bool = True
    function_error_dialog_title: str = QApplication.tr("Function Exception")
    function_error_dialog_message: str = QApplication.tr(
        "A exception raised during the function execution: {}"
    )
    print_function_error_info: bool = True
    function_error_message: str = QApplication.tr(
        "A exception raised during the function execution: {}"
    )

    timestamp: bool = True
    timestamp_pattern: str = "%Y-%m-%d %H:%M:%S"

    def apply_to(self, w: "ExecutionWindow") -> None:
        super().apply_to(w)


class ExecutionWindow(QMainWindow):
    def __init__(
        self,
        function: FunctionBundle,
        window_config: ExecutionWindowConfig = None,
        created_callback: Callable[["ExecutionWindow"], None] = None,
        parent=None,
    ):
        window_config = window_config or ExecutionWindowConfig()

        super().__init__(parent=parent)

        self._function = function
        self._window_config = window_config
        self._ui = Ui_ExecutionWindow()

        self._parameter_widgets: List[BaseParameterWidget] = []

        self._layout_parameter_widgets = QVBoxLayout()

        self._executor: Optional[FunctionExecutor] = None

        self._created_callback = created_callback

        self._upopup = UPopup(self)

        self._setup_ui()
        self.window_config = window_config

        self._setup_parameter_widgets()

        uprint.set_print_destination(self.append_output)
        upopup.set_current_window(self)

        if self._created_callback is not None:
            self._created_callback(self)

    @property
    def popup(self) -> UPopup:
        return self._upopup

    @property
    def window_config(self) -> ExecutionWindowConfig:
        return self._window_config

    @window_config.setter
    def window_config(self, window_config: ExecutionWindowConfig):
        if not isinstance(window_config, ExecutionWindowConfig):
            raise TypeError(
                f"window_config must be an instance of ExecutionWindowConfig, got {type(window_config)}"
            )
        self._window_config = window_config
        self._window_config.apply_to(self)

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
        # if not text:
        #     self._ui.textedit_output.append("\n")
        # else:
        #     self._ui.textedit_output.append(text)

    def set_parameter_values(
        self, arguments: Dict[str, Any], ignore_exceptions: bool = False
    ):
        if self._is_busy():
            self._alert_busy()
            return
        for widget in self._parameter_widgets:
            parameter_name = widget.parameter_name
            if parameter_name not in arguments:
                continue
            arg = arguments[parameter_name]
            try:
                widget.set_value(arg)
            except BaseException as e:
                msg = QApplication.tr(
                    f"Can not value of of parameter '{parameter_name}'!\n\n  {e}"
                )
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
        self._executor = FunctionExecutor(function=self._function, arguments=arguments)
        self._executor.started.connect(self._on_function_started)
        self._executor.finished.connect(self._on_function_finished)
        self._executor.exception_occurred.connect(self._on_function_error)
        self._executor.result_ready.connect(self._on_function_result)
        self._before_function_execution()
        self._executor.start()

    def closeEvent(self, event: QCloseEvent):
        if self._is_busy():
            self._alert_busy()
            event.ignore()
            return

        self._close_all_docks()
        clear_layout(self._layout_parameter_widgets)
        self._cleanup_parameter_widgets()
        event.accept()

    def _before_function_execution(self):
        self._ui.button_execute.setEnabled(False)
        self._ui.button_clear.setEnabled(False)
        if self._ui.checkbox_auto_clear.isChecked():
            self.clear_output()

    def _on_function_started(self):
        if self.window_config.print_function_started_info:
            if self.window_config.function_started_message:
                message = self.window_config.function_started_message.format(
                    self._function.function.__name__
                )
                self._ulogging_info(message)

    def _on_function_finished(self):
        if self._executor is not None:
            self._executor.deleteLater()
            self._executor = None
        self._ui.button_clear.setEnabled(True)
        self._ui.button_execute.setEnabled(True)
        if self.window_config.print_function_finished_info:
            if self.window_config.function_finished_message:
                message = self.window_config.function_finished_message.format(
                    self._function.function.__name__
                )
                self._ulogging_info(message)

    def _on_function_error(self, error: BaseException):
        if self.window_config.print_function_error_info:
            if self.window_config.function_error_message:
                message = self.window_config.function_error_message.format(str(error))
                self._ulogging_error(message)

        if self.window_config.show_function_error_dialog:
            if self.window_config.function_error_dialog_message:
                title = (
                    self.window_config.function_error_dialog_title
                    or QApplication.tr("Function Exception")
                )
                message = self.window_config.function_error_dialog_message.format(
                    str(error)
                )
                QMessageBox.critical(self, title, message)

    def _on_function_result(self, result: Any):
        result = str(result)
        if self.window_config.print_function_result:
            if self.window_config.function_result_message:
                message = self.window_config.function_result_message.format(result)
                self._ulogging_info(message)

        if self.window_config.show_function_result_dialog:
            if self.window_config.function_result_dialog_message:
                title = (
                    self.window_config.function_result_dialog_title
                    or QApplication.tr("Function Result")
                )
                message = self.window_config.function_result_dialog_message.format(
                    result
                )
                QMessageBox.information(self, title, message)

    def _setup_ui(self):
        self._ui.setupUi(self)
        self._layout_parameter_widgets.setParent(self._ui.scrollarea_content)
        self._ui.scrollarea_content.setLayout(self._layout_parameter_widgets)

        self._setup_docks()
        self._set_widgets_text()
        self._set_function_document()

        self._setup_output_widget()
        self._setup_document_widget()

        self._ui.checkbox_auto_clear.setChecked(
            self.window_config.auto_clear_output is True
        )

        self._ui.button_clear.clicked.connect(self.clear_output)
        self._ui.button_execute.clicked.connect(self.execute_function)

    def _is_busy(self):
        return self._executor is not None and self._executor.isRunning()

    def _alert_busy(self):
        msg = self.tr("A function is already running!")
        QMessageBox.warning(self, self.tr("Error"), msg)

    def _setup_parameter_widgets(self):
        self._cleanup_parameter_widgets()
        clear_layout(self._layout_parameter_widgets)
        self._create_parameter_widgets()
        self._add_parameter_widgets()

    def _create_parameter_widgets(self):
        factory = get_widget_factory()
        try:
            for parameter_info in self._function.function_info.parameters:
                parameter_widget = factory.create_widget_for_parameter(parameter_info)
                self._parameter_widgets.append(parameter_widget)
        except BaseException as e:
            self._cleanup_parameter_widgets()
            raise e

    def _add_parameter_widgets(self):
        for widget in self._parameter_widgets:
            widget.setParent(self._ui.scrollarea_content)
            self._layout_parameter_widgets.addWidget(widget)
        spacer_item = QSpacerItem(
            40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._layout_parameter_widgets.addSpacerItem(spacer_item)

    def _cleanup_parameter_widgets(self):
        for widget in self._parameter_widgets:
            widget.deleteLater()
        self._parameter_widgets.clear()

    def _get_arguments(self) -> Dict[str, Any]:
        return {
            param_widget.parameter_name: param_widget.get_value()
            for param_widget in self._parameter_widgets
        }

    def _setup_docks(self):
        if self.window_config.tabify_docks:
            self._tabify_docks()
        self.resizeDocks(
            [self._ui.dockwidget_document, self._ui.dockwidget_output],
            [460, 460],
            Qt.Orientation.Horizontal,
        )

        self._setup_dock(
            self._ui.dockwidget_document, self.window_config.document_dock_config
        )
        self._setup_dock(
            self._ui.dockwidget_output, self.window_config.output_dock_config
        )

        if self._all_docks_closed() or self._all_docks_floating():
            self.resize(460, 600)

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

    def _set_function_document(self):
        text = self._function.display_document
        text_format = self._function.document_format
        set_text_edit_text(self._ui.textedit_document, text, text_format)

    def _set_widgets_text(self):
        if self.window_config.parameters_groupbox_title is not None:
            self._ui.groupbox_parameters.setWindowTitle(
                self.window_config.parameters_groupbox_title
            )
        if self.window_config.auto_clear_checkbox_text is not None:
            self._ui.checkbox_auto_clear.setText(
                self.window_config.auto_clear_checkbox_text
            )
        if self.window_config.execute_button_text is not None:
            self._ui.button_execute.setText(self.window_config.execute_button_text)
        if self.window_config.clear_button_text is not None:
            self._ui.button_clear.setText(self.window_config.clear_button_text)

    def _setup_output_widget(self):
        setup_text_edit_stylesheet(
            self._ui.textedit_output,
            bg_color=self.window_config.output_bg_color,
            text_color=self.window_config.output_text_color,
            font_family=self.window_config.output_font_family,
            font_size=self.window_config.output_font_size,
        )
        self._ui.textedit_output.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._ui.textedit_output.setReadOnly(True)

    def _setup_document_widget(self):
        setup_text_edit_stylesheet(
            self._ui.textedit_document,
            bg_color=self.window_config.document_bg_color,
            text_color=self.window_config.document_text_color,
            font_family=self.window_config.document_font_family,
            font_size=self.window_config.document_font_size,
        )
        self._ui.textedit_document.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._ui.textedit_document.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self._ui.textedit_document.setReadOnly(True)

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
