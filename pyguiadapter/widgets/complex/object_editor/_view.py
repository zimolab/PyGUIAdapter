import dataclasses
from typing import Optional, List, Dict, Any, Tuple

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QAbstractItemView, QWidget, QTableWidgetItem

from ._commons import _KEY_COLUMN, _VALUE_COLUMN
from ._delegate import ValueDelegate
from ..commons import ValidationFailedError
from ..itemsview_base import TableView, TableViewConfig
from ..schema import ValueTypeBase


@dataclasses.dataclass
class ObjectTableViewConfig(TableViewConfig):
    key_column_header: str = "Key"
    value_column_header: str = "Value"
    key_alignment: Qt.AlignmentFlag = Qt.AlignHCenter | Qt.AlignVCenter
    value_alignment: Qt.AlignmentFlag = Qt.AlignLeft | Qt.AlignVCenter


class ObjectTableView(TableView):
    def __init__(
        self,
        parent: Optional[QWidget],
        object_schema: Dict[str, ValueTypeBase],
        config: Optional[ObjectTableViewConfig] = None,
    ):
        self._config = config or ObjectTableViewConfig()

        self._object_schema: Optional[Dict[str, ValueTypeBase]] = None
        self._item_double_clicked_hooks = {}
        self._item_clicked_hooks = {}

        super().__init__(parent, self._config)

        self._setup_ui()
        self.set_object_schema(object_schema)

        self.cellDoubleClicked.connect(self._on_item_double_clicked)
        self.cellClicked.connect(self._on_item_clicked)

    def _setup_ui(self):
        super()._setup_ui()
        self.setColumnCount(2)
        if self._config.key_column_header and self._config.value_column_header:
            self.setHorizontalHeaderLabels(
                [self._config.key_column_header, self._config.value_column_header]
            )

        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def set_object_schema(self, object_schema: Dict[str, ValueTypeBase]):
        if self._object_schema is not object_schema:
            del self._object_schema
            self._object_schema = object_schema.copy()

        self._item_double_clicked_hooks.clear()
        self._item_clicked_hooks.clear()

        self.clearContents()
        if not self._config.key_column_header or not self._config.value_column_header:
            self.horizontalHeader().setVisible(False)

        # key -> (row, default_value, delegate)
        delegates: Dict[str, Tuple[int, Any, ValueDelegate]] = {}
        # prepare default_value, delegate and hooks for each row
        for row, (key, vt) in enumerate(self._object_schema.items()):
            value_delegate = ValueDelegate(self, vt)
            delegates[key] = row, vt.default_value, value_delegate

            if vt.hook_item_clicked():
                self._item_clicked_hooks[row] = vt

            if vt.hook_item_double_clicked():
                self._item_double_clicked_hooks[row] = vt

        # append rows with the default value and set the delegate for each of them
        for key, (row, default_value, delegate) in delegates.items():
            self._append_row(key, default_value)
            self.setItemDelegateForRow(row, delegate)

    def update_object(
        self,
        obj: Dict[str, Any],
        validate: bool = True,
        ignore_unknown_keys: bool = False,
    ):
        for key, value in obj.items():
            row = self._find_row(key)
            if row < 0:
                if ignore_unknown_keys:
                    continue
                raise KeyError(f"key not found in object schema: {key}")

            if validate:
                vt = self._object_schema[key]
                if not vt.validate(value):
                    raise ValidationFailedError(f"validation failed: {key}:{value}")
            self.set_item_data(row, _VALUE_COLUMN, value)

    def set_value(self, key: str, value: Any, validate: bool = True):
        row = self._find_row(key)
        if row < 0:
            raise KeyError(f"key not found in object schema: {key}")
        if validate:
            vt = self._object_schema[key]
            if not vt.validate(value):
                raise ValidationFailedError(f"validation failed: {key}:{value}")
        self.set_item_data(row, _VALUE_COLUMN, value)

    def get_value(self, key: str, **kwargs) -> Any:
        row = self._find_row(key)
        if row < 0:
            raise KeyError(f"key not found in object schema: {key}")
        return self.get_item_data(row, _VALUE_COLUMN)

    def has_key(self, key: str) -> bool:
        return self._find_row(key) >= 0

    def keys(self) -> List[str]:
        return [self.item(row, _KEY_COLUMN).text() for row in range(self.row_count())]

    def get_object(self) -> Dict[str, Any]:
        obj = {}
        for row in range(self.rowCount()):
            key = self.get_item_data(row, _KEY_COLUMN)
            value = self.get_item_data(row, _VALUE_COLUMN)
            obj[key] = value
        return obj

    def remove_key(self, key: str):
        row = self._find_row(key)
        if row < 0:
            raise KeyError(f"key not found in object schema: {key}")
        cur_obj = self.get_object()
        del cur_obj[key]
        self._object_schema.pop(key)
        self.set_object_schema(self._object_schema)
        self.update_object(cur_obj, ignore_unknown_keys=True)

    def append_key(self, key: str, vt: ValueTypeBase, **kwargs):
        row = self._find_row(key)
        if row >= 0:
            raise KeyError(f"key already exists in object schema: {key}")
        cur_obj = self.get_object()
        if "value" in kwargs:
            value = kwargs.pop("value")
        else:
            value = vt.default_value
        cur_obj[key] = value
        self._object_schema[key] = vt
        self.set_object_schema(self._object_schema)
        self.update_object(cur_obj, ignore_unknown_keys=True)

    def replace_key(self, key: str, vt: ValueTypeBase, **kwargs):
        row = self._find_row(key)
        if row < 0:
            raise KeyError(f"key not found in object schema: {key}")
        cur_obj = self.get_object()
        if "value" in kwargs:
            value = kwargs.pop("value")
        else:
            value = vt.default_value
        cur_obj[key] = value
        self._object_schema[key] = vt
        self.set_object_schema(self._object_schema)
        self.update_object(cur_obj, ignore_unknown_keys=True)

    def create_item(self, row: int, column: int, data: Any) -> QTableWidgetItem:
        return super().create_item(row, column, data)

    def set_item_data(self, row: int, column: int, data: Any):
        item: QTableWidgetItem = self.item(row, column)
        if item is None:
            raise ValueError(f"no item found at row {row}, column {column}")

        if column == _VALUE_COLUMN:  # for value item
            item.setText(str(data))
            item.setData(Qt.EditRole, data)
            # noinspection PyTypeChecker
            item.setTextAlignment(self._config.value_alignment)
        else:  # for key item
            # noinspection PyUnresolvedReferences
            flags = item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
            item.setFlags(flags)
            item.setText(str(data))
            # noinspection PyTypeChecker
            item.setTextAlignment(self._config.key_alignment)

    def get_item_data(self, row: int, column: int) -> Any:
        item = self.item(row, column)
        if item is None:
            raise ValueError(f"no item found at row {row}, column {column}")
        if column == _VALUE_COLUMN:
            return item.data(Qt.EditRole)
        else:
            return item.text()

    def _find_row(self, key: str) -> int:
        for row in range(self.row_count()):
            item = self.item(row, _KEY_COLUMN)
            if item and item.text() == key:
                return row
        return -1

    def _insert_row(self, row: int, key: str, value: Any):
        self.insertRow(row)
        # create key item
        key_item = self.create_item(row, _KEY_COLUMN, key)
        self.setItem(row, _KEY_COLUMN, key_item)
        # set the key item
        self.set_item_data(row, _KEY_COLUMN, key)

        # create value item
        value_item = self.create_item(row, _VALUE_COLUMN, value)
        self.setItem(row, _VALUE_COLUMN, value_item)
        # set the value item
        self.set_item_data(row, _VALUE_COLUMN, value)

    def _append_row(self, key: str, value: Any):
        self._insert_row(self.rowCount(), key, value)

    def _on_item_clicked(self, row: int, column: int):
        if not self._item_clicked_hooks or column != _VALUE_COLUMN:
            return

        if row in self._item_clicked_hooks:
            vt: ValueTypeBase = self._item_clicked_hooks[row]
            item = self.item(row, _VALUE_COLUMN)
            vt.on_item_clicked(
                self, row, column, data=self.get_item_data(row, column), item=item
            )

    def _on_item_double_clicked(self, row: int, column: int):
        if not self._item_double_clicked_hooks or column != _VALUE_COLUMN:
            return

        if row in self._item_double_clicked_hooks:
            vt: ValueTypeBase = self._item_double_clicked_hooks[row]
            item = self.item(row, _VALUE_COLUMN)
            vt.on_item_double_clicked(
                self, row, column, data=self.get_item_data(row, column), item=item
            )
