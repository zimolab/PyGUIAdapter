import dataclasses
import enum
from typing import Any, Tuple

from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QCloseEvent, QTextCursor
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDockWidget,
    QMessageBox,
    QApplication,
)
from function2widgets.widget import BaseParameterWidget

from pyguiadapter.bundle import FunctionBundle
from pyguiadapter.commons import clear_layout, get_widget_factory
from pyguiadapter.executor import FunctionExecutor
from pyguiadapter.interact import uprint
from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.generated.ui_execution_window import Ui_ExecutionWindow
from pyguiadapter.ui.styles import (
    DEFAULT_BG_COLOR,
    DEFAULT_TEXT_COLOR,
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE,
    DEFAULT_DOCUMENT_BG_COLOR,
    DEFAULT_DOCUMENT_TEXT_COLOR,
    DEFAULT_DOCUMENT_FONT_FAMILY,
    DEFAULT_DOCUMENT_FONT_SIZE,
)
from pyguiadapter.ui.utils import setup_textbrowser_stylesheet, set_textbrowser_text


class DockWidgetState(enum.Enum):
    Shown = 0
    Hidden = 1
    Floating = 3


@dataclasses.dataclass
class DockConfig(object):
    title: str | None = None
    state: DockWidgetState = DockWidgetState.Shown
    floating_size: Tuple[int, int] = (400, 600)


@dataclasses.dataclass
class ExecutionWindowConfig(WindowConfig):

    tabify_docks: bool = True
    output_dock_config: DockConfig = DockConfig()
    document_dock_config: DockConfig = DockConfig()

    parameters_groupbox_title: str | None = None
    auto_clear_checkbox_text: str | None = None
    execute_button_text: str | None = None
    clear_button_text: str | None = None

    output_font_family: str = DEFAULT_FONT_FAMILY
    output_font_size: int = DEFAULT_FONT_SIZE
    output_bg_color: str = DEFAULT_BG_COLOR
    output_text_color: str = DEFAULT_TEXT_COLOR

    document_font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
    document_font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    document_bg_color: str = DEFAULT_DOCUMENT_BG_COLOR
    document_text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR

    function_executing_status_text: str | None = None
    function_executed_status_text: str | None = None
    function_execution_error_status_text: str | None = None

    auto_clear_output: bool = True
    show_exception_dialog: bool = True
    show_result_dialog: bool = True
    print_execution_start_info: bool = True
    print_execution_finish_info: bool = True
    print_execution_error_info: bool = True
    print_execution_result: bool = True
    timestamp: bool = True
    time_format: str = "%Y-%m-%d %H:%M:%S"

    def apply_to(self, w: "ExecutionWindow") -> None:
        super().apply_to(w)


class _FunctionExecutionCallbacks(QObject):
    def __init__(self, window: "ExecutionWindow"):
        super().__init__(parent=window)
        self._window = window


class ExecutionWindow(QMainWindow):
    def __init__(
        self,
        function: FunctionBundle,
        window_config: ExecutionWindowConfig = None,
        parent=None,
    ):
        window_config = window_config or ExecutionWindowConfig()

        super().__init__(parent=parent)

        self._function = function
        self._window_config = window_config
        self._ui = Ui_ExecutionWindow()

        self._parameter_widgets: list[BaseParameterWidget] = []

        self._layout_parameter_widgets = QVBoxLayout()

        self._executor: FunctionExecutor | None = None

        self._setup_ui()
        self.window_config = window_config

        self._setup_parameter_widgets()

        uprint.set_print_destination(self.append_output)

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
        self._ui.textbrowser_output.clear()

    def append_output(self, text: str, html: bool = False):
        if text and not html:
            text = f"<pre>{text}</pre>"
        cursor: QTextCursor = self._ui.textbrowser_output.textCursor()
        if text:
            cursor.insertHtml(text)
        cursor.insertHtml("<br>")
        # self._ui.textbrowser_output.ensureCursorVisible()
        # self._ui.textbrowser_output.moveCursor(QTextCursor.MoveOperation.End)

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
        status_text = self.window_config.function_executing_status_text or self.tr(
            "Executing..."
        )
        self.statusBar().showMessage(status_text)

    def _on_function_finished(self):
        if self._executor is not None:
            self._executor.deleteLater()
            self._executor = None
        self._ui.button_clear.setEnabled(True)
        self._ui.button_execute.setEnabled(True)

    def _on_function_error(self, error: BaseException):
        status_text = (
            self.window_config.function_execution_error_status_text or self.tr("Error")
        )
        self.statusBar().showMessage(status_text)
        msg = QApplication.tr(
            f"A exception raised during the execution of function '{self._function.function.__name__}':\n\n {error}"
        )
        if self.window_config.show_exception_dialog:
            QMessageBox.warning(self, self.tr("Error"), msg)

    def _on_function_result(self, result: Any):
        status_text = self.window_config.function_executing_status_text or self.tr(
            "Executed"
        )
        self.statusBar().showMessage(status_text)
        if self.window_config.show_result_dialog:
            QMessageBox.information(
                self,
                QApplication.tr("Finished"),
                QApplication.tr(f"Function executed and the result is:\n  {result}"),
            )

    def _setup_ui(self):
        self._ui.setupUi(self)
        self._layout_parameter_widgets.setParent(self._ui.scrollarea_content)
        self._ui.scrollarea_content.setLayout(self._layout_parameter_widgets)

        self._setup_docks()
        self._set_widgets_text()
        self._set_function_document()

        self._setup_output_textbrowser()
        self._setup_document_textbrowser()

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
            for parameter_description in self._function.function_description.parameters:
                parameter_widget = factory.create_widget_from_description(
                    parameter_description
                )
                self._parameter_widgets.append(parameter_widget)
        except BaseException as e:
            self._cleanup_parameter_widgets()
            raise e

    def _add_parameter_widgets(self):
        for widget in self._parameter_widgets:
            self._layout_parameter_widgets.addWidget(widget)
        spacer_item = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._layout_parameter_widgets.addSpacerItem(spacer_item)

    def _cleanup_parameter_widgets(self):
        for widget in self._parameter_widgets:
            widget.deleteLater()
        self._parameter_widgets.clear()

    def _get_arguments(self) -> dict[str, Any]:
        return {
            param_widget.parameter_name: param_widget.get_value()
            for param_widget in self._parameter_widgets
        }

    def _setup_docks(self):
        self.resizeDocks(
            [self._ui.dockwidget_document, self._ui.dockwidget_output],
            [460, 460],
            Qt.Orientation.Horizontal,
        )
        if self.window_config.tabify_docks:
            self._tabify_docks()
        self._setup_dock(
            self._ui.dockwidget_document, self.window_config.document_dock_config
        )
        self._setup_dock(
            self._ui.dockwidget_output, self.window_config.output_dock_config
        )

        if self._all_docks_closed() or self._all_docks_floating():
            self.resize(460, 600)

    def _tabify_docks(self):
        docks = [self._ui.dockwidget_output, self._ui.dockwidget_document]
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
        set_textbrowser_text(
            self._ui.textbrowser_document, text, self._function.document_format
        )

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

    def _setup_output_textbrowser(self):
        setup_textbrowser_stylesheet(
            self._ui.textbrowser_output,
            bg_color=self.window_config.output_bg_color,
            text_color=self.window_config.output_text_color,
            font_family=self.window_config.output_font_family,
            font_size=self.window_config.output_font_size,
        )

    def _setup_document_textbrowser(self):
        setup_textbrowser_stylesheet(
            self._ui.textbrowser_document,
            bg_color=self.window_config.document_bg_color,
            text_color=self.window_config.document_text_color,
            font_family=self.window_config.document_font_family,
            font_size=self.window_config.document_font_size,
        )
