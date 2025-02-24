from os import PathLike
from pathlib import Path
from typing import List, Tuple, Union, Optional, Any

from qtpy.QtCore import Qt, QPoint, QModelIndex
from qtpy.QtWidgets import (
    QPushButton,
    QWidget,
    QToolButton,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
    QTableWidgetItem,
)

from ._path import (
    SHOW_DIRS_ONLY,
    START_DIRECTORY,
    FILE_FILTERS,
    SELECTED_FILTER,
    AS_POSIX,
    PathDialog,
)
from ..object_tableview import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType
from ..item_editor import BaseItemEditor
from ..tableview import TableView
from ..utils import Widget

DEFAULT_VALUE = ""
WINDOW_TITLE = "Path"
WINDOW_SIZE = (500, 100)
CENTER_CONTAINER_TITLE = ""
FILE_BUTTON_TEXT = "File..."
DIRECTORY_BUTTON_TEXT = "Directory..."
FILE_DIALOG_TITLE = ""
DIRECTORY_DIALOG_TITLE = ""
ANY_FILE = False


class GenericPathDialog(BaseItemEditor, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        window_title: str,
        window_size: Tuple[int, int],
        center_container_title: str,
        file_button_text: str,
        directory_button_text: str,
        file_dialog_title: str,
        directory_dialog_title: str,
        any_file: bool,
        show_dirs_only: bool,
        start_directory: str,
        file_filters: str,
        selected_filter: str,
        as_posix: bool,
    ):
        self._file_button_text = file_button_text
        self._directory_button_text = directory_button_text
        self._window_title = window_title
        self._window_size = window_size
        self._center_container_title = center_container_title
        self._file_dialog_title = file_dialog_title
        self._directory_dialog_title = directory_dialog_title
        self._show_dirs_only = show_dirs_only
        self._start_directory = start_directory
        self._file_filters = file_filters
        self._selected_filter = selected_filter
        self._as_posix = as_posix
        self._any_file = any_file

        self._path_edit: Optional[QLineEdit] = None
        self._browse_file_button: Optional[QPushButton] = None
        self._browse_directory_button: Optional[QPushButton] = None

        self._default_value = None
        self._accepted = False

        super().__init__(parent)

        self._setup_ui()

        self.set_value(default_value)

    def user_bottom_widgets(self) -> List[Widget]:
        buttons = []
        if self._file_button_text:
            self._browse_file_button = QPushButton(self)
            self._browse_file_button.setText(self._file_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_file_button.clicked.connect(self._on_browse_file)
            buttons.append(self._browse_file_button)

        if self._directory_button_text:
            self._browse_directory_button = QPushButton(self)
            self._browse_directory_button.setText(self._directory_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_directory_button.clicked.connect(self._on_browse_directory)
            buttons.append(self._browse_directory_button)

        return buttons

    def accept(self):
        self._accepted = True
        super().accept()

    def reject(self):
        self._accepted = False
        super().reject()

    def set_data(self, data: str):
        self._path_edit.setText(data)

    def get_data(self) -> str:
        return self._path_edit.text()

    def set_value(self, value: str):
        self._accepted = False
        self._default_value = str(value or "")
        self.set_data(self._default_value)

    def get_value(self) -> str:
        if not self._accepted:
            return self._default_value
        return self.get_data()

    def on_create_center_widget(self, parent: QWidget) -> QWidget:
        if not self._path_edit:
            self._path_edit = QLineEdit(parent)
        return self._path_edit

    def _setup_ui(self):
        if self._window_title:
            self.setWindowTitle(self._window_title)

        if self._window_size:
            self.resize(*self._window_size)

        if self._center_container_title:
            self._center_container.setTitle(self._center_container_title)

        # noinspection PyUnresolvedReferences
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        self.setModal(True)

    def _on_browse_file(self):
        file_mode = "any_file" if self._any_file else "existing_file"
        # noinspection PyTypeChecker
        dialog = PathDialog(
            self,
            default_value=self._path_edit.text(),
            title=self._file_dialog_title,
            file_mode=file_mode,
            show_dirs_only=False,
            start_directory=self._start_directory,
            file_filters=self._file_filters,
            selected_filter=self._selected_filter,
            as_posix=self._as_posix,
        )
        ret = dialog.exec_()
        if ret != QFileDialog.Accepted:
            return
        file_path = dialog.get_value()
        self._path_edit.setText(file_path)
        dialog.deleteLater()

    def _on_browse_directory(self):
        dialog = PathDialog(
            self,
            default_value=self._path_edit.text(),
            title=self._directory_dialog_title,
            file_mode="directory",
            show_dirs_only=self._show_dirs_only,
            start_directory=self._start_directory,
            file_filters="",
            selected_filter="",
            as_posix=self._as_posix,
        )
        ret = dialog.exec_()
        if ret != QFileDialog.Accepted:
            return
        dir_path = dialog.get_value()
        self._path_edit.setText(dir_path)
        dialog.deleteLater()


class GenericPathEdit(QWidget, ValueWidgetMixin):

    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: str,
        window_title: str,
        window_size: Tuple[int, int],
        center_container_title: str,
        file_button_text: str,
        directory_button_text: str,
        file_dialog_title: str,
        directory_dialog_title: str,
        any_file: bool,
        show_dirs_only: bool,
        start_directory: str,
        file_filters: str,
        selected_filter: str,
        as_posix: bool,
    ):
        self._window_title = window_title
        self._window_size = window_size
        self._center_container_title = center_container_title
        self._file_button_text = file_button_text
        self._directory_button_text = directory_button_text
        self._file_dialog_title = file_dialog_title
        self._directory_dialog_title = directory_dialog_title
        self._any_file = any_file
        self._show_dirs_only = show_dirs_only
        self._file_filters = file_filters
        self._selected_filter = selected_filter
        self._start_directory = start_directory
        self._as_posix = as_posix

        super().__init__(parent)

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._path_edit = QLineEdit(self)
        self._layout.addWidget(self._path_edit)

        self._browse_button = QToolButton(self)
        self._browse_button.setText("...")
        # noinspection PyUnresolvedReferences
        self._browse_button.clicked.connect(self._on_browse_button_clicked)
        self._layout.addWidget(self._browse_button)

        self.set_value(default_value)

    def set_value(self, value: Any):
        self._path_edit.setText(str(value or ""))

    def get_value(self) -> str:
        return self._path_edit.text()

    def _on_browse_button_clicked(self):
        dialog = GenericPathDialog(
            self,
            default_value=self.get_value(),
            window_title=self._window_title,
            window_size=self._window_size,
            center_container_title=self._center_container_title,
            file_button_text=self._file_button_text,
            directory_button_text=self._directory_button_text,
            file_dialog_title=self._file_dialog_title,
            directory_dialog_title=self._directory_dialog_title,
            any_file=self._any_file,
            show_dirs_only=self._show_dirs_only,
            file_filters=self._file_filters,
            selected_filter=self._selected_filter,
            start_directory=self._start_directory,
            as_posix=self._as_posix,
        )
        ret = dialog.exec_()
        if ret != QFileDialog.Accepted:
            return
        file_path = dialog.get_value()
        self._path_edit.setText(file_path)
        dialog.deleteLater()


class GenericPathValue(ValueType):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        window_title: str = WINDOW_TITLE,
        window_size: Tuple[int, int] = WINDOW_SIZE,
        center_container_title: str = CENTER_CONTAINER_TITLE,
        file_button_text: str = FILE_BUTTON_TEXT,
        directory_button_text: str = DIRECTORY_BUTTON_TEXT,
        file_dialog_title: str = FILE_DIALOG_TITLE,
        directory_dialog_title: str = DIRECTORY_DIALOG_TITLE,
        any_file: bool = ANY_FILE,
        show_dirs_only: bool = SHOW_DIRS_ONLY,
        start_directory: str = START_DIRECTORY,
        file_filters: str = FILE_FILTERS,
        selected_filter: str = SELECTED_FILTER,
        as_posix: bool = AS_POSIX,
        readonly: bool = False,
        hidden: bool = False,
    ):
        self.window_title = window_title
        self.window_size = window_size
        self.center_container_title = center_container_title
        self.file_button_text = file_button_text
        self.directory_button_text = directory_button_text
        self.file_dialog_title = file_dialog_title
        self.directory_dialog_title = directory_dialog_title
        self.show_dirs_only = show_dirs_only
        self.start_directory = start_directory
        self.any_file = any_file
        self.file_filters = file_filters
        self.selected_filter = selected_filter
        self.as_posix = as_posix

        default_value = str(default_value or "")
        super().__init__(
            default_value, display_name=display_name, readonly=readonly, hidden=hidden
        )

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        return isinstance(value, (str, Path, PathLike))

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> GenericPathDialog:
        return GenericPathDialog(
            parent,
            default_value=self.default_value,
            window_title=self.window_title,
            window_size=self.window_size,
            center_container_title=self.center_container_title,
            file_button_text=self.file_button_text,
            directory_button_text=self.directory_button_text,
            file_dialog_title=self.file_dialog_title,
            directory_dialog_title=self.directory_dialog_title,
            any_file=self.any_file,
            show_dirs_only=self.show_dirs_only,
            start_directory=self.start_directory,
            file_filters=self.file_filters,
            selected_filter=self.selected_filter,
            as_posix=self.as_posix,
        )

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> GenericPathEdit:
        return GenericPathEdit(
            parent,
            default_value=self.default_value,
            window_title=self.window_title,
            window_size=self.window_size,
            center_container_title=self.center_container_title,
            file_button_text=self.file_button_text,
            directory_button_text=self.directory_button_text,
            show_dirs_only=self.show_dirs_only,
            file_dialog_title=self.file_dialog_title,
            directory_dialog_title=self.directory_dialog_title,
            start_directory=self.start_directory,
            file_filters=self.file_filters,
            selected_filter=self.selected_filter,
            as_posix=self.as_posix,
            any_file=self.any_file,
        )

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        item.setToolTip(str(value or ""))

    def before_set_editor_data(
        self,
        parent: TableView,
        editor: Union[QWidget, ValueWidgetMixin],
        index: QModelIndex,
    ):
        _ = index  # unused
        if not isinstance(editor, GenericPathDialog):
            return
        if self.window_size:
            editor.resize(*self.window_size)
        global_pos = parent.mapToGlobal(QPoint(0, 0))
        editor.move(
            global_pos.x() + (parent.width() - editor.width()) // 3,
            global_pos.y() + (parent.height() - editor.height()) // 3,
        )
