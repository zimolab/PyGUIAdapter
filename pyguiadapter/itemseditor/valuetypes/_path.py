from os import PathLike
from pathlib import Path
from typing import Optional, Any, Literal

from qtpy.QtWidgets import (
    QLineEdit,
    QToolButton,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QTableWidgetItem,
)

from ..object_tableview import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType, CellWidgetMixin

TITLE = ""
FILE_MODE = "existing_file"
SHOW_DIRS_ONLY = False
START_DIRECTORY = ""
FILE_FILTERS = ""
SELECTED_FILTER = ""
AS_POSIX = False


class PathDialog(QFileDialog, ValueWidgetMixin):

    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: str,
        *,
        title: str = TITLE,
        file_mode: Literal["any_file", "existing_file", "directory"],
        show_dirs_only: bool,
        start_directory: str,
        file_filters: str,
        selected_filter: str,
        as_posix: bool,
    ):
        self._as_posix = as_posix

        super().__init__(parent)

        if file_mode == "any_file":
            self.setFileMode(QFileDialog.AnyFile)
        elif file_mode == "existing_file":
            self.setFileMode(QFileDialog.ExistingFile)
        elif file_mode == "directory":
            self.setFileMode(QFileDialog.Directory)
            self.setOption(QFileDialog.ShowDirsOnly, show_dirs_only)
        else:
            raise ValueError(f"invalid file mode: {file_mode}")

        if title:
            self.setWindowTitle(title)

        if start_directory:
            self.setDirectory(start_directory)

        if file_filters and file_mode != "directory":
            self.setNameFilter(file_filters)
            if selected_filter:
                self.selectNameFilter(selected_filter)

        self.setModal(True)

        self._default_value = None
        self._accepted = False

        self.set_value(default_value)

    def set_value(self, value: str):
        self._accepted = False
        self._default_value = str(value or "")

    def get_value(self) -> str:
        if not self._accepted:
            return self._default_value

        selected = self.selectedFiles()
        if selected:
            value = selected[0]
            if not self._as_posix:
                return value
            return Path(value).as_posix()
        else:
            return self._default_value

    def accept(self):
        self._accepted = True
        super().accept()

    def reject(self):
        self._accepted = False
        super().reject()


# noinspection PyUnresolvedReferences
class PathEdit(QWidget, CellWidgetMixin):
    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: str,
        *,
        title: str = TITLE,
        file_mode: Literal["any_file", "existing_file", "directory"],
        show_dirs_only: bool,
        start_directory: str,
        file_filters: str,
        selected_filter: str,
        as_posix: bool,
    ):
        super().__init__(parent)
        self._default_value = None
        self._title = title
        self._file_mode = file_mode
        self._show_dirs_only = show_dirs_only
        self._start_directory = start_directory
        self._file_filters = file_filters
        self._selected_filter = selected_filter
        self._as_posix = as_posix

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._line_edit = QLineEdit(self)
        self._line_edit.setText(default_value)
        self._layout.addWidget(self._line_edit)

        self._browse_button = QToolButton(self)
        self._browse_button.setText("...")
        self._browse_button.clicked.connect(self._on_browse_button_clicked)
        self._layout.addWidget(self._browse_button)

        self.setLayout(self._layout)

        self.set_value(default_value)

    def _on_browse_button_clicked(self):
        dialog = PathDialog(
            self,
            self._default_value,
            title=self._title,
            file_mode=self._file_mode,
            show_dirs_only=self._show_dirs_only,
            start_directory=self._start_directory,
            file_filters=self._file_filters,
            selected_filter=self._selected_filter,
            as_posix=self._as_posix,
        )
        ret = dialog.exec_()
        if ret != QFileDialog.Accepted:
            return
        path = dialog.get_value()
        self._line_edit.setText(path)
        dialog.deleteLater()

    def get_value(self) -> str:
        return self._line_edit.text()

    def set_value(self, value: str):
        self._default_value = str(value or "")
        self._line_edit.setText(self._default_value)


class PathValue(ValueType):

    def __init__(
        self,
        default_value: str = "",
        *,
        display_name: Optional[str] = None,
        title: str = TITLE,
        file_mode: Literal["any_file", "existing_file", "directory"] = FILE_FILTERS,
        show_dirs_only: bool = SHOW_DIRS_ONLY,
        start_directory: str = START_DIRECTORY,
        file_filters: str = FILE_FILTERS,
        selected_filter: str = SELECTED_FILTER,
        as_posix: bool = AS_POSIX,
    ):
        self.title = title
        self.file_mode = file_mode
        self.show_dirs_only = show_dirs_only
        self.start_directory = start_directory
        self.file_filters = file_filters
        self.selected_filter = selected_filter
        self.as_posix = as_posix

        default_value = str(default_value or "")

        super().__init__(default_value, display_name=display_name)

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        return isinstance(value, (str, Path, PathLike))

    def create_item_editor_widget(self, parent: QWidget, *args, **kwargs) -> PathEdit:
        return PathEdit(
            parent,
            self.default_value,
            title=self.title,
            file_mode=self.file_mode,
            show_dirs_only=self.show_dirs_only,
            start_directory=self.start_directory,
            file_filters=self.file_filters,
            selected_filter=self.selected_filter,
            as_posix=self.as_posix,
        )

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> PathDialog:
        return PathDialog(
            parent,
            self.default_value,
            title=self.title,
            file_mode=self.file_mode,
            show_dirs_only=self.show_dirs_only,
            start_directory=self.start_directory,
            file_filters=self.file_filters,
            selected_filter=self.selected_filter,
            as_posix=self.as_posix,
        )

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        item.setToolTip(str(value or ""))
