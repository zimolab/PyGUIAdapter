import dataclasses
import os.path
import warnings

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QMessageBox

from pyguiadapter.adapter.bundle import FunctionBundle, DEFAULT_ICON
from pyguiadapter.commons import get_icon_file
from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.generated.ui_selection_window import Ui_SelectionWindow
from pyguiadapter.ui.styles import (
    DEFAULT_DOCUMENT_FONT_FAMILY,
    DEFAULT_DOCUMENT_FONT_SIZE,
    DEFAULT_DOCUMENT_BG_COLOR,
    DEFAULT_DOCUMENT_TEXT_COLOR,
)
from pyguiadapter.ui.utils import setup_textbrowser_stylesheet, set_textbrowser_text
from pyguiadapter.ui.window.execution import ExecutionWindow


@dataclasses.dataclass
class SelectionWindowConfig(WindowConfig):
    icon_mode: bool = True
    icon_size: int | None = 48
    functions_label_text: str | None = None
    document_label_text: str | None = None
    select_button_text: str | None = None

    document_font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
    document_font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    document_bg_color: str = DEFAULT_DOCUMENT_BG_COLOR
    document_text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR

    def apply_to(self, w: "SelectionWindow") -> None:
        super().apply_to(w)


class SelectionWindow(QMainWindow):
    def __init__(
        self,
        functions: list[FunctionBundle],
        window_config: SelectionWindowConfig | None = None,
        execution_window_config: WindowConfig | None = None,
        parent=None,
    ):

        window_config = window_config or SelectionWindowConfig()

        super().__init__(parent=parent)

        self._functions = [*functions]
        self._window_config = window_config
        self._execution_window_config = execution_window_config

        self._ui = Ui_SelectionWindow()

        self._execution_window: ExecutionWindow | None = None

        self._setup_ui()
        self.window_config = window_config

        self._setup_functions_listwidget()

    @property
    def window_config(self) -> SelectionWindowConfig:
        return self._window_config

    @window_config.setter
    def window_config(self, window_config: SelectionWindowConfig):
        if not isinstance(window_config, SelectionWindowConfig):
            raise TypeError(
                f"window_config must be an instance of SelectionWindowConfig, got {type(window_config)}"
            )
        self._window_config = window_config
        self._window_config.apply_to(self)

    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)

    def _setup_ui(self):
        self._ui.setupUi(self)

        self._ui.splitter.setSizes([200, 300])

        if not self._functions:
            self._ui.button_select.setEnabled(False)
        else:
            self._ui.button_select.setEnabled(True)

        self._ui.listwidget_functions.currentItemChanged.connect(
            self._on_current_item_changed
        )

        self._set_view_mode()
        self._setup_document_textbrowser()

        self._set_functions_label_text()
        self._set_document_label_text()
        self._set_select_button_text()

        self._ui.button_select.clicked.connect(self._on_open_execution_window)

    def _on_current_item_changed(self, item: QListWidgetItem):
        if not item:
            self._ui.button_select.setEnabled(False)
            self._ui.textbrowser_document.setText("")
        else:
            self._ui.button_select.setEnabled(True)
            self._set_function_document(function=item.data(Qt.ItemDataRole.UserRole))

    def _on_open_execution_window(self):
        current_item = self._ui.listwidget_functions.currentItem()
        if not current_item:
            QMessageBox.warning(
                self, self.tr("Warn"), self.tr("please select a function first!")
            )
            return
        function = current_item.data(Qt.ItemDataRole.UserRole)
        if self._execution_window is not None:
            self._execution_window.close()
            self._execution_window.deleteLater()
            self._execution_window = None
        try:
            self._execution_window = ExecutionWindow(
                function=function,
                window_config=self._execution_window_config,
                parent=self,
            )
        except BaseException as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))
        else:
            self._execution_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self._execution_window.show()

    def _set_function_document(self, function: FunctionBundle):
        text = function.display_document
        set_textbrowser_text(
            self._ui.textbrowser_document, text, function.document_format
        )

    def _setup_functions_listwidget(self):
        self._cleanup_functions_listwidget()
        for function in self._functions:
            item = self._create_function_list_item(function)
            self._ui.listwidget_functions.addItem(item)
        self._ui.listwidget_functions.setCurrentRow(0)

    def _cleanup_functions_listwidget(self):
        for i in range(self._ui.listwidget_functions.count()):
            self._ui.listwidget_functions.takeItem(0)

    # noinspection PyMethodMayBeStatic
    def _create_function_list_item(self, function: FunctionBundle) -> QListWidgetItem:
        icon_path = get_icon_file(function.display_icon)
        if not os.path.isfile(icon_path):
            warnings.warn(
                f"icon file not found, use default one instead: '{icon_path}'"
            )
            icon_path = get_icon_file(DEFAULT_ICON)
        icon = QIcon(icon_path)
        item = QListWidgetItem(icon, function.display_name)
        item.setData(Qt.ItemDataRole.UserRole, function)
        return item

    def _set_functions_label_text(self):
        text = self.window_config.functions_label_text
        if text is not None:
            self._ui.label_functions.setText(text)

    def _set_document_label_text(self):
        text = self.window_config.document_label_text
        if text is not None:
            self._ui.label_document.setText(text)

    def _set_select_button_text(self):
        text = self.window_config.select_button_text
        if text is not None:
            self._ui.button_select.setText(text)

    def _set_view_mode(self):
        icon_mode = self.window_config.icon_mode
        icon_size = self.window_config.icon_size
        if icon_mode:
            self._ui.listwidget_functions.setViewMode(QListWidget.ViewMode.IconMode)
            if icon_size is not None:
                self._ui.listwidget_functions.setIconSize(QSize(icon_size, icon_size))
        else:
            self._ui.listwidget_functions.setViewMode(QListWidget.ViewMode.ListMode)

    def _setup_document_textbrowser(self):
        setup_textbrowser_stylesheet(
            self._ui.textbrowser_document,
            bg_color=self.window_config.document_bg_color,
            text_color=self.window_config.document_text_color,
            font_family=self.window_config.document_font_family,
            font_size=self.window_config.document_font_size,
        )
