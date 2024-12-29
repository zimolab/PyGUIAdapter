from typing import Optional, Any, List

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QListWidget, QWidget, QListWidgetItem

from .._itemsview import ItemsViewInterface


class ListView(QListWidget, ItemsViewInterface):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setSelectionMode(QListWidget.ContiguousSelection)

    def insert_row(self, row: int, row_data: Any, *args, **kwargs):
        row_item = QListWidgetItem()
        row_item.setText(str(row_data))
        row_item.setData(Qt.UserRole, row_data)
        self.insertItem(row, row_item)

    def append_row(self, row_data: Any, *args, **kwargs):
        row = self.row_count()
        self.insert_row(row, row_data)

    def get_row_data(self, row: int, *args, **kwargs) -> Any:
        item = self.item(row)
        return item.data(Qt.UserRole)

    def get_all_row_data(self, *args, **kwargs) -> List[Any]:
        return [self.get_row_data(row) for row in range(self.row_count())]

    def set_row_data(self, row: int, row_data: Any, *args, **kwargs):
        row_item = self.item(row)
        row_item.setText(str(row_data))
        row_item.setData(Qt.UserRole, row_data)

    def remove_row(self, row: int, *args, **kwargs) -> Any:
        item = self.takeItem(row)
        data = item.data(Qt.UserRole)
        self.removeItemWidget(item)
        return data

    def remove_all_rows(self, *args, **kwargs):
        indexes = list(range(self.row_count()))
        for index in reversed(indexes):
            self.remove_row(index)
        self.clear()

    def row_count(self, *args, **kwargs) -> int:
        return self.count()

    def select_row(self, row: int, *args, **kwargs):
        item = self.item(row)
        item.setSelected(True)

    def get_selected_rows(
        self, sort: bool = False, reverse: bool = False, *args, **kwargs
    ) -> List[int]:
        rows = [index.row() for index in self.selectedIndexes()]
        if rows and sort:
            rows.sort(reverse=reverse)
        return rows

    def clear_selection(self, *args, **kwargs):
        self.clearSelection()
