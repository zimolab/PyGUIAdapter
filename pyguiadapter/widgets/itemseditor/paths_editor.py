import dataclasses
from pathlib import Path
from typing import Optional, Tuple, List, Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QDialogButtonBox,
    QLineEdit,
    QListWidgetItem,
)

from .common_config import CommonEditorConfig
from .item_editor import BaseItemEditor
from .itemsview_container import CommonItemsViewContainer, ControlButtonHooks
from .listview import ListView, ListViewConfig

REMOVE_CONFIRM_MESSAGE = "Are you sure you want to remove selected path?"
CLEAR_CONFIRM_MESSAGE = "Are you sure you want to clear all paths?"
DUPLICATE_WARNING_MESSAGE = "Duplicate path: {}"
NO_PATH_SELECTED_WARNING_MESSAGE = "No path selected!"
NO_PATH_ADDED_WARNING_MESSAGE = "No path added!"
MULTIPLE_PATH_WARNING_MESSAGE = "Multiple paths selected!"

WARNING_DIALOG_TITLE = "Warning"
CONFIRM_DIALOG_TITLE = "Confirm"


@dataclasses.dataclass
class PathsEditorConfig(ListViewConfig, CommonEditorConfig):
    add_file_button_text: Optional[str] = "File..."
    add_directory_button_text: Optional[str] = "Folder..."
    file_filters: str = ""
    start_directory: str = ""
    file_dialog_title: str = ""
    directory_dialog_title: str = ""
    as_posix: bool = False
    allow_duplicates: bool = True
    window_size: Tuple[int, int] = (800, 600)
    standard_buttons: bool = True
    warning_dialog_title: str = WARNING_DIALOG_TITLE
    confirm_dialog_title: str = CONFIRM_DIALOG_TITLE
    duplicate_items_warning_message: Optional[str] = DUPLICATE_WARNING_MESSAGE
    no_selection_warning_message: Optional[str] = NO_PATH_SELECTED_WARNING_MESSAGE
    no_items_warning_message: Optional[str] = NO_PATH_ADDED_WARNING_MESSAGE
    remove_confirm_message: Optional[str] = REMOVE_CONFIRM_MESSAGE
    clear_confirm_message: Optional[str] = CLEAR_CONFIRM_MESSAGE
    multiple_selection_warning_message: Optional[str] = MULTIPLE_PATH_WARNING_MESSAGE
    window_title: str = "Paths Editor"
    center_container_title: str = ""
    item_editor_title: str = ""
    item_editor_size: Tuple[int, int] = (620, 150)
    item_editor_center_container_title: str = ""
    double_click_to_edit: bool = True
    wrap_movement: bool = False


class PathItemEditor(BaseItemEditor):

    def __init__(self, parent: QWidget, config: PathsEditorConfig):
        self._config = config

        self._path_edit: Optional[QLineEdit] = None
        self._browse_file_button: Optional[QPushButton] = None
        self._browse_directory_button: Optional[QPushButton] = None

        super().__init__(parent)

        self._setup_ui()

    def user_bottom_widgets(self) -> List[QWidget]:
        buttons = []
        if self._config.add_file_button_text:
            self._browse_file_button = QPushButton(self)
            self._browse_file_button.setText(self._config.add_file_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_file_button.clicked.connect(self._on_browse_file)
            buttons.append(self._browse_file_button)

        if self._config.add_directory_button_text:
            self._browse_directory_button = QPushButton(self)
            self._browse_directory_button.setText(
                self._config.add_directory_button_text
            )
            # noinspection PyUnresolvedReferences
            self._browse_directory_button.clicked.connect(self._on_browse_directory)
            buttons.append(self._browse_directory_button)

        return buttons

    def set_data(self, data: str):
        data = data or ""
        self._path_edit.setText(str(data))

    def get_data(self) -> str:
        return self._path_edit.text()

    def on_create_center_widget(self, parent: QWidget) -> QWidget:
        if not self._path_edit:
            self._path_edit = QLineEdit(parent)
        return self._path_edit

    def _setup_ui(self):
        if self._config.item_editor_title:
            self.setWindowTitle(self._config.item_editor_title)
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        if self._config.item_editor_size:
            self.resize(*self._config.item_editor_size)

        if self._config.item_editor_center_container_title:
            self._center_container.setTitle(
                self._config.item_editor_center_container_title
            )

    def _on_browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self._config.file_dialog_title,
            self._config.start_directory,
            self._config.file_filters,
        )
        if not file_path:
            return
        if self._config.as_posix:
            file_path = Path(file_path).as_posix()
        self._path_edit.setText(file_path)

    def _on_browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            self._config.directory_dialog_title,
            self._config.start_directory,
        )
        if not dir_path:
            return
        if self._config.as_posix:
            dir_path = Path(dir_path).as_posix()
        self._path_edit.setText(dir_path)


class PathsEditor(QDialog, ControlButtonHooks):
    def __init__(self, parent: Optional[QWidget], config: PathsEditorConfig):
        super().__init__(parent)

        if not config.allow_duplicates:
            config.item_editable = False

        self._config = config

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._path_listview = ListView(None, config)
        self._view_container = CommonItemsViewContainer(
            self, self._path_listview, control_button_hooks=self
        )
        self._layout.addWidget(self._view_container)

        self._add_file_button: Optional[QPushButton] = None
        self._add_directory_button: Optional[QPushButton] = None

        self._setup_ui()

    def set_paths(self, paths: List[str]):
        self.clear_paths()
        for path in paths:
            self.add_path(path)

    def get_paths(self) -> List[str]:
        return self._path_listview.get_all_row_data()

    def add_path(self, path: str) -> bool:
        if self._config.allow_duplicates:
            self._path_listview.append_row(path)
            return True
        if self.contains_path(path):
            return False
        self._path_listview.append_row(path)
        return True

    def remove_path(self, path: str) -> bool:
        for row in range(self._path_listview.row_count()):
            data = self._path_listview.get_row_data(row)
            if data == path:
                self._path_listview.remove_row(row)
                return True
        return False

    def clear_paths(self):
        self._path_listview.remove_all_rows()

    def contains_path(self, path: str) -> bool:
        return path in self.get_paths()

    def on_add_button_clicked(self, source: QPushButton) -> bool:
        return True

    def on_edit_button_clicked(self, source: QPushButton) -> bool:
        selected_rows = self._path_listview.get_selected_rows(reverse=True)
        if len(selected_rows) < 1:
            if self._config.no_selection_warning_message:
                self._show_warning_message(self._config.no_selection_warning_message)
            return True
        if len(selected_rows) > 1:
            if self._config.multiple_selection_warning_message:
                self._show_warning_message(
                    self._config.multiple_selection_warning_message
                )
            return True
        item_editor = PathItemEditor(self, self._config)
        prev = self._path_listview.get_row_data(selected_rows[0])
        cur, ok = item_editor.start(prev)
        item_editor.deleteLater()
        if not ok or cur == prev:
            return True
        if not self._config.allow_duplicates and self.contains_path(cur):
            if self._config.duplicate_items_warning_message:
                self._show_warning_message(
                    self._config.duplicate_items_warning_message.format(cur)
                )
            return True
        self._path_listview.set_row_data(selected_rows[0], cur)
        return True

    def on_remove_button_clicked(self, source: QPushButton) -> bool:
        selected_rows = self._path_listview.get_selected_rows(reverse=True)
        if not selected_rows:
            if self._config.no_selection_warning_message:
                self._show_warning_message(self._config.no_selection_warning_message)
            return True
        if self._config.remove_confirm_message:
            ret = self._show_confirm_message(self._config.remove_confirm_message)
            if ret == QMessageBox.StandardButton.No:
                return True
        self._path_listview.remove_rows(selected_rows)
        return True

    def on_clear_button_clicked(self, source: QPushButton) -> bool:
        if self._path_listview.row_count() <= 0:
            if self._config.no_items_warning_message:
                self._show_warning_message(self._config.no_items_warning_message)
            return True

        if self._config.clear_confirm_message:
            ret = self._show_confirm_message(self._config.clear_confirm_message)
            if ret == QMessageBox.StandardButton.No:
                return True
        self.clear_paths()
        return True

    def on_move_up_button_clicked(self, source: QPushButton) -> bool:
        row_to_move = self._check_movement()
        if row_to_move < 0:
            return True
        self._path_listview.move_row_up(row_to_move, wrap=self._config.wrap_movement)
        return True

    def on_move_down_button_clicked(self, source: QPushButton) -> bool:
        row_to_move = self._check_movement()
        if row_to_move < 0:
            return True
        self._path_listview.move_row_down(row_to_move, wrap=self._config.wrap_movement)
        return True

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()

    def _show_warning_message(
        self, message: str, buttons: QMessageBox.StandardButton = QMessageBox.Ok
    ) -> Any:
        return QMessageBox.warning(
            self, self._config.warning_dialog_title, message, buttons
        )

    def _show_confirm_message(
        self,
        message: str,
        buttons: QMessageBox.StandardButton = QMessageBox.Yes | QMessageBox.No,
    ) -> Any:
        return QMessageBox.question(
            self, self._config.confirm_dialog_title, message, buttons
        )

    def _on_add_file_button_clicked(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            self._config.file_dialog_title,
            self._config.start_directory,
            self._config.file_filters,
        )
        if not filenames:
            return
        for filename in filenames:
            if self._config.as_posix:
                filename = Path(filename).as_posix()
            ok = self.add_path(filename)
            if not ok and self._config.duplicate_items_warning_message:
                ret = self._show_warning_message(
                    self._config.duplicate_items_warning_message.format(filename),
                    QMessageBox.Ignore | QMessageBox.Abort,
                )
                if ret == QMessageBox.StandardButton.Abort:
                    break

    def _on_add_directory_button_clicked(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            self._config.directory_dialog_title,
            self._config.start_directory,
        )
        if not directory:
            return
        if self._config.as_posix:
            directory = Path(directory).as_posix()
        ok = self.add_path(directory)
        if not ok and self._config.duplicate_items_warning_message:
            self._show_warning_message(
                self._config.duplicate_items_warning_message.format(directory)
            )

    def _on_item_double_clicked(self, item: QListWidgetItem):
        _ = item
        self.on_edit_button_clicked(self._view_container.edit_button)

    def _update_control_button_states(self):
        selected_rows = self._path_listview.get_selected_rows()
        self._view_container.edit_button.setEnabled(len(selected_rows) == 1)
        self._view_container.remove_button.setEnabled(len(selected_rows) > 0)
        self._view_container.move_up_button.setEnabled(len(selected_rows) == 1)
        self._view_container.move_down_button.setEnabled(len(selected_rows) == 1)

    def _setup_ui(self):
        self._view_container.add_button.hide()
        if self._config.standard_buttons:
            self._dialog_button_box = QDialogButtonBox(self)
            self._dialog_button_box.setStandardButtons(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.accepted.connect(self.on_accept)
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.rejected.connect(self.on_reject)
            self._layout.addWidget(self._dialog_button_box)

        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)

        if self._config.window_size:
            self.resize(*self._config.window_size)

        if self._config.add_file_button_text:
            self._add_file_button = QPushButton()
            self._add_file_button.setText(self._config.add_file_button_text)
            # noinspection PyUnresolvedReferences
            self._add_file_button.clicked.connect(self._on_add_file_button_clicked)
            self._view_container.insert_control_widget_after(
                self._add_file_button, self._view_container.add_button
            )

        if self._config.add_directory_button_text:
            self._add_directory_button = QPushButton()
            self._add_directory_button.setText(self._config.add_directory_button_text)
            # noinspection PyUnresolvedReferences
            self._add_directory_button.clicked.connect(
                self._on_add_directory_button_clicked
            )
            self._view_container.insert_control_widget_after(
                self._add_directory_button,
                self._add_file_button or self._view_container.add_button,
            )

        if self._config.double_click_to_edit:
            # noinspection PyUnresolvedReferences
            self._path_listview.itemDoubleClicked.connect(self._on_item_double_clicked)

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

    def _check_movement(self) -> int:
        selected_rows = self._path_listview.get_selected_rows(reverse=True)
        if len(selected_rows) < 1:
            if self._config.no_selection_warning_message:
                self._show_warning_message(self._config.no_selection_warning_message)
            return -1
        if len(selected_rows) > 1:
            if self._config.multiple_selection_warning_message:
                self._show_warning_message(
                    self._config.multiple_selection_warning_message
                )
            return -1
        return selected_rows[0]
