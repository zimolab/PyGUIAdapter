from typing import Optional, Dict, Union, Any, List

from qtpy.QtCore import Qt, QModelIndex, QAbstractItemModel
from qtpy.QtWidgets import (
    QTableWidget,
    QStyledItemDelegate,
    QWidget,
    QStyleOptionViewItem,
    QAbstractItemView,
    QTableWidgetItem,
)

from .schema import normalize_object_schema
from .valuetypes import ValueTypeBase, ValueWidgetMixin
from .valuetypes.base import HookType


class PlainObjectItemDelegate(QStyledItemDelegate):
    def __init__(
        self,
        value_type: ValueTypeBase,
        parent: Optional["PlainObjectTableWidget"] = None,
    ):
        super().__init__(parent)
        self._value_type = value_type

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        return self._value_type.on_create_editor(parent, option=option, index=index)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        data = index.data(Qt.EditRole)
        value_widget = self._to_value_widget(editor)
        value_widget.set_value(data)

    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex,
    ) -> None:
        value_widget = self._to_value_widget(editor)
        value = value_widget.get_value()
        # print("setModelData", value)
        model.setData(index, value, Qt.EditRole)

    @staticmethod
    def _to_value_widget(editor: QWidget) -> ValueWidgetMixin:
        if not isinstance(editor, ValueWidgetMixin):
            raise TypeError("editor must be a ValueWidgetMixin instance")
        return editor


class EmptyDelegate(QStyledItemDelegate):
    def __init__(self, parent: Optional["PlainObjectTableWidget"] = None):
        super().__init__(parent)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        return None


_empty_delegate = EmptyDelegate()


class PlainObjectTableWidget(QTableWidget):

    def __init__(
        self,
        object_schema: Dict[str, Union[ValueTypeBase, str, type, None]],
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._object_schema = normalize_object_schema(object_schema)
        self._key_to_column: Optional[Dict[str, int]] = None

        # col ->
        self._double_click_handlers = {}

        self._setup()

    def _setup(self):
        keys = list(self._object_schema.keys())
        self.setColumnCount(len(keys))
        self._key_to_column = {k: i for i, k in enumerate(keys)}
        self.setHorizontalHeaderLabels(keys)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.cellDoubleClicked.connect(self._on_cell_double_clicked)
        # set delegate for each column
        for key, column in self._key_to_column.items():
            value_type = self._object_schema.get(key, None)
            if value_type is None:
                continue
            if value_type.hook_type == HookType.ItemDelegate:
                delegate = PlainObjectItemDelegate(value_type, self)
                self.setItemDelegateForColumn(column, delegate)
            elif value_type.hook_type == HookType.CellDoubleClicked:
                self.setItemDelegateForColumn(column, _empty_delegate)
                self._double_click_handlers[column] = value_type
            else:
                pass

    def _on_cell_double_clicked(self, row: int, column: int):
        if column not in self._double_click_handlers:
            return
        value_type = self._double_click_handlers[column]
        value_type.on_cell_double_clicked(self, row, column)

    def get_object_schema(self) -> Dict[str, ValueTypeBase]:
        return {k: v for k, v in self._object_schema.items() if v is not None}

    def add_object(
        self,
        obj: Dict[str, Any],
        ignore_unknown_keys: bool = False,
        fill_missing_keys: bool = True,
    ):
        row = self.rowCount()
        self.insert_object(row, obj, ignore_unknown_keys, fill_missing_keys)

    def insert_object(
        self,
        row: int,
        obj: Dict[str, Any],
        ignore_unknown_keys: bool = False,
        fill_missing_keys: bool = True,
    ):
        self.insertRow(row)
        for column, value_item in self._create_items(obj, ignore_unknown_keys):
            self.setItem(row, column, value_item)
        obj_for_missing_keys = self._object_for_missing_keys(obj)
        if not obj_for_missing_keys:
            return

        if not fill_missing_keys:
            raise ValueError(f"missing keys: {obj_for_missing_keys.keys()}")

        for column, value_item in self._create_items(
            obj_for_missing_keys, ignore_unknown_keys=True
        ):
            self.setItem(row, column, value_item)

    def clear_objects(self):
        self.clearContents()
        self.setRowCount(0)

    def object_at(self, row: int) -> Dict[str, Any]:
        self._check_row(row)
        obj = {}
        for column in range(self.columnCount()):
            key = self.horizontalHeaderItem(column).text()
            value = self.item(row, column).data(Qt.EditRole)
            obj[key] = value
        return obj

    def set_objects(
        self, objects: List[Dict[str, Any]], ignore_unknown_keys: bool = False
    ):
        self.clear_objects()
        for obj in objects:
            self.add_object(obj, ignore_unknown_keys)

    def objects(self) -> List[Dict[str, Any]]:
        return [self.object_at(row) for row in range(self.rowCount())]

    def update_object(
        self, row: int, obj: Dict[str, Any], ignore_unknown_keys: bool = False
    ):
        self._check_row(row)
        for column, value_item in self._create_items(obj, ignore_unknown_keys):
            self.setItem(row, column, value_item)

    def get_selected_row(self) -> int:
        indexes = self.selectedIndexes()
        if not indexes:
            return -1
        return indexes[0].row()

    def swap_rows(self, row1: int, row2: int):
        if row1 == row2:
            return
        self._check_row(row1)
        self._check_row(row2)
        obj1 = self.object_at(row1)
        obj2 = self.object_at(row2)
        self.update_object(row1, obj2)
        self.update_object(row2, obj1)

    def move_up(self, row: int, step: int = 1, wrap: bool = False) -> int:
        self._check_row(row)
        if step < 0:
            raise ValueError("step must be a positive number")

        if step == 0:
            return row

        target_row = self._calc_target_row(row, -step, wrap)
        if target_row != row:
            self.swap_rows(row, target_row)
        return target_row

    def move_down(self, row: int, step: int = 1, wrap: bool = False) -> int:
        self._check_row(row)
        if step < 0:
            raise ValueError("step must be a positive number")

        if step == 0:
            return row

        target_row = self._calc_target_row(row, step, wrap)
        if target_row != row:
            self.swap_rows(row, target_row)
        return target_row

    def _check_row(self, row: int):
        if row < 0 or row >= self.rowCount():
            raise ValueError(f"row {row} is out of range")

    def _create_items(self, obj: Dict[str, Any], ignore_unknown_keys: bool = False):
        for key, value in obj.items():
            column = self._key_to_column.get(key, -1)
            if column == -1:
                if ignore_unknown_keys:
                    continue
                else:
                    raise ValueError(f"unknown key: {key}")
            item = QTableWidgetItem()
            item.setData(Qt.EditRole, value)
            yield column, item

    def _calc_target_row(self, current_row: int, step: int, wrap: bool):
        total = self.rowCount()
        if not wrap:
            target_row = max(0, min(current_row + step, total - 1))
        else:
            target_row = (current_row + step) % total
        return target_row

    def _object_for_missing_keys(self, obj: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ret = {}
        for key in self._object_schema.keys():
            if key not in obj:
                value_type = self._object_schema.get(key, None)
                if value_type is None:
                    raise ValueError(f"unknown value type for key: {key}")
                ret[key] = value_type.default_value
        if not ret:
            return None
        return ret
