from __future__ import annotations

import dataclasses
import json
from collections import OrderedDict
from typing import Type, TypeVar, Dict, Any, List, Tuple

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters import QJSONHighlighter
from qtpy.QtCore import Qt, QModelIndex
from qtpy.QtGui import QStandardItemModel, QStandardItem
from qtpy.QtWidgets import (
    QWidget,
    QTableView,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QHeaderView,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QLabel,
)

from ..codeeditor import JsonFormatter
from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils

TextElideMode = Qt.TextElideMode
GridStyle = Qt.PenStyle


@dataclasses.dataclass(frozen=True)
class PlainDictEditConfig(CommonParameterWidgetConfig):
    default_value: Dict[str] | None = None
    edit_button_text: str = "Edit"
    add_button_text: str = "Add"
    remove_button_text: str = "Remove"
    clear_button_text: str = "Clear"
    key_header: str = "Key"
    value_header: str = "Value"
    show_grid: bool = True
    grid_style: GridStyle = GridStyle.SolidLine
    alternating_row_colors: bool = True
    text_elide_mode: TextElideMode = TextElideMode.ElideRight
    corner_button_enabled: bool = True
    vertical_header_visible: bool = False
    horizontal_header_visible: bool = True
    min_height: int = 300
    confirm_remove: bool = True
    no_item_dialog_title: str = "Info"
    no_item_dialog_message: str = "No item has been added."
    no_selected_items_dialog_title: str = "Info"
    no_selected_items_dialog_message: str = "No item is selected."
    remove_item_dialog_title: str = "Confirm"
    remove_item_dialog_message: str = (
        "Are you sure you want to remove selected item(s)?"
    )
    clear_items_dialog_title: str = "Confirm"
    clear_items_dialog_message: str = "Are you sure you want to clear all items?"
    edit_item_editor_title: str = "Edit Item"
    add_item_editor_title: str = "Add Item"
    item_editor_size: Tuple[int, int] = (500, 400)

    @classmethod
    def target_widget_class(cls) -> Type["PlainDictEdit"]:
        return PlainDictEdit


class PlainDictEdit(CommonParameterWidget):
    Self = TypeVar("Self", bound="PlainDictEdit")
    ConfigClass = PlainDictEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: PlainDictEditConfig,
    ):
        self._config: PlainDictEditConfig = config
        self._value_widget: QWidget | None = None
        self._table_view: QTableView | None = None
        self._add_button: QPushButton | None = None
        self._remove_button: QPushButton | None = None
        self._clear_button: QPushButton | None = None
        self._edit_button: QPushButton | None = None

        self._model: QStandardItemModel | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            layout_main = QVBoxLayout()
            layout_main.setContentsMargins(0, 0, 0, 0)
            layout_main.setSpacing(0)
            self._value_widget.setLayout(layout_main)

            self._table_view = QTableView(self._value_widget)
            if self._config.min_height > 0:
                self._table_view.setMinimumHeight(self._config.min_height)
            self._table_view.setDragEnabled(False)
            self._table_view.setTextElideMode(self._config.text_elide_mode)
            self._table_view.setAlternatingRowColors(
                self._config.alternating_row_colors
            )
            self._table_view.setShowGrid(self._config.show_grid)
            self._table_view.setGridStyle(self._config.grid_style)
            self._table_view.setCornerButtonEnabled(self._config.corner_button_enabled)
            self._table_view.verticalHeader().setVisible(
                self._config.vertical_header_visible
            )
            self._table_view.horizontalHeader().setVisible(
                self._config.horizontal_header_visible
            )
            self._table_view.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeToContents
            )
            self._table_view.horizontalHeader().setStretchLastSection(True)
            self._table_view.setEditTriggers(QTableView.NoEditTriggers)
            self._table_view.setSelectionBehavior(QTableView.SelectRows)
            self._table_view.setSelectionMode(QTableView.SingleSelection)
            # noinspection PyUnresolvedReferences
            self._table_view.doubleClicked.connect(self._on_start_editing)

            self._model = QStandardItemModel(0, 2)
            self._model.setHorizontalHeaderLabels(
                [self._config.key_header, self._config.value_header]
            )
            self._table_view.setModel(self._model)
            layout_main.addWidget(self._table_view)

            layout_buttons = QGridLayout(self._value_widget)

            self._edit_button = QPushButton(
                self._config.edit_button_text, self._value_widget
            )
            # noinspection PyUnresolvedReferences
            self._edit_button.clicked.connect(self._on_edit_item)
            layout_buttons.addWidget(self._edit_button, 1, 1)

            self._add_button = QPushButton(
                self._config.add_button_text, self._value_widget
            )
            # noinspection PyUnresolvedReferences
            self._add_button.clicked.connect(self._on_add_item)
            layout_buttons.addWidget(self._add_button, 1, 0)

            self._remove_button = QPushButton(
                self._config.remove_button_text, self._value_widget
            )
            # noinspection PyUnresolvedReferences
            self._remove_button.clicked.connect(self._on_remove_item)
            layout_buttons.addWidget(self._remove_button, 2, 0)

            self._clear_button = QPushButton(
                self._config.clear_button_text, self._value_widget
            )
            # noinspection PyUnresolvedReferences
            self._clear_button.clicked.connect(self._on_clear_items)
            layout_buttons.addWidget(self._clear_button, 2, 1)

            layout_main.addLayout(layout_buttons)
        return self._value_widget

    def set_value_to_widget(self, value: Dict[str, Any]):
        self._clear_items()
        for key, value in value.items():
            self._insert_item(key, value, -1)

    def get_value_from_widget(self) -> Dict[str, Any]:
        value = OrderedDict()
        for row in range(self._model.rowCount()):
            key_item = self._model.item(row, 0)
            value_item = self._model.item(row, 1)
            value[key_item.text()] = json.loads(value_item.text())
        return value

    def _on_add_item(self):
        keys = self._get_keys()
        editor = _KeyValueEditor(
            self,
            keys,
            current_key=None,
            current_value=None,
            key_label=self._config.key_header,
            value_label=self._config.value_header,
            window_size=self._config.item_editor_size,
        )
        editor.setWindowTitle(self._config.add_item_editor_title)
        if editor.exec_() == QDialog.Rejected:
            return
        new_key = editor.get_current_key()
        new_value = editor.get_current_value()
        if new_key is None or new_value is None:
            return
        selected_rows = self._table_view.selectionModel().selectedRows()
        if not selected_rows:
            selected_row = self._model.rowCount()
        else:
            selected_row = selected_rows[-1]
            if isinstance(selected_row, QModelIndex):
                if selected_row.isValid():
                    selected_row = selected_row.row() + 1
                else:
                    selected_row = self._model.rowCount()
        self._model.insertRow(selected_row)
        self._model.setItem(selected_row, 0, QStandardItem(new_key))
        self._model.setItem(selected_row, 1, QStandardItem(new_value))

    def _on_remove_item(self):
        selected_rows = self._table_view.selectionModel().selectedRows()
        if not selected_rows:
            utils.show_info_message(
                self,
                title=self._config.no_selected_items_dialog_title,
                message=self._config.no_selected_items_dialog_message,
            )
            return
        if self._config.confirm_remove:
            ret = utils.show_question_message(
                self,
                title=self._config.remove_item_dialog_title,
                message=self._config.remove_item_dialog_message,
                buttons=utils.StandardButton.Yes | utils.StandardButton.No,
            )
            if ret != utils.StandardButton.Yes:
                return
        self._remove_rows(selected_rows)

    def _on_edit_item(self):
        selected_index = self._table_view.selectionModel().selectedIndexes()
        if not selected_index:
            utils.show_info_message(
                self,
                title=self._config.no_selected_items_dialog_title,
                message=self._config.no_selected_items_dialog_message,
            )
            return
        first_idx = selected_index[0]
        self._on_start_editing(first_idx)

    def _on_start_editing(self, idx: QModelIndex):
        if not idx.isValid():
            return
        current_key_item = self._model.item(idx.row(), 0)
        current_value_item = self._model.item(idx.row(), 1)
        current_key = current_key_item.text()
        current_value = current_value_item.text()
        keys = self._get_keys()

        editor = _KeyValueEditor(
            self,
            keys,
            current_key,
            current_value,
            key_label=self._config.key_header,
            value_label=self._config.value_header,
            window_size=self._config.item_editor_size,
        )
        editor.setWindowTitle(self._config.edit_item_editor_title)
        if editor.exec_() == QDialog.Rejected:
            return
        new_key = editor.get_current_key()
        new_value = editor.get_current_value()
        if new_key is None or new_value is None:
            return
        self._model.setItem(idx.row(), 0, QStandardItem(new_key))
        self._model.setItem(idx.row(), 1, QStandardItem(new_value))

    def _on_clear_items(self):
        if self._item_count() <= 0:
            utils.show_info_message(
                self,
                title=self._config.no_item_dialog_title,
                message=self._config.no_item_dialog_message,
            )
            return
        if not self._config.confirm_remove:
            self._clear_items()
            return
        ret = utils.show_question_message(
            self,
            title=self._config.clear_items_dialog_title,
            message=self._config.clear_items_dialog_message,
            buttons=utils.StandardButton.Yes | utils.StandardButton.No,
        )
        if ret == utils.StandardButton.Yes:
            self._clear_items()

    def _clear_items(self):
        self._model.removeRows(0, self._model.rowCount())

    def _insert_item(self, key: str, value: Any, row: int):
        if row == -1:
            row = self._model.rowCount()
        self._model.insertRow(row)
        key_item = QStandardItem(key)
        value = json.dumps(value, ensure_ascii=False)
        value_item = QStandardItem(value)
        self._model.setItem(row, 0, key_item)
        self._model.setItem(row, 1, value_item)

    def _item_count(self) -> int:
        return self._model.rowCount()

    def _remove_rows(self, rows: List[QModelIndex]):
        rows = list(set(row.row() for row in rows if row.isValid()))
        rows.sort(reverse=True)
        print(rows)
        for row in rows:
            self._model.removeRow(row)

    def _get_keys(self) -> List[str]:
        keys = []
        for i in range(self._item_count()):
            key_item = self._model.item(i, 0)
            if key_item:
                keys.append(key_item.text())
        return keys


class _KeyValueEditor(QDialog):
    def __init__(
        self,
        parent: QWidget | None,
        added_keys: List[str],
        current_key: str | None = None,
        current_value: str | None = None,
        *,
        key_label: str = "Key",
        value_label: str = "Value",
        window_size: Tuple[int, int] | None = None,
    ):
        super().__init__(parent)
        self._keys = added_keys
        self._current_key = current_key
        self._current_value = current_value

        self._formater = JsonFormatter()

        if window_size:
            self.resize(*window_size)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self._key_label = QLabel(key_label, self)
        layout.addWidget(self._key_label)

        self._key_edit: QLineEdit = QLineEdit(self)
        layout.addWidget(self._key_edit)

        self._value_label: QLabel = QLabel(value_label, self)
        layout.addWidget(self._value_label)

        self._value_edit: QCodeEditor = QCodeEditor(self)
        highlighter = QJSONHighlighter()
        self._value_edit.setHighlighter(highlighter)
        layout.addWidget(self._value_edit)

        self._button_box = QDialogButtonBox(self)
        self._button_box.setStandardButtons(
            QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        )
        self._button_box.setOrientation(Qt.Horizontal)
        # noinspection PyUnresolvedReferences
        self._button_box.accepted.connect(self._on_confirm)
        # noinspection PyUnresolvedReferences
        self._button_box.rejected.connect(self._on_cancel)
        layout.addWidget(self._button_box)

        if self._current_key is not None:
            self._key_edit.setText(self._current_key)

        if self._current_value is not None:
            self._value_edit.setPlainText(
                self._formater.format_code(self._current_value)
            )

    def get_current_key(self) -> str | None:
        return self._current_key

    def get_current_value(self) -> str:
        return self._current_value

    def _on_confirm(self):
        current_key = self._key_edit.text()
        current_value = self._value_edit.toPlainText()

        if current_key != self._current_key and current_key in self._keys:
            utils.show_info_message(
                self,
                title="Duplicated key",
                message="The key is duplicated with other keys.",
            )
            return

        if current_value == "":
            self._current_value = "null"
            self._current_key = current_key
            self.accept()
            return

        try:
            current_value = json.dumps(json.loads(current_value), ensure_ascii=False)
        except Exception as e:
            utils.show_info_message(
                self,
                title="Invalid JSON",
                message=f"The current value text is not valid JSON type: {e}",
            )
        else:
            self._current_value = current_value
            self._current_key = current_key
            self.accept()

    def _on_cancel(self):
        self.reject()
