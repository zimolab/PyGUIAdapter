import dataclasses
from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QDialogButtonBox,
    QMessageBox,
    QFileDialog,
)

from typing import Optional, Tuple

_DEFAULT_SIZE = (655, 185)


@dataclasses.dataclass
class StringDictItemEditorConfig(object):
    key_label: Optional[str] = None
    value_label: Optional[str] = None
    key_readonly: bool = False
    browse_file_button: bool = True
    browse_file_button_text: str = "Browse File..."
    browse_file_filters: str = ""
    browse_file_start_dir: Optional[str] = None
    browse_file_dialog_title: str = "Browse File"
    browse_dir_button: bool = True
    browse_dir_button_text = "Browse Directory..."
    browse_dir_start_dir: Optional[str] = None
    browse_dir_dialog_title: str = "Browse Directory"
    file_path_as_posix: bool = False

    def as_dict(self):
        return dataclasses.asdict(self)


class StringDictItemEditor(QDialog):

    def __init__(
        self,
        parent: QWidget,
        title: str,
        size: Optional[Tuple[int, int]] = None,
        initial_key: str = "",
        initial_value: str = "",
        *,
        key_label: str = "Key",
        value_label: str = "Value",
        key_readonly: bool = False,
        browse_file_button: bool = True,
        browse_file_button_text: str = "Browse File...",
        browse_file_filters: str = "",
        browse_file_start_dir: Optional[str] = None,
        browse_file_dialog_title: str = "Browse File",
        browse_dir_button: bool = True,
        browse_dir_button_text="Browse Directory...",
        browse_dir_start_dir: Optional[str] = None,
        browse_dir_dialog_title: str = "Browse Directory",
        file_path_as_posix: bool = False,
    ):
        super().__init__(parent)

        self._browse_file_filters = browse_file_filters
        self._browse_file_start_dir = browse_file_start_dir
        self._browse_file_dialog_title = browse_file_dialog_title
        self._browse_dir_start_dir = browse_dir_start_dir
        self._browse_dir_dialog_title = browse_dir_dialog_title
        self._file_path_as_posix = file_path_as_posix

        self._current_key = initial_key
        self._current_value = initial_value

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self._layout.setSpacing(20)

        self._grid_layout = QGridLayout()
        self._layout.addLayout(self._grid_layout)

        self._key_label = QLabel(self)
        self._key_label.setText(key_label)
        self._key_edit = QLineEdit(self)
        self._key_edit.setText(initial_key)
        self._key_edit.setReadOnly(key_readonly)
        self._grid_layout.addWidget(self._key_label, 0, 0)
        self._grid_layout.addWidget(self._key_edit, 0, 1)

        self._value_label = QLabel(self)
        self._value_label.setText(value_label)
        self._value_edit = QLineEdit(self)
        self._value_edit.setText(initial_value)
        self._grid_layout.addWidget(self._value_label, 1, 0)
        self._grid_layout.addWidget(self._value_edit, 1, 1)

        self._button_layout = QHBoxLayout()
        self._layout.addLayout(self._button_layout)

        if browse_file_button:
            self._browse_file_button = QPushButton(self)
            self._browse_file_button.setText(browse_file_button_text)
            self._browse_file_button.clicked.connect(self._on_browse_file)
            self._button_layout.addWidget(self._browse_file_button)

        if browse_dir_button:
            self._browse_dir_button = QPushButton(self)
            self._browse_dir_button.setText(browse_dir_button_text)
            self._browse_dir_button.clicked.connect(self._on_browse_dir)
            self._button_layout.addWidget(self._browse_dir_button)

        self._button_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        self._button_box = QDialogButtonBox(self)
        self._button_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self._button_box.accepted.connect(self._on_accept)
        self._button_box.rejected.connect(self._on_reject)
        self._button_layout.addWidget(self._button_box)

        self._layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        size = size or _DEFAULT_SIZE
        self.resize(*size)
        self.setWindowTitle(title)

        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)

    def get_key_value(self) -> Optional[Tuple[str, str]]:
        ret = self.exec_()
        if ret == QDialog.Accepted:
            return self._current_key, self._current_value
        else:
            return None

    def _update_current_key_value(self):
        self._current_key = self._key_edit.text()
        self._current_value = self._value_edit.text()

    def _on_accept(self):
        self._update_current_key_value()
        if not self._current_key:
            QMessageBox.critical(self, "Error", "Key cannot be empty")
            return
        self.accept()

    def _on_reject(self):
        self.reject()

    def _on_browse_file(self):
        # filename, _ = getopenfilename(
        #     parent=self,
        #     basedir=self._browse_file_start_dir or "",
        #     filters=self._browse_file_filters or "",
        #     caption=self._browse_file_dialog_title,
        # )
        filename, _ = QFileDialog.getOpenFileName(
            self,
            self._browse_file_dialog_title,
            self._browse_file_start_dir or "",
            self._browse_file_filters or "",
        )
        if not filename:
            return
        if self._file_path_as_posix:
            self._value_edit.setText(Path(filename).absolute().as_posix())
        else:
            self._value_edit.setText(filename)

    def _on_browse_dir(self):
        # dir_name = getexistingdirectory(
        #     parent=self,
        #     basedir=self._browse_dir_start_dir or "",
        #     caption=self._browse_dir_dialog_title,
        # )
        dir_name = QFileDialog.getExistingDirectory(
            self,
            self._browse_dir_dialog_title,
            self._browse_dir_start_dir or "",
        )
        if not dir_name:
            return
        if self._file_path_as_posix:
            self._value_edit.setText(Path(dir_name).absolute().as_posix())
        else:
            self._value_edit.setText(dir_name)
