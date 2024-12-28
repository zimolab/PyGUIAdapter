import dataclasses
from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QDialogButtonBox,
    QSpacerItem,
    QSizePolicy,
    QGroupBox,
)
from qtpy.compat import getopenfilename, getopenfilenames, getexistingdirectory
from typing import Optional, Tuple, List

from .itemdlg import PathItemEditorConfig, PathItemEditor
from ...common import CommonParameterWidgetConfig

_DEFAULT_SIZE = (600, 515)


@dataclasses.dataclass(frozen=True)
class PathListEditorConfig(CommonParameterWidgetConfig):

    editor_title: str = ""
    """路径列表编辑器的标题"""

    editor_size: Optional[Tuple[int, int]] = None
    """路径列表编辑器窗口的大小"""

    file_list_title: str = "Paths"
    """路径列表区域的标题"""

    add_file: bool = True
    """是否开启添加文件功能"""

    add_dir: bool = True
    """是否开启添加文件夹功能"""

    pick_multiple_paths: bool = True
    """是否允许选择多个文件或文件夹"""

    add_file_button_text: str = "Add File"
    """添加文件按钮的文本"""

    file_filters: str = ""
    """文件过滤器，用于选择文件对话框"""

    add_dir_button_text: str = "Add Directory"
    """添加文件夹按钮的文本"""

    start_dir: str = ""
    """文件对话框的初始目录"""

    path_as_posix: bool = True
    """是否将选择的文件或文件夹的路径以 Posix 格式保存"""

    edit_button_text: str = "Edit"
    """编辑按钮的文本"""

    remove_button_text: str = "Remove"
    """移除按钮的文本"""

    clear_button_text: str = "Clear"
    """清空按钮的文本"""

    up_button_text: str = "Up"
    """上移按钮的文本"""

    down_button_text: str = "Down"
    """下移按钮的文本"""

    file_dialog_title: str = "Select File"
    """选择文件对话框的标题"""

    dir_dialog_title: str = "Select Directory"
    """选择文件夹对话框的标题"""

    confirm_dialog_title: str = "Confirm"
    """确认对话框的标题"""

    warning_dialog_title: str = "Warning"
    """警告对话框的标题"""

    error_dialog_title: str = "Error"
    """错误对话框的标题"""

    confirm_clear_message: Optional[str] = (
        "Are you sure to remove all items from the list?"
    )
    """清空文件列表的确认消息文本，如果为 None 则不显示确认消息，直接清空文件列表"""

    confirm_remove_message: Optional[str] = (
        "Are you sure to remove the selected item from the list?"
    )
    """移除当前选中项的确认消息文本，如果为 None 则不显示确认消息，直接移除当前选中项"""

    no_item_selected_message: Optional[str] = "No item selected!"
    """没有选中任何项时的提示消息"""

    no_items_added_message: Optional[str] = "No items added!"
    """没有添加任何项时的提示消息"""

    double_click_to_edit: bool = True
    """是否允许双击列表项进行编辑"""

    # grid_line: bool = True
    # """是否显示网格线"""

    # persistent_editor: bool = True
    # """是否使用持久化编辑器"""

    item_editor_config: Optional[PathItemEditorConfig] = None
    """路径列表项编辑器的配置"""


class PathListEditor(QDialog):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        config: Optional[PathListEditorConfig] = None,
    ):
        super().__init__(parent)
        self._config = config or PathListEditorConfig()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._main_area = QGroupBox(self)
        self._main_area.setTitle(self._config.file_list_title)
        self._main_area_layout = QHBoxLayout()
        self._main_area.setLayout(self._main_area_layout)
        self._layout.addWidget(self._main_area)

        self._list_widget = QListWidget(self._main_area)
        self._setup_list_widget()
        self._main_area_layout.addWidget(self._list_widget)

        self._buttons_layout = QVBoxLayout()
        self._main_area_layout.addLayout(self._buttons_layout)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        if self._config.add_file:
            self._add_file_button = QPushButton(
                self._config.add_file_button_text, self._main_area
            )
            self._add_file_button.clicked.connect(self._on_add_file)
            self._buttons_layout.addWidget(self._add_file_button)

        if self._config.add_dir:
            self._add_dir_button = QPushButton(
                self._config.add_dir_button_text, self._main_area
            )
            self._add_dir_button.clicked.connect(self._on_add_dir)
            self._buttons_layout.addWidget(self._add_dir_button)

        self._edit_button = QPushButton(self._config.edit_button_text, self._main_area)
        self._edit_button.clicked.connect(self._on_edit)
        self._buttons_layout.addWidget(self._edit_button)

        self._remove_button = QPushButton(
            self._config.remove_button_text, self._main_area
        )
        self._remove_button.clicked.connect(self._on_remove)
        self._buttons_layout.addWidget(self._remove_button)

        self._clear_button = QPushButton(
            self._config.clear_button_text, self._main_area
        )
        self._clear_button.clicked.connect(self._on_clear)
        self._buttons_layout.addWidget(self._clear_button)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self._up_button = QPushButton(self._config.up_button_text, self._main_area)
        self._up_button.clicked.connect(self._on_move_up_item)
        self._buttons_layout.addWidget(self._up_button)

        self._down_button = QPushButton(self._config.down_button_text, self._main_area)
        self._down_button.clicked.connect(self._on_move_down_item)
        self._buttons_layout.addWidget(self._down_button)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self._dlg_button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self._dlg_button_box.accepted.connect(self._on_ok)
        self._dlg_button_box.rejected.connect(self._on_cancel)
        self._layout.addWidget(self._dlg_button_box)

        self.resize(*self._config.editor_size or _DEFAULT_SIZE)
        self.setWindowTitle(self._config.editor_title)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)

        self._update_button_status()

    def _setup_list_widget(self):
        self._list_widget.setSelectionMode(QListWidget.SingleSelection)
        self._list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        if self._config.double_click_to_edit:
            self._list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)

        # if self._config.persistent_editor:
        #     self._list_widget.currentItemChanged.connect(self._on_current_item_changed)

    @property
    def path_list(self) -> List[str]:
        return [
            self._list_widget.item(i).text() for i in range(self._list_widget.count())
        ]

    @path_list.setter
    def path_list(self, value: List[str]):
        self._clear_items()
        for path in value:
            self._add_item(path)

    def _on_add_file(self):
        if self._config.pick_multiple_paths:
            paths, _ = getopenfilenames(
                self,
                caption=self._config.file_dialog_title,
                basedir=self._config.start_dir,
                filters=self._config.file_filters,
            )
            if not paths:
                return
        else:
            path, _ = getopenfilename(
                self,
                caption=self._config.file_dialog_title,
                basedir=self._config.start_dir,
                filters=self._config.file_filters,
            )
            if not path:
                return
            paths = [path] if path else []
        for path in paths:
            if self._config.path_as_posix:
                path = Path(path).absolute().as_posix()
            self._add_item(path)
        self._update_button_status()

    def _on_add_dir(self):
        path = getexistingdirectory(
            self,
            caption=self._config.dir_dialog_title,
            basedir=self._config.start_dir,
        )
        if not path:
            return
        if self._config.path_as_posix:
            path = Path(path).absolute().as_posix()
        self._add_item(path)
        self._update_button_status()

    def _on_remove(self):
        selected_index = self._check_selected_index()
        if selected_index < 0:
            return
        if self._config.confirm_remove_message:
            ret = QMessageBox.question(
                self,
                self._config.confirm_dialog_title,
                self._config.confirm_remove_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if ret != QMessageBox.Yes:
                return
        self._remove_item(selected_index)
        self._update_button_status()

    def _on_clear(self):
        if not self._list_widget.count():
            if self._config.no_items_added_message:
                QMessageBox.warning(
                    self,
                    self._config.warning_dialog_title,
                    self._config.no_items_added_message,
                )
            return

        if self._config.confirm_clear_message:
            ret = QMessageBox.question(
                self,
                self._config.confirm_dialog_title,
                self._config.confirm_clear_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if ret != QMessageBox.Yes:
                return
        self._clear_items()
        self._update_button_status()

    def _on_edit(self):
        selected_index = self._check_selected_index()
        if selected_index < 0:
            return
        selected_item = self._list_widget.item(selected_index)
        self._edit_item(selected_item.text(), selected_index)
        self._update_button_status()

    def _on_move_up_item(self):
        selected_index = self._check_selected_index()
        if selected_index < 0:
            return
        # already at the top
        if selected_index == 0:
            return

        current_item = self._list_widget.item(selected_index)
        current_item_text = current_item.text()

        prev_index = selected_index - 1
        prev_item = self._list_widget.item(prev_index)
        prev_item_text = prev_item.text()

        current_item.setText(prev_item_text)
        prev_item.setText(current_item_text)

        self._list_widget.setItemSelected(prev_item, True)
        self._update_button_status()

    def _on_move_down_item(self):
        selected_index = self._check_selected_index()
        if selected_index < 0:
            return
        # already at the bottom
        if selected_index == self._list_widget.count() - 1:
            return

        current_item = self._list_widget.item(selected_index)
        current_item_text = current_item.text()

        next_index = selected_index + 1
        next_item = self._list_widget.item(next_index)
        next_item_text = next_item.text()

        current_item.setText(next_item_text)
        next_item.setText(current_item_text)

        self._list_widget.setItemSelected(next_item, True)
        self._update_button_status()

    def _on_selection_changed(self):
        self._update_button_status()

    def _on_item_double_clicked(self, item: QListWidgetItem):
        # if (
        #     self._config.persistent_editor
        #     and not self._list_widget.isPersistentEditorOpen(item)
        # ):
        #     self._list_widget.openPersistentEditor(item)
        #     return

        if not item:
            return
        index = self._list_widget.row(item)
        if index < 0:
            return
        self._edit_item(item.text(), index)
        self._update_button_status()

    def _on_current_item_changed(
        self, current: QListWidgetItem, previous: QListWidgetItem
    ):
        # if self._config.persistent_editor:
        #     if previous and self._list_widget.isPersistentEditorOpen(previous):
        #         self._list_widget.closePersistentEditor(previous)
        #     if current and self._list_widget.isPersistentEditorOpen(current):
        #         self._list_widget.closePersistentEditor(current)
        pass

    def _add_item(self, item_text: str):
        item = QListWidgetItem(item_text, self._list_widget)
        self._list_widget.addItem(item)

    def _update_item(self, index: int, new_value: str):
        item = self._list_widget.item(index)
        item.setText(new_value)

    def _remove_item(self, index: int):
        item = self._list_widget.takeItem(index)
        if item is not None:
            self._list_widget.removeItemWidget(item)
            del item

    def _clear_items(self):
        indices = sorted(range(self._list_widget.count()), reverse=True)
        for index in indices:
            self._remove_item(index)

    def _edit_item(self, item: str, index: int):
        item_editor_config = self._config.item_editor_config or PathItemEditorConfig(
            browse_file_button=self._config.add_file,
            browse_dir_button=self._config.add_dir,
            file_filters=self._config.file_filters,
            start_dir=self._config.start_dir,
            file_dialog_title=self._config.file_dialog_title,
            dir_dialog_title=self._config.dir_dialog_title,
            path_as_posix=self._config.path_as_posix,
        )
        item_editor = PathItemEditor(
            self, initial_value=item, config=item_editor_config
        )
        ret = item_editor.exec_()
        if ret == QDialog.Accepted:
            new_value = item_editor.current_value
            self._update_item(index, new_value)
            self._update_button_status()

        item_editor.destroy()
        item_editor.deleteLater()

    def _on_ok(self):
        self.accept()

    def _on_cancel(self):
        self.reject()

    def _update_button_status(self):
        selected_indexes = self._list_widget.selectedIndexes()
        selected_index = -1 if not selected_indexes else selected_indexes[0].row()
        self._edit_button.setEnabled(selected_index >= 0)
        self._remove_button.setEnabled(selected_index >= 0)

        is_first_item = selected_index == 0
        self._up_button.setEnabled(selected_index >= 0 and not is_first_item)

        is_last_item = selected_index == self._list_widget.count() - 1
        self._down_button.setEnabled(selected_index >= 0 and not is_last_item)

    def _check_index(self, index: int):
        if index < 0 or index >= self._list_widget.count():
            raise IndexError(
                f'index out of range: {index}, allowed range: [0, {self._list_widget.count()})")'
            )

    def _check_selected_index(self) -> int:
        selected_indexes = self._list_widget.selectedIndexes()
        if not selected_indexes:
            if self._config.no_item_selected_message:
                QMessageBox.warning(
                    self,
                    self._config.warning_dialog_title,
                    self._config.no_item_selected_message,
                )
                return -1
        return selected_indexes[0].row()
