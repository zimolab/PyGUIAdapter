from qtpy.QtGui import QCloseEvent
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QApplication,
    QVBoxLayout,
    QTableWidget,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QAbstractItemView,
    QMessageBox,
    QTableWidgetItem,
)
from typing import Dict, Optional, Tuple, Callable

from .itemdlg import StringDictItemDialogConfig, ItemDialog

_KEY_COLUMN = 0
_VALUE_COLUMN = 1
_ROW_NOT_FOUND = -1

_DEFAULT_SIZE = (700, 350)


class StringDictEditor(QDialog):
    def __init__(
        self,
        parent: Optional[QDialog] = None,
        title: str = "",
        size: Optional[Tuple[int, int]] = None,
        *,
        key_label: str = "Key",
        value_label: str = "Value",
        up_button_text: str = "Up",
        down_button_text: str = "Down",
        add_button_text: str = "New",
        edit_button_text: str = "Edit",
        remove_button_text: str = "Remove",
        clear_button_text: str = "Clear",
        remove_confirm_message: Optional[str] = "Are you sure to remove this item?",
        clear_confirm_message: Optional[str] = "Are you sure to clear all items?",
        no_selected_item_message: str = "No item is selected! Please select an item first!",
        no_items_added_message: str = "No items are added!",
        waring_dialog_title: str = "Warning",
        error_dialog_title: str = "Error",
        vertical_header: bool = True,
        value_column_editable: bool = True,
        double_click_to_edit: bool = True,
        add_item_dialog_title: str = "Add Item",
        edit_item_dialog_title: str = "Edit Item",
        item_dialog_size: Optional[Tuple[int, int]] = None,
        item_dialog_config: Optional[StringDictItemDialogConfig] = None,
        before_close_callback: Optional[Callable[["StringDictEditor"], bool]] = None,
        **kwargs,
    ):
        super().__init__(parent)

        self._key_label = key_label
        self._value_label = value_label
        self._remove_confirm_message = remove_confirm_message
        self._clear_confirm_message = clear_confirm_message
        self._no_selected_item_message = no_selected_item_message
        self._no_items_added_message = no_items_added_message
        self._waring_dialog_title = waring_dialog_title
        self._error_dialog_title = error_dialog_title
        self._vertical_header = vertical_header
        self._value_column_editable = value_column_editable
        self._double_click_to_edit = double_click_to_edit

        self._before_close_callback = before_close_callback

        self._add_item_dialog_title = add_item_dialog_title
        self._edit_item_dialog_title = edit_item_dialog_title
        self._item_dialog_size = item_dialog_size
        if item_dialog_config is not None:
            if not item_dialog_config.key_label:
                item_dialog_config.key_label = self._key_label
            if not item_dialog_config.value_label:
                item_dialog_config.value_label = self._value_label
            self._item_dialog_config = item_dialog_config
        else:
            self._item_dialog_config = StringDictItemDialogConfig(
                key_label=self._key_label,
                value_label=self._value_label,
            )

        self._item_dialog: Optional[ItemDialog] = None

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._table_widget: QTableWidget = QTableWidget(self)
        self._layout.addWidget(self._table_widget)
        self._setup_table_widget()

        self._button_layout = QHBoxLayout()
        self._layout.addLayout(self._button_layout)

        self._button_layout.addSpacerItem(
            QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        self._up_button = QPushButton(up_button_text, self)
        self._up_button.clicked.connect(self._on_move_up_item)
        self._button_layout.addWidget(self._up_button)

        self._down_button = QPushButton(down_button_text, self)
        self._down_button.clicked.connect(self._on_move_down_item)
        self._button_layout.addWidget(self._down_button)

        self._button_layout.addSpacerItem(
            QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        self._add_button = QPushButton(add_button_text, self)
        self._add_button.clicked.connect(self._on_add_item)
        self._button_layout.addWidget(self._add_button)

        self._edit_button = QPushButton(edit_button_text, self)
        self._edit_button.clicked.connect(self._on_edit_item)
        self._button_layout.addWidget(self._edit_button)

        self._remove_button = QPushButton(remove_button_text, self)
        self._remove_button.clicked.connect(self._on_remove_item)
        self._button_layout.addWidget(self._remove_button)

        self._clear_button = QPushButton(clear_button_text, self)
        self._clear_button.clicked.connect(self._on_clear_items)
        self._button_layout.addWidget(self._clear_button)

        self._button_layout.addSpacerItem(
            QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        # self._dlg_buttons = QDialogButtonBox(
        #     QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        # )
        # self._dlg_buttons.accepted.connect(self.accept)
        # self._dlg_buttons.rejected.connect(self.reject)
        # self._button_layout.addWidget(self._dlg_buttons)

        size = size or _DEFAULT_SIZE
        self.resize(*size)
        self.setWindowTitle(title)

        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)

        self._update_button_status()

    def closeEvent(self, event: QCloseEvent):
        if not self._before_close_callback:
            return super().closeEvent(event)

        ret = self._before_close_callback(self)
        if ret:
            event.accept()
            return
        event.ignore()

    def _setup_table_widget(self):
        self._table_widget.setColumnCount(2)
        self._table_widget.setHorizontalHeaderLabels(
            [self._key_label, self._value_label]
        )
        self._table_widget.horizontalHeader().setStretchLastSection(True)
        self._table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self._table_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self._table_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self._table_widget.verticalHeader().setVisible(self._vertical_header)

        self._table_widget.setEditTriggers(QAbstractItemView.CurrentChanged)

        if self._double_click_to_edit:
            self._table_widget.cellDoubleClicked.connect(self._on_cell_double_clicked)

    @property
    def string_dict(self) -> Dict[str, str]:
        """
        Returns the current string dictionary.
        """
        current_dict = {}
        for row in range(self._table_widget.rowCount()):
            key = self._table_widget.item(row, _KEY_COLUMN).text()
            value = self._table_widget.item(row, _VALUE_COLUMN).text()
            current_dict[key] = value
        return current_dict

    @string_dict.setter
    def string_dict(self, values: Dict[str, str]):
        """
        Set the current string dictionary.
        """
        value = values or {}
        self.clear()
        for key in values:
            self._add_row(key, value[key])
        self._update_button_status()

    def set(self, key: str, value: str):
        self._add_row(key, value)
        self._update_button_status()

    def get(self, key: str, **kwargs) -> str:
        row = self._find_row(key)
        if row != _ROW_NOT_FOUND:
            value = self._table_widget.item(row, _VALUE_COLUMN).text()
            return value

        if not "default" in kwargs:
            raise KeyError(f"key not found: {key}")
        return kwargs["default"]

    def remove(self, key: str, no_raise: bool = False):
        row = self._find_row(key)
        if row == _ROW_NOT_FOUND and not no_raise:
            raise KeyError(f"key not found: {key}")
        self._table_widget.removeRow(row)
        self._update_button_status()

    def clear(self):
        for row in range(self._table_widget.rowCount()):
            self._table_widget.removeRow(self._table_widget.rowCount() - 1)
        self._update_button_status()

    def contains(self, key: str) -> bool:
        return self._find_row(key) != _ROW_NOT_FOUND

    def _add_row(self, key: str, value: str):
        row = self._find_row(key)
        if row != _ROW_NOT_FOUND:
            self._update_row(row, key, value)
            self._update_button_status()
            return
        self._table_widget.insertRow(self._table_widget.rowCount())
        current_row = self._table_widget.rowCount() - 1

        key_item = QTableWidgetItem(key)
        key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)

        value_item = QTableWidgetItem(value)
        if self._value_column_editable:
            value_item.setFlags(value_item.flags() | Qt.ItemIsEditable)

        self._table_widget.setItem(current_row, _KEY_COLUMN, key_item)
        self._table_widget.setItem(current_row, _VALUE_COLUMN, value_item)

    def _update_row(self, row: int, key: str, value: str):
        key_item = self._table_widget.item(row, _KEY_COLUMN)
        value_item = self._table_widget.item(row, _VALUE_COLUMN)
        key_item.setText(key)
        value_item.setText(value)

    def _find_row(self, key: str) -> int:
        for row in range(self._table_widget.rowCount()):
            current_key = self._table_widget.item(row, _KEY_COLUMN).text()
            if current_key == key:
                return row
        return _ROW_NOT_FOUND

    def _dismiss_item_dialog(self):
        if self._item_dialog is not None:
            self._item_dialog.close()
            self._item_dialog.deleteLater()
            self._item_dialog = None

    def _on_add_item(self):
        self._dismiss_item_dialog()
        self._item_dialog = ItemDialog(
            self,
            title=self._add_item_dialog_title,
            size=self._item_dialog_size,
            **self._item_dialog_config.as_dict(),
        )
        new_key_value = self._item_dialog.get_key_value()
        self._dismiss_item_dialog()
        if new_key_value is not None:
            self._add_row(*new_key_value)
            self._update_button_status()

    def _on_edit_item(self):
        self._dismiss_item_dialog()
        current_row = self._table_widget.selectionModel().currentIndex().row()
        if current_row < 0:
            QMessageBox.warning(
                self, self._waring_dialog_title, self._no_selected_item_message
            )
            return
        current_key = self._table_widget.item(current_row, _KEY_COLUMN).text()
        current_value = self._table_widget.item(current_row, _VALUE_COLUMN).text()
        self._item_dialog = ItemDialog(
            self,
            title=self._edit_item_dialog_title,
            size=self._item_dialog_size,
            initial_key=current_key,
            initial_value=current_value,
            **self._item_dialog_config.as_dict(),
        )
        new_key_value = self._item_dialog.get_key_value()
        self._dismiss_item_dialog()
        if new_key_value is not None:
            self._add_row(*new_key_value)
            self._update_button_status()

    def _on_cell_double_clicked(self, row: int, column: int):
        _ = row, column  # unused
        self._on_edit_item()

    def _on_remove_item(self):
        current_row = self._table_widget.selectionModel().currentIndex().row()
        if current_row < 0:
            QMessageBox.warning(
                self, self._waring_dialog_title, self._no_selected_item_message
            )
            return
        if not self._remove_confirm_message:
            self._table_widget.removeRow(current_row)
            return
        ret = QMessageBox.question(
            self,
            self._waring_dialog_title,
            self._remove_confirm_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if ret == QMessageBox.Yes:
            self._table_widget.removeRow(current_row)

    def _on_clear_items(self):
        if self._table_widget.rowCount() == 0:
            QMessageBox.warning(
                self, self._waring_dialog_title, self._no_items_added_message
            )
            return
        if not self._clear_confirm_message:
            self.clear()
            return
        ret = QMessageBox.question(
            self,
            self._waring_dialog_title,
            self._clear_confirm_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if ret == QMessageBox.Yes:
            self.clear()

    def _on_move_up_item(self):
        selected_row = self._table_widget.selectionModel().currentIndex().row()
        if selected_row < 0:
            QMessageBox.warning(
                self, self._waring_dialog_title, self._no_selected_item_message
            )
            return
        if selected_row == 0:
            return

        current_key_item = self._table_widget.item(selected_row, _KEY_COLUMN)
        current_value_item = self._table_widget.item(selected_row, _VALUE_COLUMN)
        current_key = current_key_item.text()
        current_value = current_value_item.text()

        above_row = selected_row - 1
        above_key_item = self._table_widget.item(above_row, _KEY_COLUMN)
        above_value_item = self._table_widget.item(above_row, _VALUE_COLUMN)
        above_key = above_key_item.text()
        above_value = above_value_item.text()

        above_key_item.setText(current_key)
        above_value_item.setText(current_value)

        current_key_item.setText(above_key)
        current_value_item.setText(above_value)

        self._table_widget.selectRow(above_row)

    def _on_move_down_item(self):
        selected_row = self._table_widget.selectionModel().currentIndex().row()
        if selected_row < 0:
            QMessageBox.warning(
                self, self._waring_dialog_title, self._no_selected_item_message
            )
            return
        if selected_row == (self._table_widget.rowCount() - 1):
            return

        current_key_item = self._table_widget.item(selected_row, _KEY_COLUMN)
        current_value_item = self._table_widget.item(selected_row, _VALUE_COLUMN)
        current_key = current_key_item.text()
        current_value = current_value_item.text()

        below_row = selected_row + 1
        below_key_item = self._table_widget.item(below_row, _KEY_COLUMN)
        below_value_item = self._table_widget.item(below_row, _VALUE_COLUMN)
        below_key = below_key_item.text()
        below_value = below_value_item.text()

        below_key_item.setText(current_key)
        below_value_item.setText(current_value)

        current_key_item.setText(below_key)
        current_value_item.setText(below_value)

        self._table_widget.selectRow(below_row)

    def _on_selection_changed(self):
        self._update_button_status()

    def _update_button_status(self):
        selected_row = self._table_widget.selectionModel().currentIndex().row()
        is_first_row = selected_row == 0
        is_last_row = selected_row == (self._table_widget.rowCount() - 1)
        self._up_button.setEnabled(selected_row >= 0 and not is_first_row)
        self._down_button.setEnabled(selected_row >= 0 and not is_last_row)
        self._remove_button.setEnabled(selected_row >= 0)
        self._edit_button.setEnabled(selected_row >= 0)


if __name__ == "__main__":
    app = QApplication()
    dialog = StringDictEditor()
    dialog.string_dict = {"a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6"}
    dialog.show()
    app.exec_()
    print(dialog.string_dict)
