import dataclasses
from typing import Optional, List, Any, Tuple, Union, Dict, Literal

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QWidget,
)

from .._itemsview import ItemsViewInterface
from ...schema import CellWidgetMixin


@dataclasses.dataclass
class TableViewConfig(object):
    vertical_header_visible: bool = True
    horizontal_header_visible: bool = True
    continuous_selection: bool = True
    alternating_row_colors: bool = False
    stretch_last_column: bool = True
    show_grid_lines: bool = True
    no_focus: bool = False
    item_text_alignment: Optional[Qt.Alignment] = Qt.AlignCenter


class TableView(QTableWidget):
    def __init__(
        self, parent: Optional[QWidget], config: TableViewConfig, *args, **kwargs
    ):

        self._config = config
        super().__init__(parent)

        self._setup_ui()

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def create_item(
        self, row: int, column: int, item_data: Any
    ) -> Union[QTableWidgetItem, CellWidgetMixin]:
        item = QTableWidgetItem()
        self.setItem(row, column, item)
        return item

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def set_item_data(self, row: int, column: int, item_data: Any):
        cell_widget = self.cell_value_widget(row, column)
        if isinstance(cell_widget, CellWidgetMixin):
            cell_widget.set_value(item_data)
            return

        item = self.item(row, column)
        if item is None:
            raise ValueError(f"no item found at row {row}, column {column}")

        item.setText(str(item_data))
        item.setData(Qt.EditRole, item_data)

        if self._config.item_text_alignment is not None:
            item.setTextAlignment(self._config.item_text_alignment)

    def get_item_data(self, row: int, column: int) -> Any:
        cell_widget = self.cell_value_widget(row, column)
        if isinstance(cell_widget, CellWidgetMixin):
            return cell_widget.get_value()
        item = self.item(row, column)
        if item is None:
            raise ValueError(f"no item found at row {row}, column {column}")
        return item.data(Qt.EditRole)

    def cell_value_widget(self, row: int, column: int) -> Optional[CellWidgetMixin]:
        cell_widget = self.cellWidget(row, column)
        if isinstance(cell_widget, CellWidgetMixin):
            return cell_widget
        return None

    def _setup_ui(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        if self._config.continuous_selection:
            self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        else:
            self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setShowGrid(self._config.show_grid_lines)
        if self._config.no_focus:
            self.setFocusPolicy(Qt.NoFocus)
        self.horizontalHeader().setStretchLastSection(self._config.stretch_last_column)
        self.setAlternatingRowColors(self._config.alternating_row_colors)
        self.verticalHeader().setVisible(self._config.vertical_header_visible)
        self.horizontalHeader().setVisible(self._config.horizontal_header_visible)


class RowBasedTableView(TableView, ItemsViewInterface):
    """
    Once the column headers are given, the table view will be created with the certain column count with the certain
    header labels. Don't try to change the columns after the table view is created, including adding/removing columns,
    changing the order of columns, or changing the header of a column.

    If you want to change the column headers, you should create a new table view with the new column headers or use the
    `reset_view()` method. Be aware that the `reset_view()` method will remove all the data in the table view. It is the
    responsibility of the caller to save the data before calling `reset_view()` and restore it afterward.
    """

    def __init__(
        self,
        parent: Optional[QWidget],
        column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]],
        config: TableViewConfig,
        *args,
        **kwargs,
    ):
        """
        When `column_headers` is a dictionary, it means a set of "column_label_text" to "column_key" pairs. The
        "column_key" will be used to access(get/set/remove...) the data in the row data. And the "column_label_text"
        will be shown in the table view as the column header.

        When `column_headers` is a list or a tuple, the "column_label_text" will be the same as the "column_key".
        """
        self._config = config
        self._column_headers: Dict[str, str] = {}

        super().__init__(parent, self._config, *args, **kwargs)

        self.reset_view(column_headers, self._config)

    @property
    def column_headers(self) -> Dict[str, str]:
        return self._column_headers.copy()

    @property
    def column_header_labels(self) -> Tuple[str, ...]:
        return tuple(self._column_headers.values())

    @property
    def column_header_keys(self) -> Tuple[str, ...]:
        return tuple(self._column_headers.keys())

    def column_count(self) -> int:
        return self.columnCount()

    def reset_view(
        self,
        column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]],
        config: TableViewConfig,
    ):
        self._config = config
        if isinstance(column_headers, (list, tuple)):
            column_headers = {h: h for h in column_headers}
        self._column_headers.clear()
        self._column_headers = column_headers
        self.remove_all_rows()
        self.clear()  # this will also remove the column headers
        # reset the columns
        self.setColumnCount(len(self._column_headers))
        self.setHorizontalHeaderLabels(list(self._column_headers.values()))

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

    def index_of_column(self, column: str) -> int:
        for header, i in enumerate(self._column_headers.keys()):
            if self._column_headers[i] == column:
                return header
        return -1

    def insert_row(
        self,
        row: int,
        row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]],
        ignore_unknown_columns: bool = False,
        *args,
        **kwargs,
    ):
        if not isinstance(row_data, (list, tuple, dict)):
            raise TypeError(f"unsupported row data type: {type(row_data)}")

        required = self.column_count()
        provided = len(row_data)
        if provided < required:
            raise ValueError(
                f"insufficient data: {required} columns expected, {provided} provided"
            )
        self.insertRow(row)
        # for dictionary
        if isinstance(row_data, dict):
            missing = self.missing_columns(row_data)
            # check if all required columns are present
            if missing:
                raise ValueError(f"missing data for columns: {missing}")
            # check if there are any unknown columns if ignore_unknown_columns is False
            if not ignore_unknown_columns:
                unknown = self.unknown_columns(row_data)
                if unknown:
                    raise ValueError(f"unknown columns: {unknown}")

            for col_key, item_data in row_data.items():
                col = self.index_of_column(col_key)
                if col < 0:
                    continue
                self.create_item(row, col, item_data)
                self.set_item_data(row, col, item_data)

            return
        # for list or tuple, assume all columns are present and in the same order as the column headers
        for col, item_data in enumerate(row_data):
            self.create_item(row, col, item_data)
            self.set_item_data(row, col, item_data)

    def append_row(
        self, row_data: Any, ignore_unknown_columns: bool = False, *args, **kwargs
    ):
        self.insert_row(
            self.row_count(),
            row_data,
            ignore_unknown_columns=ignore_unknown_columns,
            *args,
            **kwargs,
        )

    def get_row_data(
        self,
        row: int,
        row_data_type: Literal["tuple", "dict"] = "dict",
        *args,
        **kwargs,
    ) -> Union[Tuple[Any, ...], Dict[str, Any]]:
        if row_data_type not in ["tuple", "dict"]:
            raise ValueError(f"unsupported row data type: {row_data_type}")
        if row < 0 or row >= self.row_count():
            raise IndexError(f"row out of range: {row}")
        if row_data_type == "tuple":
            return tuple(
                self.get_item_data(row, col) for col in range(self.column_count())
            )

        return {
            col_key: self.get_item_data(row, col)
            for col, col_key in enumerate(self._column_headers.keys())
        }

    def get_all_row_data(
        self, row_data_type: Literal["tuple", "dict"] = "dict", *args, **kwargs
    ) -> List[Union[Tuple[Any, ...], Dict[str, Any]]]:
        return [
            self.get_row_data(row, row_data_type, *args, **kwargs)
            for row in range(self.row_count())
        ]

    def set_row_data(
        self,
        row: int,
        row_data: Union[List[Any], Tuple[Any, ...], Dict[str, Any]],
        ignore_unknown_columns: bool = False,
        *args,
        **kwargs,
    ):
        if not isinstance(row_data, (list, tuple, dict)):
            raise TypeError(f"unsupported row data type: {type(row_data)}")
        if row < 0 or row >= self.row_count():
            raise IndexError(f"row out of range: {row}")
        required = self.column_count()
        provided = len(row_data)
        if provided < required:
            raise ValueError(
                f"insufficient data: {required} columns expected, {provided} provided"
            )
        # for dictionary
        if isinstance(row_data, dict):
            missing = self.missing_columns(row_data)
            # check if all required columns are present
            if missing:
                raise ValueError(f"missing data for columns: {missing}")
            # check if there are any unknown columns if ignore_unknown_columns is False
            if not ignore_unknown_columns:
                unknown = self.unknown_columns(row_data)
                if unknown:
                    raise ValueError(f"unknown columns: {unknown}")
            for col_key, item_data in row_data.items():
                col = self.index_of_column(col_key)
                if col < 0:
                    continue
                self.set_item_data(row, col, item_data)
            return
        # for list or tuple, assume all columns are present and in the same order as the column headers
        for col, item_data in enumerate(row_data):
            self.set_item_data(row, col, item_data)

    def remove_row(
        self,
        row: int,
        row_data_type: Literal["tuple", "dict"] = "dict",
        *args,
        **kwargs,
    ) -> Union[Tuple[Any, ...], Dict[str, Any]]:
        if row < 0 or row >= self.row_count():
            raise IndexError(f"row out of range: {row}")

    def remove_all_rows(self, *args, **kwargs):
        if self.row_count() <= 0:
            return
        self.clearSelection()
        # remove all rows by iterating from the last row to the first row
        for row in range(self.row_count() - 1, -1, -1):
            self.remove_row(row, *args, **kwargs)
        # just in case
        self.setRowCount(0)

    def row_count(self, *args, **kwargs) -> int:
        return self.rowCount()

    def select_row(self, row: int, *args, **kwargs):
        if row < 0 or row >= self.row_count():
            raise IndexError(f"row out of range: {row}")
        self.selectRow(row)

    def get_selected_rows(
        self, sort: bool = False, reverse: bool = False, *args, **kwargs
    ) -> List[int]:
        rows = list({index.row() for index in self.selectedIndexes()})
        if rows and sort:
            rows.sort(reverse=reverse)
        return rows

    def clear_selection(self, *args, **kwargs):
        self.clearSelection()
