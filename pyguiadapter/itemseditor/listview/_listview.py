from typing import Optional, Any, List

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QListWidget, QWidget, QListWidgetItem

from ..itemsview import CommonItemsViewInterface
from ._config import ListViewConfig


class ListView(QListWidget, CommonItemsViewInterface):
    def __init__(self, parent: Optional[QWidget], config: ListViewConfig):
        self._config = config
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self):
        self.setSelectionMode(QListWidget.ContiguousSelection)
        self.setAlternatingRowColors(self.config.alternating_row_colors)

    @property
    def config(self) -> ListViewConfig:
        return self._config

    def row_count(self) -> int:
        return self.count()

    def select_row(self, row: int):
        item = self.item(row)
        if item is not None:
            item.setSelected(True)
            return
        raise IndexError(f"index out of range: {row}")

    def get_selected_rows(self, sort=False, reverse=False) -> List[int]:
        rows = [index.row() for index in self.selectedIndexes()]
        if rows and sort:
            rows.sort(reverse=reverse)
        return rows

    def clear_selection(self):
        self.clearSelection()

    def on_create_item(self, row: int, col: int) -> Any:
        return QListWidgetItem()

    def on_insert_item(self, row: int, col: int, item: QListWidgetItem):
        if not isinstance(item, QListWidgetItem):
            raise TypeError(f"unexpected list item type: {type(item)}")
        self.insertItem(row, item)

    def on_set_item_data(self, row: int, col: int, value: Any):
        item = self.item(row)
        if not item:
            raise IndexError(f"index out of range: {row}")
        # set text and user data of the item
        display_text = str(value) if value is not None else ""
        item.setText(display_text)
        item.setData(Qt.UserRole, value)

        # set properties of the item
        flags = item.flags()
        if self.config.item_editable:
            flags |= Qt.ItemIsEditable
        item.setFlags(flags)

        if self.config.item_text_alignment is not None:
            item.setTextAlignment(self.config.item_text_alignment)

        if self.config.item_data_as_tooltip:
            item.setToolTip(display_text)

        if self.config.item_data_as_status_tip:
            item.setStatusTip(display_text)

    def on_get_item_data(self, row: int, col: int) -> Any:
        item = self.item(row)
        if item is None:
            raise IndexError(f"index out of range: {row}")
        return item.data(Qt.UserRole)

    def on_remove_item(self, row: int, col: int) -> Any:
        item = self.takeItem(row)
        if item is None:
            raise IndexError(f"index out of range: {row}")
        data = item.data(Qt.UserRole)
        self.removeItemWidget(item)
        del item
        return data
