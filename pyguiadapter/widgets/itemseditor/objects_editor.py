import dataclasses
from typing import Optional, Tuple, Dict, Any, List

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QDialogButtonBox,
    QMessageBox,
    QPushButton,
)

from .itemsview_container import CommonItemsViewContainer, ControlButtonHooks
from .item_editor import BaseScrollableItemEditor
from .object_tableview import MultiObjectEditView, MultiObjectEditViewConfig
from .object_tableview.schema import ValueType


REMOVE_CONFIRM_MESSAGE = "Are you sure you want to remove selected object?"
CLEAR_CONFIRM_MESSAGE = "Are you sure you want to clear all objects?"
NO_OBJECT_SELECTED_WARNING_MESSAGE = "No object selected!"
NO_OBJECT_ADDED_WARNING_MESSAGE = "No object added!"
MULTIPLE_OBJECTS_WARNING_MESSAGE = "Multiple objects selected!"

WARNING_DIALOG_TITLE = "Warning"
CONFIRM_DIALOG_TITLE = "Confirm"


@dataclasses.dataclass
class MultiObjectEditorConfig(MultiObjectEditViewConfig):
    window_title: str = "Objects Editor"
    window_size: tuple = (800, 600)
    standard_buttons: bool = True
    warning_dialog_title: str = WARNING_DIALOG_TITLE
    confirm_dialog_title: str = CONFIRM_DIALOG_TITLE
    no_object_selected_warning_message: Optional[str] = (
        NO_OBJECT_SELECTED_WARNING_MESSAGE
    )
    no_object_added_warning_message: Optional[str] = NO_OBJECT_ADDED_WARNING_MESSAGE
    remove_confirm_message: Optional[str] = REMOVE_CONFIRM_MESSAGE
    clear_confirm_message: Optional[str] = CLEAR_CONFIRM_MESSAGE
    multiple_objects_warning_message: Optional[str] = MULTIPLE_OBJECTS_WARNING_MESSAGE
    center_container_title: str = ""
    item_editor_title: str = ""
    item_editor_size: Tuple[int, int] = (620, 150)
    item_editor_center_container_title: str = ""
    double_click_to_edit: bool = True
    wrap_movement: bool = False
    stretch_last_section: bool = True
    ignore_unknown_columns: bool = True
    fill_missing_keys_with_default: bool = True


class MultiObjectEditor(QDialog, ControlButtonHooks):
    def __init__(
        self,
        parent: Optional[QWidget],
        schema: Dict[str, ValueType],
        config: MultiObjectEditorConfig,
    ):
        self._config = config
        self._schema = schema
        self._dialog_button_box: Optional[QWidget] = None

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
        return super().on_add_button_clicked(source)

    def on_edit_button_clicked(self, source: QPushButton) -> bool:
        return super().on_edit_button_clicked(source)

    def on_remove_button_clicked(self, source: QPushButton) -> bool:
        selected_rows = self._objects_view.get_selected_rows(reverse=True)
        if not selected_rows:
            if self._config.no_object_selected_warning_message:
                self._show_warning_message(
                    self._config.no_object_selected_warning_message
                )
            return True
        if self._config.remove_confirm_message:
            ret = self._show_confirm_message(self._config.remove_confirm_message)
            if ret == QMessageBox.StandardButton.No:
                return True
        self._objects_view.remove_rows(selected_rows)
        return True

    def on_clear_button_clicked(self, source: QPushButton) -> bool:
        if self._objects_view.row_count() <= 0:
            if self._config.no_object_selected_warning_message:
                self._show_warning_message(
                    self._config.no_object_selected_warning_message
                )
            return True

        if self._config.clear_confirm_message:
            ret = self._show_confirm_message(self._config.clear_confirm_message)
            if ret == QMessageBox.StandardButton.No:
                return True
        self.clear_objects()
        return True

    def on_move_up_button_clicked(self, source: QPushButton) -> bool:
        row_to_move = self._check_movement()
        if row_to_move < 0:
            return True
        self._objects_view.move_row_up(row_to_move, wrap=self._config.wrap_movement)
        return True

    def on_move_down_button_clicked(self, source: QPushButton) -> bool:
        row_to_move = self._check_movement()
        if row_to_move < 0:
            return True
        self._objects_view.move_row_down(row_to_move, wrap=self._config.wrap_movement)
        return True

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()

    def _on_item_double_clicked(self, item):
        pass

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
            self._dialog_button_box.accepted.connect(self.on_accept)
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.rejected.connect(self.on_reject)
            self._layout.addWidget(self._dialog_button_box)

        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)

        if self._config.window_size:
            self.resize(*self._config.window_size)

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        if self._config.double_click_to_edit:
            self._objects_view.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _check_movement(self) -> int:
        selected_rows = self._objects_view.get_selected_rows(reverse=True)
        if len(selected_rows) < 1:
            if self._config.no_object_selected_warning_message:
                self._show_warning_message(self._config.no_object_added_warning_message)
            return -1
        if len(selected_rows) > 1:
            if self._config.multiple_objects_warning_message:
                self._show_warning_message(
                    self._config.multiple_objects_warning_message
                )
            return -1
        return selected_rows[0]
