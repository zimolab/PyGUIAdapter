from typing import Optional, Union

from qtpy.QtCore import Qt, QModelIndex, QAbstractItemModel
from qtpy.QtWidgets import QWidget, QStyledItemDelegate, QStyleOptionViewItem

from ._value_type import ValueTypeBase
from ._widget_mixin import ValueWidgetMixin


class ValueTypeItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: QWidget, vt: ValueTypeBase):
        super().__init__(parent)
        self._vt = vt

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        return self._vt.create_item_delegate_widget(parent, option=option, index=index)

    def setEditorData(
        self, editor: Union[QWidget, ValueWidgetMixin], index: QModelIndex
    ) -> None:
        if not editor:
            return
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
        model.setData(index, value, Qt.EditRole)
