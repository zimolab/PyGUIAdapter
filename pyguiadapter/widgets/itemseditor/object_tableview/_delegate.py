from typing import Optional, Union

from qtpy.QtCore import Qt, QModelIndex, QAbstractItemModel
from qtpy.QtWidgets import (
    QWidget,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)

from ._commons import KEY_COLUMN_INDEX
from ..schema import ValueType, ValueWidgetMixin
from ..tableview import TableView


class ObjectItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: Union[QWidget, TableView], vt: ValueType):
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
        self._vt.before_set_editor_data(self._parent, editor, index)
        if isinstance(self._parent, TableView):
            data = self._parent.on_get_item_data(index.row(), index.column())
        else:
            data = index.data(Qt.UserRole)
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
            self._parent.on_set_item_data(index.row(), index.column(), value)
        else:
            model.setData(index, value, Qt.UserRole)


class KeyValueDelegate(ObjectItemDelegate):
    def __init__(self, parent: QWidget, value_type: ValueType):
        super().__init__(parent, value_type)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        if index.column() == KEY_COLUMN_INDEX:
            return None
        return super().createEditor(parent, option, index)

    def setEditorData(
        self, editor: Union[QWidget, ValueWidgetMixin], index: QModelIndex
    ) -> None:
        if index.column() == KEY_COLUMN_INDEX:
            return
        super().setEditorData(editor, index)

    def setModelData(
        self,
        editor: Union[QWidget, ValueWidgetMixin],
        model: QAbstractItemModel,
        index: QModelIndex,
    ) -> None:
        if index.column() == KEY_COLUMN_INDEX:
            return
        super().setModelData(editor, model, index)
