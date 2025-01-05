import dataclasses
from typing import Dict, Union, Any, Optional, cast, List

from qtpy.QtWidgets import QWidget, QTableWidgetItem

from ._delegate import ObjectItemDelegate
from ..schema import ValueType, CellWidgetMixin
from ..exceptions import ValidationFailedError
from ..tableview import TableView, TableViewConfig


@dataclasses.dataclass
class MultiObjectEditViewConfig(TableViewConfig):
    row_data_type: str = "dict"
    validate_added_object: bool = True


class MultiObjectEditView(TableView):

    def __init__(
        self,
        parent: Optional[QWidget],
        config: MultiObjectEditViewConfig,
        schema: Dict[str, ValueType],
    ):
        self._schema = schema.copy()
        self._item_double_clicked_handlers: Dict[int, ValueType] = {}
        self._item_clicked_handlers: Dict[int, ValueType] = {}

        # make sure row_data_type is "dict"
        config.row_data_type = "dict"

        super().__init__(
            parent, column_headers=self._get_column_headers(), config=config
        )

        self.cellDoubleClicked.connect(self._on_cell_double_clicked)
        self.cellClicked.connect(self._on_cell_clicked)

        self._setup_columns()

    @property
    def config(self) -> MultiObjectEditViewConfig:
        return cast(MultiObjectEditViewConfig, super().config)

    def add_object(self, obj: Dict[str, Any]):
        if self.config.validate_added_object and not self.validate_object(obj):
            raise ValidationFailedError(f"validation failed: {obj}")
        self.append_row(obj)

    def update_object(self, row: int, obj: Dict[str, Any]):
        if row < 0 or row >= self.rowCount():
            raise IndexError(f"row index out of range: {row}")
        if self.config.validate_added_object and not self.validate_object(obj):
            raise ValidationFailedError(f"validation failed: {obj}")
        self.set_row_data(row, obj)

    def insert_object(self, row: int, obj: Dict[str, Any]):
        if self.config.validate_added_object and not self.validate_object(obj):
            raise ValidationFailedError(f"validation failed: {obj}")
        self.insert_row(row, obj)

    def remove_object(self, row: int) -> Dict[str, Any]:
        if row < 0 or row >= self.rowCount():
            raise IndexError(f"row index out of range: {row}")
        return self.remove_row(row)

    def clear_objects(self):
        self.remove_all_rows()

    def get_object(self, row: int) -> Dict[str, Any]:
        if row < 0 or row >= self.rowCount():
            raise IndexError(f"row index out of range: {row}")
        return self.get_row_data(row)

    def get_all_objects(self) -> List[Dict[str, Any]]:
        return self.get_all_row_data()

    def missing_keys(self, obj: Dict[str, Any]) -> List[str]:
        return self.missing_columns(obj)

    def fill_missing_keys_with_default(
        self, obj: Dict[str, Any], copy: bool = True
    ) -> Dict[str, Any]:
        if copy:
            obj = obj.copy()
        missing_keys = self.missing_keys(obj)
        if not missing_keys:
            return obj
        for key in missing_keys:
            vt = self._schema.get(key, None)
            if not vt:
                continue
            obj[key] = vt.default_value
        return obj

    def on_create_item(
        self, row: int, col: int
    ) -> Union[QTableWidgetItem, CellWidgetMixin]:
        key = self.column_keys[col]
        vt = self._schema.get(key, None)
        if not vt:
            return super().on_create_item(row, col)
        cell_widget = vt.create_cell_widget(self, row, col)
        if isinstance(cell_widget, CellWidgetMixin):
            return cell_widget
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
        vt = self._schema.get(self.column_keys[col], None)
        if not vt:
            return
        vt.after_insert_item(row, col, item)

    def on_set_item_data(self, row: int, col: int, data: Any):
        cell_widget = self.cellWidget(row, col)
        if isinstance(cell_widget, CellWidgetMixin):
            cell_widget.set_value(data)
            return
        super().on_set_item_data(row, col, data)
        vt = self._schema.get(self.column_keys[col], None)
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

    def validate_object(self, obj: Dict[str, Any]) -> bool:
        for key, value in obj.items():
            vt = self._schema.get(key, None)
            if not vt and not self.config.ignore_unknown_columns:
                return False
            if vt and not vt.validate(value):
                return False
        return True

    def _get_column_headers(self) -> Dict[str, str]:
        headers = {}
        for key, vt in self._schema.items():
            label = vt.display_name or key
            headers[key] = label
        return headers

    def _setup_columns(self):
        for column_index, column_key in enumerate(self.column_keys):
            # column_key = self.column_keys[column_index]
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
        vt: ValueType = self._item_double_clicked_handlers.get(column, None)
        if not vt:
            return
        item = self.item(row, column)
        data = self.on_get_item_data(row, column)
        vt.on_item_double_clicked(self, row, column, data, item)

    def _on_cell_clicked(self, row: int, column: int):
        if not self._item_clicked_handlers:
            return
        vt: ValueType = self._item_clicked_handlers.get(column, None)
        if not vt:
            return
        item = self.item(row, column)
        data = self.on_get_item_data(row, column)
        vt.on_item_clicked(self, row, column, data, item)
