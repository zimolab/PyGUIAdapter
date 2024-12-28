import dataclasses
from typing import Optional, Tuple, Dict, Union, List, Any

from PyQt5.QtWidgets import QMessageBox
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
    QSpacerItem,
    QSizePolicy,
    QGroupBox,
)

from ...common import CommonParameterWidgetConfig
from .tablewidget import PlainObjectTableWidget
from .valuetypes import ValueTypeBase
from .itemeditor import PlainObjectItemEditor, PlainObjectItemEditorConfig

_DEFAULT_SIZE = (800, 600)


@dataclasses.dataclass(frozen=True)
class PlainObjectListEditorConfig(CommonParameterWidgetConfig):

    object_schema: Dict[str, Union[ValueTypeBase, type, str, None]] = dataclasses.field(
        default_factory=dict
    )

    editor_title: str = ""
    """编辑器的标题"""

    editor_size: Optional[Tuple[int, int]] = None
    """编辑器窗口的大小"""

    object_list_title: str = "Objects"
    """编辑区域的标题"""

    add_button: bool = True
    """是否显示添加对象按钮"""

    add_button_text: str = "Add"
    """添加对象按钮的文本"""

    edit_button: bool = True
    """是否显示编辑对象按钮"""

    edit_button_text: str = "Edit"
    """编辑按钮的文本"""

    remove_button: bool = True
    """是否显示移除对象按钮"""

    remove_button_text: str = "Remove"
    """移除按钮的文本"""

    clear_button: bool = True
    """是否显示清空列表按钮"""

    clear_button_text: str = "Clear"
    """清空按钮的文本"""

    move_up_button: bool = True
    """是否显示上移按钮"""

    move_up_button_text: str = "Up"
    """上移按钮的文本"""

    move_down_button: bool = True
    """是否显示下移按钮"""

    move_down_button_text: str = "Down"
    """下移按钮的文本"""

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

    move_wrapping: bool = True
    """是否允许向上或向下移动时循环到顶或底"""


class PlainObjectListEditor(QDialog):
    def __init__(
        self,
        config: Optional[PlainObjectListEditorConfig],
        parent: Optional[QWidget] = None,
    ):
        if not config.object_schema:
            raise ValueError("schema must be provided")

        super().__init__(parent)
        self._config = config or PlainObjectListEditorConfig()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._main_area = QGroupBox(self)
        self._main_area.setTitle(self._config.object_list_title)
        self._main_area_layout = QHBoxLayout()
        self._main_area.setLayout(self._main_area_layout)
        self._layout.addWidget(self._main_area)

        self._table_widget = PlainObjectTableWidget(
            self._config.object_schema, self._main_area
        )
        self._setup_table_widget()
        self._main_area_layout.addWidget(self._table_widget)

        self._buttons_layout = QVBoxLayout()
        self._main_area_layout.addLayout(self._buttons_layout)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        if self._config.add_button:
            self._add_button = QPushButton(
                self._config.add_button_text, self._main_area
            )
            # noinspection PyUnresolvedReferences
            self._add_button.clicked.connect(self._on_add)
            self._buttons_layout.addWidget(self._add_button)

        if self._config.edit_button:
            self._edit_button = QPushButton(
                self._config.edit_button_text, self._main_area
            )
            # noinspection PyUnresolvedReferences
            self._edit_button.clicked.connect(self._on_edit)
            self._buttons_layout.addWidget(self._edit_button)

        if self._config.remove_button:
            self._remove_button = QPushButton(
                self._config.remove_button_text, self._main_area
            )
            # noinspection PyUnresolvedReferences
            self._remove_button.clicked.connect(self._on_remove)
            self._buttons_layout.addWidget(self._remove_button)

        if self._config.clear_button:
            self._clear_button = QPushButton(
                self._config.clear_button_text, self._main_area
            )
            # noinspection PyUnresolvedReferences
            self._clear_button.clicked.connect(self._on_clear)
            self._buttons_layout.addWidget(self._clear_button)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        if self._config.move_up_button:
            self._up_button = QPushButton(
                self._config.move_up_button_text, self._main_area
            )
            # noinspection PyUnresolvedReferences
            self._up_button.clicked.connect(self._on_move_up)
            self._buttons_layout.addWidget(self._up_button)

        if self._config.move_down_button:
            self._down_button = QPushButton(
                self._config.move_down_button_text, self._main_area
            )
            # noinspection PyUnresolvedReferences
            self._down_button.clicked.connect(self._on_move_down)
            self._buttons_layout.addWidget(self._down_button)

        self._buttons_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self._dlg_button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        # noinspection PyUnresolvedReferences
        self._dlg_button_box.accepted.connect(self._on_ok)
        # noinspection PyUnresolvedReferences
        self._dlg_button_box.rejected.connect(self._on_cancel)
        self._layout.addWidget(self._dlg_button_box)

        self.resize(*self._config.editor_size or _DEFAULT_SIZE)
        self.setWindowTitle(self._config.editor_title)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)

        self._update_button_status()

    def set_objects(
        self, objects: List[Dict[str, Any]], ignore_unknown_keys: bool = False
    ):
        self._table_widget.set_objects(objects, ignore_unknown_keys)
        self._update_button_status()

    def get_objects(self) -> List[Dict[str, Any]]:
        return self._table_widget.objects()

    def _setup_table_widget(self):
        pass

    def _on_add(self):
        item_editor_config = PlainObjectItemEditorConfig(
            object_schema=self._table_widget.get_object_schema(), title="Add Object"
        )
        item_editor = PlainObjectItemEditor(item_editor_config, self)
        item_editor.exec_()

    def _on_remove(self):
        selected_row = self._table_widget.get_selected_row()
        if selected_row < 0:
            if self._config.no_item_selected_message:
                QMessageBox.warning(
                    self,
                    self._config.warning_dialog_title,
                    self._config.no_item_selected_message,
                )
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
        self._table_widget.removeRow(selected_row)

    def _on_clear(self):
        count = self._table_widget.rowCount()
        if count == 0:
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
        self._table_widget.clear_objects()

    def _on_edit(self):
        selected_row = self._table_widget.get_selected_row()
        if selected_row < 0:
            if self._config.no_item_selected_message:
                QMessageBox.warning(
                    self,
                    self._config.warning_dialog_title,
                    self._config.no_item_selected_message,
                )
                return
        current_object = self._table_widget.object_at(selected_row)
        item_editor_config = PlainObjectItemEditorConfig(
            object_schema=self._table_widget.get_object_schema(), title="Edit Object"
        )
        item_editor = PlainObjectItemEditor(item_editor_config, self)
        item_editor.set_object(current_object)
        ret = item_editor.exec_()
        if ret == QDialog.Accepted:
            new_object = item_editor.get_object()
            self._table_widget.update_object(selected_row, new_object)
        item_editor.destroy()
        item_editor.deleteLater()

    def _on_move_up(self):
        selected_row = self._table_widget.get_selected_row()
        if selected_row < 0:
            if self._config.no_item_selected_message:
                QMessageBox.warning(
                    self,
                    self._config.warning_dialog_title,
                    self._config.no_item_selected_message,
                )
                return
        target_row = self._table_widget.move_up(
            selected_row, step=1, wrap=self._config.move_wrapping
        )
        if target_row >= 0:
            self._table_widget.selectRow(target_row)
        self._update_button_status()

    def _on_move_down(self):
        selected_row = self._table_widget.get_selected_row()
        if selected_row < 0:
            if self._config.no_item_selected_message:
                QMessageBox.warning(
                    self,
                    self._config.warning_dialog_title,
                    self._config.no_item_selected_message,
                )
                return
        target_row = self._table_widget.move_down(
            selected_row, step=1, wrap=self._config.move_wrapping
        )
        if target_row >= 0:
            self._table_widget.selectRow(target_row)
        self._update_button_status()

    def _on_ok(self):
        self.accept()

    def _on_cancel(self):
        self.reject()

    def _update_button_status(self):
        pass
