import dataclasses
from typing import Optional, Dict, Any, List, Union, Tuple

from PySide2.QtWidgets import QTableWidgetItem
from qtpy.QtWidgets import QWidget

from ..itemsview_base import RowBasedTableView, TableViewConfig, TableViewItemDelegate
from ..schema import ValueTypeBase, ValueWidgetMixin


@dataclasses.dataclass
class ObjectsTableViewConfig(TableViewConfig):
    resize_row_to_contents: bool = True


class ObjectsTableView(RowBasedTableView):
    def __init__(
        self,
        parent: Optional[QWidget],
        column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]],
        schema: Dict[str, ValueTypeBase],
        config: ObjectsTableViewConfig,
        *args,
        **kwargs
    ):
        self._config = config
        self._schema = schema
        self._item_double_clicked_handlers: Dict[int, ValueTypeBase] = {}
        self._item_clicked_handlers: Dict[int, ValueTypeBase] = {}

        super().__init__(parent, column_headers, self._config, *args, **kwargs)

        self.cellDoubleClicked.connect(self._on_cell_double_clicked)
        self.cellClicked.connect(self._on_cell_clicked)

        self._setup_columns()

    def insert_row(
        self,
        row: int,
        row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]],
        ignore_unknown_columns: bool = False,
        *args,
        **kwargs
    ):
        super().insert_row(row, row_data, ignore_unknown_columns, *args, **kwargs)
        if self._config.resize_row_to_contents:
            self.resizeRowToContents(row)

    def create_item(
        self, row: int, column: int, item_data: Any
    ) -> Union[QTableWidgetItem, ValueWidgetMixin, None]:
        key = self.column_header_keys[column]
        vt = self._schema.get(key, None)
        if not vt:
            return super().create_item(row, column, item_data)
        cell_widget = vt.create_cell_widget(self, row, column, item_data)
        if not cell_widget:
            return super().create_item(row, column, item_data)
        self.setCellWidget(row, column, cell_widget)
        return None

    def get_item_data(self, row: int, column: int) -> Any:
        return super().get_item_data(row, column)

    def set_item_data(self, row: int, column: int, item_data: Any):
        return super().set_item_data(row, column, item_data)

    def _setup_columns(self):
        for column_index, column_key in enumerate(self.column_header_keys):
            column_key = self.column_header_keys[column_index]
            vt = self._schema[column_key]
            delegate = TableViewItemDelegate(self, vt)
            self.setItemDelegateForColumn(column_index, delegate)
            # hook events if needed
            if vt.hook_item_double_clicked():
                self._item_double_clicked_handlers[column_index] = vt

            if vt.hook_item_clicked():
                self._item_clicked_handlers[column_index] = vt

    def _on_cell_double_clicked(self, row: int, column: int):
        if not self._item_double_clicked_handlers:
            return
        vt: ValueTypeBase = self._item_double_clicked_handlers.get(column, None)
        if not vt:
            return
        item = self.item(row, column)
        data = self.get_item_data(row, column)
        vt.on_item_double_clicked(self, row, column, data, item)

    def _on_cell_clicked(self, row: int, column: int):
        if not self._item_clicked_handlers:
            return
        vt: ValueTypeBase = self._item_clicked_handlers.get(column, None)
        if not vt:
            return
        item = self.item(row, column)
        data = self.get_item_data(row, column)
        vt.on_item_clicked(self, row, column, data, item)
