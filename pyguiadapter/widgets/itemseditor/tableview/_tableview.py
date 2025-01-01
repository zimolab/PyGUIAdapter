from typing import Optional, Any, List, Union, Tuple, Dict

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QTableWidget, QAbstractItemView, QWidget, QTableWidgetItem

from ._config import TableViewConfig
from ..exceptions import InsufficientColumnsError, UnexpectedColumnError
from ..itemsview import CommonItemsViewInterface


class TableView(QTableWidget, CommonItemsViewInterface):
    def __init__(
        self,
        parent: Optional[QWidget],
        column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]],
        config: TableViewConfig,
    ):

        super().__init__(parent)
        self._config = config
        self._column_headers: Dict[str, str] = {}
        self._setup_ui()
        self.reset_view(column_headers)

    @property
    def config(self) -> TableViewConfig:
        return self._config

    @property
    def column_headers(self) -> Dict[str, str]:
        return self._column_headers.copy()

    @property
    def column_keys(self) -> List[str]:
        return list(self._column_headers.keys())

    @property
    def column_labels(self) -> List[str]:
        return list(self._column_headers.values())

    def reset_view(
        self, column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]]
    ):
        self._column_headers.clear()
        self._column_headers.update(self._normalize_column_headers(column_headers))
        self.remove_all_rows()
        self.setColumnCount(len(self._column_headers))
        self.setHorizontalHeaderLabels(self.column_labels)

    def row_count(self) -> int:
        return self.rowCount()

    def select_row(self, row: int):
        self.selectRow(row)

    def insert_row(
        self, row: int, row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]]
    ):

        self._check_missing_columns(row_data)
        self._check_unknown_columns(row_data)

        self.insertRow(row)

        if isinstance(row_data, (list, tuple)):
            for col, value in enumerate(row_data):
                item = self.on_create_item(row, col)
                self.on_insert_item(row, col, item)
                self.on_set_item_data(row, col, value)
        else:
            for col_key, value in row_data.items():
                col = self.index_of_column_key(col_key)
                if col < 0:
                    continue
                item = self.on_create_item(row, col)
                self.on_insert_item(row, col, item)
                self.on_set_item_data(row, col, value)

        if self.config.resize_rows_to_contents:
            self.resizeRowsToContents()

    def remove_all_rows(self):
        super().remove_all_rows()
        self.clearContents()
        self.setRowCount(0)

    def append_row(self, row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]]):
        super().append_row(row_data)

    def get_row_data(
        self, row: int
    ) -> Union[List[Any], Tuple[Any, ...], Dict[str, Any]]:
        if self.config.row_data_type == "list":
            return [
                self.on_get_item_data(row, col) for col in range(self.columnCount())
            ]
        elif self.config.row_data_type == "tuple":
            return tuple(
                self.on_get_item_data(row, col) for col in range(self.columnCount())
            )
        elif self.config.row_data_type == "dict":
            return {
                col_key: self.on_get_item_data(row, col)
                for col, col_key in enumerate(self._column_headers.keys())
            }
        else:
            raise ValueError(f"unsupported row data type: {self.config.row_data_type}")

    def set_row_data(
        self, row: int, row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]]
    ):
        self._check_missing_columns(row_data)
        self._check_unknown_columns(row_data)
        if isinstance(row_data, (list, tuple)):
            for col, value in enumerate(row_data):
                self.on_set_item_data(row, col, value)
        else:
            for col_key, value in row_data.items():
                col = self.index_of_column_key(col_key)
                if col < 0:
                    continue
                self.on_set_item_data(row, col, value)

    def remove_row(self, row: int) -> Any:
        row_data = self.get_row_data(row)
        for col in range(self.columnCount()):
            self.on_remove_item(row, col)
        self.removeRow(row)
        return row_data

    def get_selected_rows(self, sort: bool = False, reverse: bool = False) -> List[int]:
        rows = list({index.row() for index in self.selectedIndexes()})
        if rows and sort:
            rows.sort(reverse=reverse)
        return rows

    def clear_selection(self):
        self.clearSelection()

    def on_create_item(self, row: int, col: int) -> QTableWidgetItem:
        return QTableWidgetItem()

    def on_insert_item(self, row: int, col: int, item: QTableWidgetItem):
        self.setItem(row, col, item)

    def on_set_item_data(self, row: int, col: int, value: Any):
        item = self.item(row, col)
        if item is None:
            raise ValueError(f"item not found at row {row}, col {col}")

        display_text = str(value)
        item.setText(display_text)

        item.setData(Qt.UserRole, value)

        if self.config.item_text_alignment is not None:
            item.setTextAlignment(self.config.item_text_alignment)

        if self.config.item_data_as_tooltip:
            item.setToolTip(display_text)

        if self.config.item_data_as_status_tip:
            item.setStatusTip(display_text)

    def on_get_item_data(self, row: int, col: int) -> Any:
        item = self.item(row, col)
        if item is None:
            raise ValueError(f"item not found at row {row}, col {col}")
        data = item.data(Qt.UserRole)
        return data

    def on_remove_item(self, row: int, col: int) -> Any:
        item = self.takeItem(row, col)
        data = item.data(Qt.UserRole)
        del item
        return data

    def missing_columns(self, row_data: Dict[str, Any]) -> List[str]:
        missing = []
        for col in self._column_headers.keys():
            if col not in row_data:
                missing.append(col)
        return missing

    def unknown_columns(self, row_data: Dict[str, Any]) -> List[str]:
        unknown = []
        for col in row_data.keys():
            if col not in self._column_headers.keys():
                unknown.append(col)
        return unknown

    def index_of_column_key(self, column_key: str) -> int:
        column_keys = list(self._column_headers.keys())
        for i in range(len(column_keys)):
            if column_keys[i] == column_key:
                return i
        return -1

    def index_of_column_label(self, column_label: str) -> int:
        column_labels = list(self._column_headers.values())
        for i in range(len(column_labels)):
            if column_labels[i] == column_label:
                return i
        return -1

    def _check_missing_columns(
        self, row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]]
    ) -> None:
        if not isinstance(row_data, (list, tuple, dict)):
            raise TypeError("row_data must be a list, tuple, or dict")

        # check length first
        expected = self.columnCount()
        provided = len(row_data)
        if provided < expected:
            raise InsufficientColumnsError(
                f"missing columns in row data, {expected} expected, {provided} provided"
            )

        # check if there are any missing columns when row_data is a dict
        if not isinstance(row_data, dict):
            return
        missing_cols = self.missing_columns(row_data)
        if missing_cols:
            raise InsufficientColumnsError(f"missing columns: {missing_cols}")

    def _check_unknown_columns(
        self, row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]]
    ) -> None:
        if self.config.ignore_unknown_columns:
            return
        if not isinstance(row_data, dict):
            return
        unknown_cols = self.unknown_columns(row_data)
        if unknown_cols:
            raise UnexpectedColumnError(f"unknown columns: {unknown_cols}")

    def _setup_ui(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setShowGrid(self.config.show_grid)
        self.setAlternatingRowColors(self.config.alternating_row_colors)

        self.horizontalHeader().setVisible(self.config.show_horizontal_header)
        self.verticalHeader().setVisible(self.config.show_vertical_header)

        if self.config.continuous_selection:
            self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        else:
            self.setSelectionMode(QAbstractItemView.SingleSelection)

        if self.config.stretch_last_section:
            self.horizontalHeader().setStretchLastSection(True)

    @staticmethod
    def _normalize_column_headers(
        column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]]
    ):
        if isinstance(column_headers, dict):
            return column_headers
        elif isinstance(column_headers, (list, tuple)):
            return {key: key for key in column_headers}
        else:
            raise TypeError("column_headers must be a list, tuple, or dict")
