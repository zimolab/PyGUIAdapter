import dataclasses
from pathlib import Path
from typing import Optional, Any, Union

from qtpy.QtCore import Qt, QModelIndex
from qtpy.QtWidgets import (
    QLineEdit,
    QFileDialog,
    QDialog,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDialogButtonBox,
    QWidget,
    QStyleOptionViewItem,
    QTableWidget,
)

from .base import ValueWidgetMixin, ValueTypeBase, HookType

DEFAULT_VALUE = ""

DEFAULT_FILE_BTN_TEXT = "File"
DEFAULT_DIR_BTN_TEXT = "Folder"

PATH_TYPES = ("file", "dir", "both")
FILE_PATH_TYPE = "file"
DIR_PATH_TYPE = "dir"
BOTH_PATH_TYPE = "both"


@dataclasses.dataclass
class CommonPathConfig(object):
    file_dialog_title: Optional[str] = None
    dir_dialog_title: Optional[str] = None
    filters: Optional[str] = None
    start_dir: Optional[str] = None
    save_mode: bool = False
    detailed_view: bool = False
    as_posix: bool = False
    browse_file_button_text: str = DEFAULT_FILE_BTN_TEXT
    browse_dir_button_text: str = DEFAULT_DIR_BTN_TEXT


class SinglePathTypeSelector(QFileDialog, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        path_type: str,
        *,
        config: Optional[CommonPathConfig] = None,
    ):
        super().__init__(parent)

        self._config = config or CommonPathConfig()

        self._init_value = default_value

        if path_type not in PATH_TYPES:
            raise ValueError(f"invalid path_type: {path_type}")

        self._path_type = path_type

        if path_type == FILE_PATH_TYPE:
            self.setFileMode(QFileDialog.ExistingFile)
        elif path_type == DIR_PATH_TYPE:
            self.setFileMode(QFileDialog.Directory)
        else:
            raise ValueError(f"invalid path_type: {path_type}")

        file_dialog_title = self._config.file_dialog_title or ""
        dir_dialog_title = self._config.dir_dialog_title or ""
        window_title = (
            file_dialog_title if path_type == FILE_PATH_TYPE else dir_dialog_title
        )
        self.setWindowTitle(window_title)

        if self._config.filters is not None:
            self.setNameFilter(self._config.filters)

        if self._config.start_dir is not None and Path(self._config.start_dir).is_dir():
            self.setDirectory(self._config.start_dir)

        if self._config.save_mode:
            self.setAcceptMode(QFileDialog.AcceptSave)

        if self._config.detailed_view:
            self.setViewMode(QFileDialog.Detail)

        self._accepted = False

        self.setModal(True)
        self.setWindowModality(Qt.WindowModal)

    def accept(self):
        self._accepted = True
        super().accept()

    def cast_value(self, original_value: Any) -> str:
        return str(Path(original_value))

    def get_value(self) -> str:
        if self._path_type == DIR_PATH_TYPE and not self._accepted:
            return self._init_value

        selected_files = self.selectedFiles()
        if not selected_files:
            return self._init_value
        selected_file = selected_files[0]
        if self._config.as_posix:
            return Path(selected_file).as_posix()
        return selected_file

    def set_value(self, value: str):
        if value is None:
            value = DEFAULT_VALUE
        if not isinstance(value, str):
            value = self.cast_value(value)
        self._init_value = value


class PathSelect(QWidget, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        path_type: str,
        compact_layout: bool,
        *,
        config: Optional[CommonPathConfig] = None,
    ):
        super().__init__(parent)

        self._config = config or CommonPathConfig()

        self._browse_buttons = []

        if path_type not in PATH_TYPES:
            raise ValueError(f"invalid path_type: {path_type}")

        if path_type == FILE_PATH_TYPE:
            self._browse_file_button = QPushButton(self)
            self._browse_file_button.setText(self._config.browse_file_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_file_button.clicked.connect(self._on_browse_file)
            self._browse_buttons.append(self._browse_file_button)

        elif path_type == DIR_PATH_TYPE:
            self._browse_dir_button = QPushButton(self)
            self._browse_dir_button.setText(self._config.browse_dir_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_dir_button.clicked.connect(self._on_browse_dir)
            self._browse_buttons.append(self._browse_dir_button)
        else:
            self._browse_file_button = QPushButton(self)
            self._browse_file_button.setText(self._config.browse_file_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_file_button.clicked.connect(self._on_browse_file)

            self._browse_dir_button = QPushButton(self)
            self._browse_dir_button.setText(self._config.browse_dir_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_dir_button.clicked.connect(self._on_browse_dir)

            self._browse_buttons.append(self._browse_file_button)
            self._browse_buttons.append(self._browse_dir_button)

        self._layout: Optional[QLayout] = None
        self._edit: QLineEdit = QLineEdit(self)
        self._edit.setText(default_value)

        self._buttons_layout: Optional[QLayout] = None
        if compact_layout:
            self._init_compact_layout()
        else:
            self._init_normal_layout()

    @property
    def buttons_layout(self) -> Optional[QLayout]:
        return self._buttons_layout

    def cast_value(self, original_value: Any) -> str:
        return str(Path(original_value))

    def get_value(self) -> str:
        return self._edit.text()

    def set_value(self, value: str):
        if value is None:
            value = DEFAULT_VALUE
        if not isinstance(value, str):
            value = self.cast_value(value)
        self._edit.setText(value)

    def _init_compact_layout(self):
        self._buttons_layout = None
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._layout.addWidget(self._edit)
        for btn in self._browse_buttons:
            self._layout.addWidget(btn)

    def _init_normal_layout(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._layout.addWidget(self._edit)
        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self._buttons_layout)

        for btn in self._browse_buttons:
            self._buttons_layout.addWidget(btn)

    def _on_browse_file(self):
        file_dialog = SinglePathTypeSelector(
            self,
            default_value=self._edit.text(),
            path_type=FILE_PATH_TYPE,
            config=self._config,
        )
        ret = file_dialog.exec_()
        if ret == QDialog.Accepted:
            self._edit.setText(file_dialog.get_value())
        file_dialog.destroy()
        file_dialog.deleteLater()

    def _on_browse_dir(self):
        dir_dialog = SinglePathTypeSelector(
            self,
            default_value=self._edit.text(),
            path_type=DIR_PATH_TYPE,
            config=self._config,
        )
        ret = dir_dialog.exec_()
        if ret == QDialog.Accepted:
            self._edit.setText(dir_dialog.get_value())
        dir_dialog.destroy()
        dir_dialog.deleteLater()


class BothPathTypeSelector(QDialog):
    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        title: str = "",
        config: Optional[CommonPathConfig] = None,
    ):
        super().__init__(parent)
        self._config = config or CommonPathConfig()
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._current_value = default_value

        self._path_select = PathSelect(
            self,
            default_value=default_value,
            path_type=BOTH_PATH_TYPE,
            compact_layout=False,
            config=self._config,
        )

        self._layout.addWidget(self._path_select)
        self._button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        # noinspection PyUnresolvedReferences
        self._button_box.accepted.connect(self._on_accept)
        # noinspection PyUnresolvedReferences
        self._button_box.rejected.connect(self.rejected)
        self._path_select.buttons_layout.addWidget(self._button_box)

        self.setWindowTitle(title)
        self.setModal(True)

    def _on_accept(self):
        self._current_value = self._path_select.get_value()
        self.accept()

    def get_value(self) -> str:
        return self._current_value

    def set_value(self, value: str):
        self._path_select.set_value(value)
        self._current_value = value


class SinglePathTypeValue(ValueTypeBase):
    def __init__(
        self,
        default_value: str,
        path_type: str,
        *,
        config: Optional[CommonPathConfig] = None,
    ):
        super().__init__(default_value)
        if path_type not in PATH_TYPES:
            raise ValueError(f"invalid path_type: {path_type}")

        self._config = config or CommonPathConfig()
        self._path_type = path_type

    def on_create_editor(
        self,
        parent: QWidget,
        option: Optional[QStyleOptionViewItem],
        index: Optional[QModelIndex],
        **kwargs,
    ) -> QWidget:
        return SinglePathTypeSelector(
            parent,
            default_value=self.default_value,
            path_type=self._path_type,
            config=self._config,
        )

    def on_create_edit(self, parent: QWidget, **kwargs) -> Union[QWidget, QLayout]:
        edit = PathSelect(
            parent,
            default_value=self.default_value,
            path_type=self._path_type,
            compact_layout=True,
            config=self._config,
        )
        return edit


class FilePathValue(SinglePathTypeValue):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        *,
        config: Optional[CommonPathConfig] = None,
    ):

        super().__init__(default_value, path_type=FILE_PATH_TYPE, config=config)


class DirPathValue(SinglePathTypeValue):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        *,
        config: Optional[CommonPathConfig] = None,
    ):
        super().__init__(default_value, path_type=DIR_PATH_TYPE, config=config)


class PathValue(ValueTypeBase):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        path_type: str = BOTH_PATH_TYPE,
        *,
        config: Optional[CommonPathConfig] = None,
    ):
        super().__init__(default_value)
        if path_type not in PATH_TYPES:
            raise ValueError(f"invalid path_type: {path_type}")

        self._config = config or CommonPathConfig()
        self._path_type = path_type

    @property
    def hook_type(self) -> HookType:
        return HookType.CellDoubleClicked

    def on_cell_double_clicked(
        self, parent: QTableWidget, row: int, col: int, **kwargs
    ):
        item = parent.item(row, col)
        if item is None:
            return
        data = item.data(Qt.EditRole)
        dialog = BothPathTypeSelector(
            parent,
            default_value=data or self.default_value,
            config=self._config,
        )
        ret = dialog.exec_()
        if ret == QDialog.Accepted:
            current_value = dialog.get_value()
            item.setData(Qt.EditRole, current_value)
        dialog.destroy()
        dialog.deleteLater()

    def on_create_editor(
        self,
        parent: QWidget,
        option: Optional[QStyleOptionViewItem],
        index: Optional[QModelIndex],
        **kwargs,
    ) -> Optional[QWidget]:
        return None

    def on_create_edit(self, parent: QWidget, **kwargs) -> Union[QWidget, QLayout]:
        edit = PathSelect(
            parent,
            default_value=self.default_value,
            path_type=self._path_type,
            compact_layout=True,
            config=self._config,
        )
        return edit
