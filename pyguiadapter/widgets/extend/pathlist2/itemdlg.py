import dataclasses
from pathlib import Path

from PySide2.QtWidgets import QFileDialog
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QDialogButtonBox,
)
from typing import Optional, Tuple

_DEFAULT_SIZE = (520, 110)


@dataclasses.dataclass(frozen=True)
class PathListItemEditorConfig(object):
    title: str = "Edit Path"
    size: Optional[Tuple[int, int]] = None
    label: str = "Path:"
    browse_file_button: bool = True
    browse_dir_button: bool = True
    browse_file_button_text: str = "Browse File..."
    browse_dir_button_text: str = "Browse Directory..."
    file_dialog_title: str = "Browse File"
    dir_dialog_title: str = "Browse Directory"
    file_filters: str = ""
    start_dir: str = ""
    path_as_posix: bool = False


class PathListItemEditor(QDialog):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        initial_value: Optional[str] = None,
        config: Optional[PathListItemEditorConfig] = None,
    ):
        super().__init__(parent)

        self._current_value = initial_value

        self._config = config or PathListItemEditorConfig()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._layout.addSpacerItem(
            QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        self._edit_layout = QHBoxLayout()
        self._layout.addLayout(self._edit_layout)

        self._label = QLabel(self)
        self._label.setText(self._config.label)
        self._edit_layout.addWidget(self._label)

        self._edit = QLineEdit(self)
        if self._current_value is not None:
            self._edit.setText(self._current_value)
        self._edit_layout.addWidget(self._edit)

        self._buttons_layout = QHBoxLayout()
        self._layout.addLayout(self._buttons_layout)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        if self._config.browse_file_button:
            self._browser_file_button = QPushButton(self)
            self._browser_file_button.setText(self._config.browse_file_button_text)
            self._browser_file_button.clicked.connect(self._on_browser_file)
            self._buttons_layout.addWidget(self._browser_file_button)

        if self._config.browse_dir_button:
            self._browser_dir_button = QPushButton(self)
            self._browser_dir_button.setText(self._config.browse_dir_button_text)
            self._browser_dir_button.clicked.connect(self._on_browser_dir)
            self._buttons_layout.addWidget(self._browser_dir_button)

        self._dlg_buttons_box = QDialogButtonBox(self)
        self._dlg_buttons_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self._dlg_buttons_box.accepted.connect(self._on_ok)
        self._dlg_buttons_box.rejected.connect(self._on_cancel)
        self._buttons_layout.addWidget(self._dlg_buttons_box)

        self.resize(*self._config.size or _DEFAULT_SIZE)
        self.setWindowTitle(self._config.title)
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

    @property
    def current_value(self) -> Optional[str]:
        return self._current_value

    def _on_browser_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            self._config.file_dialog_title,
            self._config.start_dir,
            self._config.file_filters,
        )
        if not filename:
            return
        if self._config.path_as_posix:
            filename = Path(filename).absolute().as_posix()
        self._edit.setText(filename)

    def _on_browser_dir(self):
        dir_name = QFileDialog.getExistingDirectory(
            self, self._config.dir_dialog_title, self._config.start_dir
        )
        if not dir_name:
            return
        if self._config.path_as_posix:
            dir_name = Path(dir_name).absolute().as_posix()
        self._edit.setText(dir_name)

    def _on_ok(self):
        self._current_value = self._edit.text()
        self.accept()

    def _on_cancel(self):
        self.reject()
