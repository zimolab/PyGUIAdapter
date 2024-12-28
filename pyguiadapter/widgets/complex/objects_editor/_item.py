from typing import Any, Dict

from qtpy.QtWidgets import QWidget, QGridLayout, QLabel, QSpacerItem, QSizePolicy

from ..itemsview_base import ScrollableItemEditorBase
from ..schema import ValueTypeBase, ValueWidgetMixin


class ObjectItemEditor(ScrollableItemEditorBase):

    def __init__(self, parent: QWidget, object_schema: Dict[str, ValueTypeBase]):
        self._object_schema = object_schema
        self._widgets: Dict[str, ValueWidgetMixin] = {}
        super().__init__(parent)
        self.resize(500, 600)

    def set_data(self, data: Dict[str, Any]):
        if not data:
            return
        for key, value in data.items():
            if key in self._widgets:
                self._widgets[key].set_value(value)

    def get_data(self) -> Dict[str, Any]:
        data = {}
        for key, widget in self._widgets.items():
            data[key] = widget.get_value()
        return data

    def on_create_item_widgets(self, parent: QWidget):
        layout = QGridLayout()
        for i, (key, vt) in enumerate(self._object_schema.items()):
            label = QLabel(key, parent)
            layout.addWidget(label, i, 0)
            edit = vt.create_item_editor_widget(parent)
            layout.addWidget(edit, i, 1)
            self._widgets[key] = edit
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        parent.setLayout(layout)
