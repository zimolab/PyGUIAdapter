import dataclasses
from typing import Dict, Any, List, Optional, Tuple, Callable

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QMessageBox,
    QPushButton,
    QWidget,
    QGridLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)

from .common_config import CommonEditorConfig
from .item_editor import BaseScrollableItemEditor
from .itemsview_container import CommonItemsViewContainer, ControlButtonHooks
from .object_tableview import MultiObjectEditView, MultiObjectEditViewConfig
from .schema import ValueType, ValueWidgetMixin

REMOVE_CONFIRM_MESSAGE = "Are you sure you want to remove selected object?"
CLEAR_CONFIRM_MESSAGE = "Are you sure you want to clear all objects?"
NO_OBJECT_SELECTED_WARNING_MESSAGE = "No object selected!"
NO_OBJECT_ADDED_WARNING_MESSAGE = "No object added!"
MULTIPLE_OBJECTS_WARNING_MESSAGE = "Multiple objects selected!"


@dataclasses.dataclass
class MultiObjectEditorConfig(MultiObjectEditViewConfig, CommonEditorConfig):
    fill_missing_keys_with_default: bool = True
    window_title: str = "Objects Editor"
    window_size: Tuple[int, int] = (800, 600)
    stretch_last_section: bool = True
    ignore_unknown_columns: bool = True
    alternating_row_colors: bool = False
    validate_added_object: bool = True
    no_selection_warning_message: Optional[str] = NO_OBJECT_SELECTED_WARNING_MESSAGE
    no_items_warning_message: Optional[str] = NO_OBJECT_ADDED_WARNING_MESSAGE
    remove_confirm_message: Optional[str] = REMOVE_CONFIRM_MESSAGE
    clear_confirm_message: Optional[str] = CLEAR_CONFIRM_MESSAGE
    multiple_selection_warning_message: Optional[str] = MULTIPLE_OBJECTS_WARNING_MESSAGE
    double_click_to_edit: bool = False


class ObjectItemEditor(BaseScrollableItemEditor):

    def __init__(
        self,
        parent: QWidget,
        schema: Dict[str, ValueType],
        config: CommonEditorConfig,
        *,
        accept_hook: Optional[
            Callable[["ObjectItemEditor", Dict[str, Any]], bool]
        ] = None,
        reject_hook: Optional[Callable[["ObjectItemEditor"], bool]] = None,
    ):
        self._schema = schema
        self._config = config

        self._accept_hook = accept_hook
        self._reject_hook = reject_hook

        self._widgets: Dict[str, ValueWidgetMixin] = {}

        super().__init__(parent)

        self._setup_ui()

    def user_bottom_widgets(self) -> List[QWidget]:
        return []

    def set_data(self, data: Dict[str, Any]):
        if not data:
            return
        for key, value in data.items():
            widget = self._widgets.get(key, None)
            if widget:
                widget.set_value(value)

    def get_data(self) -> Dict[str, Any]:
        data = {}
        for key, widget in self._widgets.items():
            data[key] = widget.get_value()
        return data

    def on_create_item_widgets(self, parent: QWidget):
        layout = QGridLayout()
        for i, (key, vt) in enumerate(self._schema.items()):
            edit = vt.create_item_editor_widget(parent)
            if edit is None:
                continue
            label = QLabel(parent)
            label.setText(vt.display_name or key)
            layout.addWidget(
                label,
                i,
                0,
                alignment=self._config.item_editor_key_column_alignment
                or Qt.AlignmentFlag.AlignCenter,
            )
            layout.addWidget(
                edit,
                i,
                1,
                alignment=self._config.item_editor_value_column_alignment
                or Qt.AlignmentFlag.AlignCenter,
            )
            self._widgets[key] = edit
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        parent.setLayout(layout)

    def accept(self):
        if self._accept_hook is None or self._accept_hook(self, self.get_data()):
            super().accept()
            return

    def reject(self):
        if self._reject_hook is None or self._reject_hook(self):
            super().reject()
            return

    def _setup_ui(self):
        if self._config.item_editor_title:
            self.setWindowTitle(self._config.item_editor_title)

        if self._config.item_editor_size:
            self.resize(*self._config.item_editor_size)

        if self._config.item_editor_center_container_title:
            self._center_container.setTitle(
                self._config.item_editor_center_container_title
            )

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)


class MultiObjectEditor(QDialog, ControlButtonHooks):
    def __init__(
        self,
        parent: Optional[QWidget],
        schema: Dict[str, ValueType],
        config: MultiObjectEditorConfig,
        *,
        accept_hook: Optional[
            Callable[["MultiObjectEditor", List[Dict[str, Any]]], bool]
        ] = None,
        reject_hook: Optional[Callable[["MultiObjectEditor"], bool]] = None,
        item_editor_accept_hook: Optional[
            Callable[["ObjectItemEditor", Dict[str, Any]], bool]
        ] = None,
        item_editor_reject_hook: Optional[Callable[["ObjectItemEditor"], bool]] = None,
    ):
        self._config = config
        self._schema = schema
        self._dialog_button_box: Optional[QWidget] = None
        self._accept_hook = accept_hook
        self._reject_hook = reject_hook
        self._item_editor_accept_hook = item_editor_accept_hook
        self._item_editor_reject_hook = item_editor_reject_hook

        super().__init__(parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._objects_view = MultiObjectEditView(self, config, schema)
        self._view_container = CommonItemsViewContainer(
            self, self._objects_view, control_button_hooks=self
        )
        self._layout.addWidget(self._view_container)

        self._setup_ui()

    def set_objects(self, objects: List[Dict[str, Any]]):
        self._objects_view.clear_objects()
        for obj in objects:
            self.add_object(obj)

    def clear_objects(self):
        self._objects_view.clear_objects()

    def get_objects(self) -> List[Dict[str, Any]]:
        return self._objects_view.get_all_objects()

    def add_object(self, obj: Dict[str, Any]):
        if self._config.fill_missing_keys_with_default:
            obj = self.fill_missing_keys_with_default(obj)
        self._objects_view.add_object(obj)

    def insert_object(self, index: int, obj: Dict[str, Any]):
        self._objects_view.insert_object(index, obj)

    def remove_object(self, index: int) -> Dict[str, Any]:
        return self._objects_view.remove_object(index)

    def update_object(self, index: int, obj: Dict[str, Any]):
        self._objects_view.update_object(index, obj)

    def missing_keys(self, obj: Dict[str, Any]) -> List[str]:
        return self._objects_view.missing_keys(obj)

    def fill_missing_keys_with_default(
        self, obj: Dict[str, Any], copy: bool = True
    ) -> Dict[str, Any]:
        return self._objects_view.fill_missing_keys_with_default(obj, copy)

    def on_add_button_clicked(self, source: QPushButton) -> bool:
        item_editor = ObjectItemEditor(
            self,
            self._schema,
            self._config,
            accept_hook=self._item_editor_accept_hook,
            reject_hook=self._item_editor_reject_hook,
        )
        obj, ok = item_editor.start(None)
        item_editor.deleteLater()
        if not ok:
            return True
        self.add_object(obj)
        return True

    def on_edit_button_clicked(self, source: QPushButton) -> bool:
        selected_row = self._check_selected_row()
        if selected_row < 0:
            return True
        item_editor = ObjectItemEditor(
            self,
            self._schema,
            self._config,
            accept_hook=self._item_editor_accept_hook,
            reject_hook=self._item_editor_reject_hook,
        )
        prev = self._objects_view.get_object(selected_row)
        cur, ok = item_editor.start(prev)
        item_editor.deleteLater()
        if not ok:
            return True
        self.update_object(selected_row, cur)
        return True

    def on_remove_button_clicked(self, source: QPushButton) -> bool:
        selected_rows = self._objects_view.get_selected_rows(reverse=True)
        if not selected_rows:
            if self._config.no_selection_warning_message:
                self._show_warning_message(self._config.no_selection_warning_message)
            return True
        if self._config.remove_confirm_message:
            ret = self._show_confirm_message(self._config.remove_confirm_message)
            if ret == QMessageBox.StandardButton.No:
                return True
        self._objects_view.remove_rows(selected_rows)
        return True

    def on_clear_button_clicked(self, source: QPushButton) -> bool:
        if self._objects_view.row_count() <= 0:
            if self._config.no_selection_warning_message:
                self._show_warning_message(self._config.no_items_warning_message)
            return True

        if self._config.clear_confirm_message:
            ret = self._show_confirm_message(self._config.clear_confirm_message)
            if ret == QMessageBox.StandardButton.No:
                return True
        self.clear_objects()
        return True

    def on_move_up_button_clicked(self, source: QPushButton) -> bool:
        row_to_move = self._check_selected_row()
        if row_to_move < 0:
            return True
        self._objects_view.move_row_up(row_to_move, wrap=self._config.wrap_movement)
        return True

    def on_move_down_button_clicked(self, source: QPushButton) -> bool:
        row_to_move = self._check_selected_row()
        if row_to_move < 0:
            return True
        self._objects_view.move_row_down(row_to_move, wrap=self._config.wrap_movement)
        return True

    def accept(self):
        if self._accept_hook is None or self._accept_hook(self, self.get_objects()):
            super().accept()
            return

    def reject(self):
        if self._reject_hook is None or self._reject_hook(self):
            super().reject()
            return

    def _on_item_double_clicked(self, item):
        _ = item
        self.on_edit_button_clicked(self._view_container.edit_button)

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

    def _setup_ui(self):
        if self._config.standard_buttons:
            self._dialog_button_box = QDialogButtonBox(self)
            self._dialog_button_box.setStandardButtons(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.accepted.connect(self.accept)
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.rejected.connect(self.reject)
            self._layout.addWidget(self._dialog_button_box)

        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)

        if self._config.window_size:
            self.resize(*self._config.window_size)

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        if self._config.double_click_to_edit:
            # noinspection PyUnresolvedReferences
            self._objects_view.itemDoubleClicked.connect(self._on_item_double_clicked)

        if self._config.add_button_text:
            self._view_container.add_button.setText(self._config.add_button_text)
        if self._config.edit_button_text:
            self._view_container.edit_button.setText(self._config.edit_button_text)
        if self._config.remove_button_text:
            self._view_container.remove_button.setText(self._config.remove_button_text)
        if self._config.move_up_button_text:
            self._view_container.move_up_button.setText(
                self._config.move_up_button_text
            )
        if self._config.move_down_button_text:
            self._view_container.move_down_button.setText(
                self._config.move_down_button_text
            )
        if self._config.clear_button_text:
            self._view_container.clear_button.setText(self._config.clear_button_text)

        if self._config.center_container_title:
            self._view_container.items_view_box.setTitle(
                self._config.center_container_title
            )

    def _check_selected_row(self) -> int:
        selected_rows = self._objects_view.get_selected_rows(reverse=True)
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
