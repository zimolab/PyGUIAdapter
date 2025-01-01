import dataclasses
from typing import Dict, Union, Any, Optional, cast, Tuple, List

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView

from ._commons import KEY_COLUMN_INDEX, VALUE_COLUMN_INDEX
from ._delegate import ObjectItemDelegate, KeyValueDelegate
from .schema import ValueType, CellWidgetMixin
from ..exceptions import ValidationFailedError
from ..tableview import TableView, TableViewConfig


@dataclasses.dataclass
class ObjectEditViewConfig(TableViewConfig):
    key_column_header: str = "Key"
    value_column_header: str = "Value"
    validate_values: bool = True
    ignore_unknown_keys: bool = False
    item_text_alignment: Union[Qt.AlignmentFlag, int, None] = Qt.AlignCenter
    value_item_alignment: Union[Qt.AlignmentFlag, int, None] = None
    key_item_selectable: bool = False
    row_data_type: str = "tuple"
    row_selection_mode: bool = True
    real_key_as_tooltip: bool = False


class ObjectEditView(TableView):

    def __init__(
        self,
        parent: Optional[QWidget],
        config: ObjectEditViewConfig,
        schema: Dict[str, ValueType],
    ):
        self._schema = schema.copy()
        self._item_double_clicked_handlers: Dict[int, ValueType] = {}
        self._item_clicked_handlers: Dict[int, ValueType] = {}

        config.row_data_type = "tuple"

        super().__init__(
            parent,
            column_headers=[config.key_column_header, config.value_column_header],
            config=config,
        )

        # noinspection PyUnresolvedReferences
        self.cellDoubleClicked.connect(self._on_cell_double_clicked)
        # noinspection PyUnresolvedReferences
        self.cellClicked.connect(self._on_cell_clicked)

        self.set_schema(schema)

    @property
    def config(self) -> ObjectEditViewConfig:
        return cast(ObjectEditViewConfig, super().config)

    @property
    def schema(self) -> Dict[str, ValueType]:
        return self._schema.copy()

    def set_schema(self, schema: Dict[str, ValueType]):

        if self._schema is not schema:
            del self._schema
            self._schema = schema.copy()
        self._item_double_clicked_handlers.clear()
        self._item_clicked_handlers.clear()
        self.remove_all_rows()

        if not self.config.key_column_header or not self.config.value_column_header:
            self.horizontalHeader().setVisible(False)

        # key -> (row, default_value, delegate)
        delegates: Dict[str, Tuple[int, Any, KeyValueDelegate]] = {}
        # prepare default_value, delegate and hooks for each row
        for row, (key, vt) in enumerate(self._schema.items()):
            value_delegate = KeyValueDelegate(self, vt)
            delegates[key] = row, vt.default_value, value_delegate

            if vt.hook_item_clicked():
                self._item_clicked_handlers[row] = vt

            if vt.hook_item_double_clicked():
                self._item_double_clicked_handlers[row] = vt

        # append rows with the default value and set the delegate for each of them
        for key, (row, default_value, delegate) in delegates.items():
            self.insert_row(row, (key, default_value))
            self.setItemDelegateForRow(row, delegate)

    def keys(self) -> List[str]:
        return [
            self.item(row, KEY_COLUMN_INDEX).data(Qt.UserRole)
            for row in range(self.row_count())
        ]

    def contains_key(self, key: str) -> bool:
        return self._row_for_key(key) >= 0

    def update_object(self, obj: Dict[str, Any]):
        for key, value in obj.items():
            row = self._row_for_key(key)
            if row < 0:
                if self.config.ignore_unknown_keys:
                    continue
                raise KeyError(f"unknown key: {key}")
            if self.config.validate_values:
                vt = self._schema[key]
                if not vt.validate(value):
                    raise ValidationFailedError(f"invalid value: {key}: {value}")
            self.on_set_item_data(row, VALUE_COLUMN_INDEX, value)

    def set_value(self, key: str, value: Any):
        row = self._row_for_key(key)
        if row < 0:
            raise KeyError(f"unknown key: {key}")
        if self.config.validate_values:
            vt = self._schema[key]
            if not vt.validate(value):
                raise ValidationFailedError(f"invalid value: {key}: {value}")
        self.on_set_item_data(row, VALUE_COLUMN_INDEX, value)

    def get_value(self, key: str) -> Any:
        row = self._row_for_key(key)
        if row < 0:
            raise KeyError(f"unknown key: {key}")
        return self.on_get_item_data(row, VALUE_COLUMN_INDEX)

    def remove_key(self, key: str):
        row = self._row_for_key(key)
        if row < 0:
            raise KeyError(f"unknown key: {key}")
        cur = self.get_object()
        del cur[key]
        self._schema.pop(key, None)
        self.set_schema(self._schema)
        self.update_object(cur)

    def add_key(self, key: str, value_type: ValueType, **kwargs):
        row = self._row_for_key(key)
        if row >= 0:
            raise KeyError(f"key already exists: {key}")
        cur = self.get_object()
        if "value" in kwargs:
            value = kwargs.pop("value")
            if self.config.validate_values:
                if not value_type.validate(value):
                    raise ValidationFailedError(f"invalid value: {key}: {value}")
        else:
            value = value_type.default_value
        cur[key] = value
        self._schema[key] = value_type
        self.set_schema(self._schema)
        self.update_object(cur)

    def replace_key(self, key: str, value_type: ValueType, **kwargs):
        row = self._row_for_key(key)
        if row < 0:
            raise KeyError(f"unknown key: {key}")
        cur = self.get_object()
        if "value" in kwargs:
            value = kwargs.pop("value")
            if self.config.validate_values:
                if not value_type.validate(value):
                    raise ValidationFailedError(f"invalid value: {key}: {value}")
        else:
            value = value_type.default_value
        cur[key] = value
        self._schema[key] = value_type
        self.update_object(cur)

    def get_object(self) -> Dict[str, Any]:
        return {key: value for key, value in self.get_all_row_data()}

    def on_create_item(
        self, row: int, col: int
    ) -> Union[QTableWidgetItem, CellWidgetMixin]:
        # get value_type for this row
        vt = self._get_value_type(row)

        # for key column, just create a normal item
        if col == KEY_COLUMN_INDEX:
            item = QTableWidgetItem()
            # call after_create_item hook in value_type
            vt.after_create_item(row, col, item)
            return item

        # create item or cell widget for value column
        if not vt:
            return super().on_create_item(row, col)
        cell_widget = vt.create_cell_widget(self, row, col)
        if isinstance(cell_widget, CellWidgetMixin):
            return cell_widget

        # call after_create_item hook in value_type
        item = super().on_create_item(row, col)
        vt.after_create_item(row, col, item)
        return item

    def on_insert_item(
        self, row: int, col: int, item: Union[QTableWidgetItem, CellWidgetMixin]
    ):
        if isinstance(item, CellWidgetMixin):
            assert isinstance(item, QWidget)
            self.setCellWidget(row, col, item)
            return
        super().on_insert_item(row, col, item)
        vt = self._get_value_type(row)
        if not vt:
            return
        vt.after_insert_item(row, col, item)

    def on_set_item_data(self, row: int, col: int, data: Any):
        cell_widget = self.cellWidget(row, col)
        if isinstance(cell_widget, CellWidgetMixin):
            cell_widget.set_value(data)
            return
        super().on_set_item_data(row, col, data)
        if col == VALUE_COLUMN_INDEX:
            if self.config.value_item_alignment is not None:
                item = self.item(row, col)
                if item is not None:
                    item.setTextAlignment(self.config.value_item_alignment)
        elif col == KEY_COLUMN_INDEX:
            # we store the key as the data of the key column item,
            # and we display the item using the display_name of the value_type if available
            # so that the display name is not necessarily the same as the real key
            item = self.item(row, col)
            display_name = self._display_name_for_row(row) or data
            item.setText(display_name)
            item.setData(Qt.UserRole, data)
            if self.config.real_key_as_tooltip:
                item.setToolTip(data)
            if not item:
                return
            if not self.config.key_item_selectable:
                # noinspection PyUnresolvedReferences
                flags = item.flags() & ~Qt.ItemIsSelectable
                item.setFlags(flags)
        else:
            raise ValueError(f"unexpected column: {col}")

        vt = self._get_value_type(row)
        if not vt:
            return
        item = self.item(row, col)
        vt.after_set_item_data(row, col, item, data)

    def on_get_item_data(self, row: int, col: int) -> Any:
        cell_widget = self.cellWidget(row, col)
        if isinstance(cell_widget, CellWidgetMixin):
            return cell_widget.get_value()
        return super().on_get_item_data(row, col)

    def on_remove_item(self, row: int, col: int) -> Any:
        cell_widget = self.cellWidget(row, col)
        if isinstance(cell_widget, CellWidgetMixin):
            data = cell_widget.get_value()
            assert isinstance(cell_widget, QWidget)
            self.removeCellWidget(row, col)
            cell_widget.deleteLater()
            return data
        return super().on_remove_item(row, col)

    def _setup_columns(self):
        for column_index, column_key in enumerate(self.column_headers):
            column_key = self.column_keys[column_index]
            vt = self._schema[column_key]
            delegate = ObjectItemDelegate(self, vt)
            self.setItemDelegateForColumn(column_index, delegate)
            # hook events if needed
            if vt.hook_item_double_clicked():
                self._item_double_clicked_handlers[column_index] = vt

            if vt.hook_item_clicked():
                self._item_clicked_handlers[column_index] = vt

    def _on_cell_double_clicked(self, row: int, column: int):
        if not self._item_double_clicked_handlers:
            return
        vt: ValueType = self._item_double_clicked_handlers.get(row, None)
        if not vt:
            return
        item = self.item(row, column)
        data = self.on_get_item_data(row, column)
        vt.on_item_double_clicked(self, row, column, data, item)

    def _on_cell_clicked(self, row: int, column: int):
        if not self._item_clicked_handlers:
            return
        vt: ValueType = self._item_clicked_handlers.get(row, None)
        if not vt:
            return
        item = self.item(row, column)
        data = self.on_get_item_data(row, column)
        vt.on_item_clicked(self, row, column, data, item)

    def _display_name_for_row(self, row: int) -> Optional[str]:
        vt = self._get_value_type(row)
        if not vt:
            return ""
        return vt.display_name

    def _setup_ui(self):
        super()._setup_ui()
        self.setColumnCount(2)
        if self.config.key_column_header and self.config.value_column_header:
            self.setHorizontalHeaderLabels(
                [self.config.key_column_header, self.config.value_column_header]
            )
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        if self.config.row_selection_mode:
            self.setSelectionBehavior(QAbstractItemView.SelectRows)
        else:
            self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def _get_value_type(self, row: int) -> Optional[ValueType]:
        keys = list(self._schema.keys())
        if 0 > row >= len(keys):
            return None
        return self._schema.get(keys[row], None)

    def _row_for_key(self, key: str) -> int:
        for row in range(self.row_count()):
            item = self.item(row, KEY_COLUMN_INDEX)
            if item and item.data(Qt.UserRole) == key:
                return row
        return -1
