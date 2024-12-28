from typing import Optional, Union

from qtpy.QtCore import QModelIndex, QAbstractItemModel
from qtpy.QtWidgets import QWidget, QStyleOptionViewItem


from ..schema import ValueTypeItemDelegate, ValueTypeBase, ValueWidgetMixin
from ._commons import _KEY_COLUMN


class ValueDelegate(ValueTypeItemDelegate):
    def __init__(self, parent: QWidget, value_type: ValueTypeBase):
        super().__init__(parent, value_type)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        if index.column() == _KEY_COLUMN:
            return None
        return super().createEditor(parent, option, index)

    def setEditorData(
        self, editor: Union[QWidget, ValueWidgetMixin], index: QModelIndex
    ) -> None:
        if index.column() == _KEY_COLUMN:
            return
        super().setEditorData(editor, index)

    def setModelData(
        self,
        editor: Union[QWidget, ValueWidgetMixin],
        model: QAbstractItemModel,
        index: QModelIndex,
    ) -> None:
        if index.column() == _KEY_COLUMN:
            return
        super().setModelData(editor, model, index)
