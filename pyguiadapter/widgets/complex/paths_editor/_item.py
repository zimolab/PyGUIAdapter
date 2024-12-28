import dataclasses
from pathlib import Path
from typing import Optional, Any, List, Tuple

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLineEdit, QPushButton, QWidget, QFileDialog

from ..commons import Widget, v_line
from ..itemsview_base import ItemEditorBase

DEFAULT_SIZE = (620, 150)


@dataclasses.dataclass
class PathItemEditorConfig(object):
    window_title: str = "Path Editor"
    window_size: Optional[Tuple[int, int]] = DEFAULT_SIZE
    file_button_text: Optional[str] = "File"
    directory_button_text: Optional[str] = "Folder"
    start_directory: str = ""
    filters: str = ""
    file_dialog_title: str = "Select File"
    directory_dialog_title: str = "Select Folder"
    path_as_posix: bool = False
    center_container_title: str = "Path"


class PathItemEditor(ItemEditorBase):
    def __init__(self, parent: QWidget, config: PathItemEditorConfig):
        self._config = config
        self._path_edit: Optional[QLineEdit] = None
        self._browse_file_button: Optional[QPushButton] = None
        self._browse_directory_button: Optional[QPushButton] = None

        super().__init__(
            parent,
            center_container_title=config.center_container_title,
            dialog_button_box=True,
            top_spacer=True,
            bottom_spacer=True,
        )
        self._setup_ui()

    def _setup_ui(self):
        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)
        self.resize(*self._config.window_size or DEFAULT_SIZE)
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

    def user_bottom_widgets(self) -> List[Widget]:
        buttons = []
        if self._config.file_button_text:
            self._browse_file_button = QPushButton(self)
            self._browse_file_button.setText(self._config.file_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_file_button.clicked.connect(self.on_browse_file)
            buttons.append(self._browse_file_button)
        if self._config.directory_button_text:
            self._browse_directory_button = QPushButton(self)
            self._browse_directory_button.setText(self._config.directory_button_text)
            # noinspection PyUnresolvedReferences
            self._browse_directory_button.clicked.connect(self.on_browse_directory)
            buttons.append(self._browse_directory_button)
        if buttons:
            buttons.append(v_line(self))
        return buttons

    def set_data(self, data: Any):
        if data is None:
            data = ""
        self._path_edit.setText(str(data))

    def get_data(self) -> str:
        return self._path_edit.text()

    def on_create_center_widget(self, parent: QWidget) -> QWidget:
        if not self._path_edit:
            self._path_edit = QLineEdit(parent)
        return self._path_edit

    def on_browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self._config.file_dialog_title,
            self._config.start_directory,
            self._config.filters,
        )
        if not file_path:
            return
        if self._config.path_as_posix:
            file_path = Path(file_path).as_posix()
        self._path_edit.setText(file_path)

    def on_browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            self._config.directory_dialog_title,
            self._config.start_directory,
        )
        if not dir_path:
            return
        if self._config.path_as_posix:
            dir_path = Path(dir_path).as_posix()
        self._path_edit.setText(dir_path)
