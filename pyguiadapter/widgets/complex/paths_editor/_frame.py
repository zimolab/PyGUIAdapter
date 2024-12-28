import dataclasses
from pathlib import Path
from typing import Optional

from qtpy.QtWidgets import QWidget, QPushButton, QFileDialog

from ._item import PathItemEditorConfig, PathItemEditor
from ..itemsview_base import ListViewFrameBase, ItemEditorBase, ItemsViewFrameConfig


@dataclasses.dataclass
class PathListViewFrameConfig(ItemsViewFrameConfig):
    double_click_to_edit: bool = True
    add_file_button_text: Optional[str] = "Files..."
    add_directory_button_text: Optional[str] = "Folder..."
    filters: str = ""
    start_directory: str = ""
    path_as_posix: bool = False
    file_dialog_title: str = ""
    directory_dialog_title: str = ""
    add_item_editor_title: str = "Add Path"
    edit_item_editor_title: str = "Edit Path"
    path_edit_label_text: str = "Path:"
    path_list_label_text: str = "Paths"
    exit_confirm_message: Optional[str] = "Are you sure you want to exit?"


class PathListViewFrame(ListViewFrameBase):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        config: Optional[PathListViewFrameConfig] = None,
    ):
        self._config = config or PathListViewFrameConfig()
        super().__init__(parent, self._config)

    def create_add_item_editor(self) -> ItemEditorBase:
        item_editor_config = PathItemEditorConfig(
            window_title=self._config.add_item_editor_title,
            file_button_text=self._config.add_file_button_text,
            directory_button_text=self._config.add_directory_button_text,
            file_dialog_title=self._config.file_dialog_title,
            directory_dialog_title=self._config.directory_dialog_title,
            filters=self._config.filters,
            start_directory=self._config.start_directory,
            path_as_posix=self._config.path_as_posix,
            center_container_title=self._config.path_edit_label_text,
        )
        editor = PathItemEditor(self, item_editor_config)
        return editor

    def create_edit_item_editor(self) -> ItemEditorBase:
        item_editor_config = PathItemEditorConfig(
            window_title=self._config.edit_item_editor_title,
            file_button_text=self._config.add_file_button_text,
            directory_button_text=self._config.add_directory_button_text,
            file_dialog_title=self._config.file_dialog_title,
            directory_dialog_title=self._config.directory_dialog_title,
            filters=self._config.filters,
            start_directory=self._config.start_directory,
            path_as_posix=self._config.path_as_posix,
            center_container_title=self._config.path_edit_label_text,
        )
        editor = PathItemEditor(self, item_editor_config)
        return editor

    def _setup_ui(self):
        super()._setup_ui()

        if self._config.double_click_to_edit:
            # noinspection PyUnresolvedReferences
            self.items_view.itemDoubleClicked.connect(self._on_item_double_clicked)

        # create button for adding files
        if self._config.add_file_button_text:
            self._add_file_button = QPushButton(self)
            self._add_file_button.setText(self._config.add_file_button_text)
            # noinspection PyUnresolvedReferences
            self._add_file_button.clicked.connect(self._on_add_file_clicked)
            self.insert_top_widget(0, self._add_file_button)

        # create button for adding directories
        if self._config.add_directory_button_text:
            self._add_directory_button = QPushButton(self)
            self._add_directory_button.setText(self._config.add_directory_button_text)
            # noinspection PyUnresolvedReferences
            self._add_directory_button.clicked.connect(self._on_add_directory_clicked)
            if self._add_file_button:
                self.insert_top_widget_after(
                    self._add_directory_button, self._add_file_button
                )
            else:
                self.insert_top_widget(0, self._add_directory_button)

    def _on_item_double_clicked(self):
        self.on_edit_button_clicked()

    def _on_add_file_clicked(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self._config.file_dialog_title,
            self._config.start_directory,
            self._config.filters,
        )
        if not files:
            return
        for file in files:
            if self._config.path_as_posix:
                file = Path(file).as_posix()
            self.items_view.append_row(file)

    def _on_add_directory_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, self._config.directory_dialog_title, self._config.start_directory
        )
        if not dir_path:
            return
        if self._config.path_as_posix:
            dir_path = Path(dir_path).as_posix()
        self.items_view.append_row(dir_path)
