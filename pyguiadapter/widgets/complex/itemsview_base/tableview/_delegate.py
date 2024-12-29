from typing import Optional, Union

from qtpy.QtCore import Qt, QModelIndex, QAbstractItemModel
from qtpy.QtWidgets import QWidget, QStyledItemDelegate, QStyleOptionViewItem

from ...schema import ValueTypeBase, ValueWidgetMixin
from ._view import TableView


class TableViewItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: Union[QWidget, TableView], vt: ValueTypeBase):
        super().__init__(parent)
        self._vt = vt
        self._parent = parent

    def createEditor(
        self,
        parent: Union[QWidget, TableView],
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> Optional[QWidget]:
        return self._vt.create_item_delegate_widget(parent, option=option, index=index)

    def setEditorData(
        self, editor: Union[QWidget, ValueWidgetMixin], index: QModelIndex
    ) -> None:
        if not editor:
            return
        if isinstance(self._parent, TableView):
            data = self._parent.get_item_data(index.row(), index.column())
        else:
            data = index.data(Qt.EditRole)
        editor.set_value(data)

    def setModelData(
        self,
        editor: Union[QWidget, ValueWidgetMixin],
        model: QAbstractItemModel,
        index: QModelIndex,
    ) -> None:
        if not editor:
            return
        value = editor.get_value()
        if isinstance(self._parent, TableView):
            self._parent.set_item_data(index.row(), index.column(), value)
        else:
            model.setData(index, value, Qt.EditRole)
