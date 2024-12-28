from abc import abstractmethod
from typing import Optional

from qtpy.QtWidgets import QWidget

from ._view import ListView
from .._frame import CommonItemsViewFrameBase, ItemsViewFrameConfig
from .._itemeditor import ItemEditorBase


class ListViewFrameBase(CommonItemsViewFrameBase):

    def __init__(self, parent: Optional[QWidget], config: ItemsViewFrameConfig):
        self._listview: Optional[ListView] = None

        super().__init__(parent, config)

        self._update_buttons_state()

    @property
    def items_view(self) -> ListView:
        return self._listview

    def on_create_items_view(self) -> ListView:
        if not self._listview:
            self._listview = ListView(self)
            # noinspection PyUnresolvedReferences
            self._listview.itemSelectionChanged.connect(self._on_selection_changed)
        return self._listview

    @abstractmethod
    def create_add_item_editor(self) -> ItemEditorBase:
        pass

    @abstractmethod
    def create_edit_item_editor(self) -> ItemEditorBase:
        pass

    def _update_buttons_state(self):
        selected_rows = self._listview.get_selected_rows()
        has_selection = len(selected_rows) > 0
        self.edit_button.setEnabled(has_selection)
        self.remove_button.setEnabled(has_selection)
        self.move_up_button.setEnabled(has_selection)
        self.move_down_button.setEnabled(has_selection)

    def _on_selection_changed(self):
        self._update_buttons_state()
