import os.path
import os.path
import warnings
from typing import List, Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QTextOption
from PyQt6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
)

from pyguiadapter.adapter.bundle import Callable, DEFAULT_ICON, FunctionBundle
from pyguiadapter.commons import get_icon_file
from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.generated.ui_selection_window import Ui_SelectionWindow
from pyguiadapter.ui.utils import setup_textedit_stylesheet, set_textedit_text
from pyguiadapter.ui.utils import (
    show_critical_dialog,
    show_warning_dialog,
)
from pyguiadapter.ui.window.func_execution import ExecutionWindow
from .config import SelectionWindowConfig
from .constants import (
    DEFAULT_SPLIT_SIZE,
    ERROR_DIALOG_TITLE,
    WARNING_DIALOG_TITLE,
    NO_FUNC_SELECTED_MSG,
)


class SelectionWindow(QMainWindow):
    def __init__(
        self,
        func_bundles: List[Callable],
        config: Optional[SelectionWindowConfig] = None,
        config_execution_window: Optional[WindowConfig] = None,
        callback_window_created: Optional[Callable[[QMainWindow], None]] = None,
        callback_execution_window_created: Optional[
            Callable[[ExecutionWindow], None]
        ] = None,
        parent=None,
    ):

        super().__init__(parent=parent)

        self._func_bundles = [*func_bundles]
        self._config = config or SelectionWindowConfig()
        self._callback_window_created = callback_window_created
        self._ui = Ui_SelectionWindow()

        self._config_execution_window = config_execution_window
        self._callback_execution_window_created = callback_execution_window_created
        self._execution_window: Optional[ExecutionWindow] = None

        self._setup_ui()
        self.window_config = config
        self._setup_func_listwidget()

        if self._callback_window_created is not None:
            self._callback_window_created(self)

    @property
    def window_config(self) -> SelectionWindowConfig:
        return self._config

    @window_config.setter
    def window_config(self, window_config: SelectionWindowConfig):
        if not isinstance(window_config, SelectionWindowConfig):
            raise TypeError(
                f"window_config must be an instance of SelectionWindowConfig, got {type(window_config)}"
            )
        self._config = window_config
        self._config.apply_basic_configs(self)

    def _setup_ui(self):
        self._ui.setupUi(self)

        self._ui.splitter.setSizes(DEFAULT_SPLIT_SIZE)

        if not self._func_bundles:
            self._ui.button_select.setEnabled(False)
        else:
            self._ui.button_select.setEnabled(True)

        self._ui.listwidget_functions.currentItemChanged.connect(
            self._on_current_item_changed
        )

        self._set_view_mode()
        self._setup_document_widget()

        text = self.window_config.func_list_label_text
        if text is not None:
            self._ui.label_func_list.setText(text)

        text = self.window_config.document_label_text
        if text is not None:
            self._ui.label_document.setText(text)

        text = self.window_config.select_button_text
        if text is not None:
            self._ui.button_select.setText(text)

        self._ui.button_select.clicked.connect(self._open_execution_window)
        self._ui.listwidget_functions.itemDoubleClicked.connect(
            self._open_execution_window
        )

    def _on_current_item_changed(self, item: QListWidgetItem):
        if not item:
            self._ui.button_select.setEnabled(False)
            self._ui.textedit_document.setText("")
        else:
            self._ui.button_select.setEnabled(True)
            self._set_document(function=item.data(Qt.ItemDataRole.UserRole))

    def _open_execution_window(self):
        current_item = self._ui.listwidget_functions.currentItem()
        if not current_item:
            show_warning_dialog(
                self, title=WARNING_DIALOG_TITLE, message=NO_FUNC_SELECTED_MSG
            )
            return
        func_bundle = current_item.data(Qt.ItemDataRole.UserRole)
        if self._execution_window is not None:
            self._execution_window.close()
            self._execution_window.deleteLater()
            self._execution_window = None
        try:
            self._execution_window = ExecutionWindow(
                func_bundle=func_bundle,
                config=self._config_execution_window,
                callback_window_created=self._callback_execution_window_created,
                parent=self,
            )
        except BaseException as e:
            show_critical_dialog(self, title=ERROR_DIALOG_TITLE, message=str(e))
        else:
            self._execution_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self._execution_window.show()

    def _set_document(self, function: FunctionBundle):
        text = function.display_document
        set_textedit_text(self._ui.textedit_document, text, function.document_format)

    def _setup_func_listwidget(self):
        self._cleanup_func_listwidget()
        for function in self._func_bundles:
            item = self._create_func_listitem(function)
            self._ui.listwidget_functions.addItem(item)
        self._ui.listwidget_functions.setCurrentRow(0)

    def _cleanup_func_listwidget(self):
        for i in range(self._ui.listwidget_functions.count()):
            self._ui.listwidget_functions.takeItem(0)

    # noinspection PyMethodMayBeStatic
    def _create_func_listitem(self, func: FunctionBundle) -> QListWidgetItem:
        icon_path = get_icon_file(func.display_icon)
        if not os.path.isfile(icon_path):
            warnings.warn(
                f"icon file not found, use default one instead: '{icon_path}'"
            )
            icon_path = get_icon_file(DEFAULT_ICON)
        icon = QIcon(icon_path)
        item = QListWidgetItem(icon, func.display_name)
        item.setData(Qt.ItemDataRole.UserRole, func)
        return item

    def _set_view_mode(self):
        icon_mode = self.window_config.icon_mode
        icon_size = self.window_config.icon_size
        if icon_mode:
            self._ui.listwidget_functions.setViewMode(QListWidget.ViewMode.IconMode)
            if icon_size is not None:
                self._ui.listwidget_functions.setIconSize(QSize(icon_size, icon_size))
        else:
            self._ui.listwidget_functions.setViewMode(QListWidget.ViewMode.ListMode)

    def _setup_document_widget(self):
        setup_textedit_stylesheet(
            self._ui.textedit_document,
            bg_color=self.window_config.document_bg_color,
            text_color=self.window_config.document_text_color,
            font_family=self.window_config.document_font_family,
            font_size=self.window_config.document_font_size,
        )
        self._ui.textedit_document.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self._ui.textedit_document.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._ui.textedit_document.setReadOnly(True)
        self._ui.textedit_document.setOpenExternalLinks(True)
