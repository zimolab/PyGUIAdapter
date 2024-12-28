import dataclasses
from abc import abstractmethod
from typing import Optional, List, Tuple, Union, Dict

from qtpy.QtWidgets import QAbstractItemView, QWidget

from ._view import TableViewConfig, RowBasedTableView
from .._frame import CommonItemsViewFrameBase, ItemsViewFrameConfig
from .._itemeditor import ItemEditorBase


@dataclasses.dataclass
class RowBasedTableViewFrameConfig(ItemsViewFrameConfig):
    tableview_config: TableViewConfig = dataclasses.field(
        default_factory=TableViewConfig
    )


class RowBasedTableViewFrameBase(CommonItemsViewFrameBase):

    def __init__(
        self,
        parent: Optional[QWidget],
        column_headers: Union[List[str], Tuple[str, ...], Dict[str, str]],
        config: Optional[RowBasedTableViewFrameConfig] = None,
    ):
        self._config = config or RowBasedTableViewFrameConfig()
        self._tableview: Optional[RowBasedTableView] = None
        self._column_headers = column_headers

        super().__init__(parent, config=self._config)

        self._update_buttons_state()

    @property
    def items_view(self) -> RowBasedTableView:
        return self._tableview

    @abstractmethod
    def create_add_item_editor(self) -> ItemEditorBase:
        pass

    @abstractmethod
    def create_edit_item_editor(self) -> ItemEditorBase:
        pass

    def on_create_items_view(self) -> QAbstractItemView:
        if self._tableview is None:
            self._tableview = RowBasedTableView(
                self,
                column_headers=self._column_headers,
                config=self._config.tableview_config,
            )
            self._tableview.itemSelectionChanged.connect(self._on_selection_changed)

        return self._tableview

    def _on_selection_changed(self):
        self._update_buttons_state()

    def _update_buttons_state(self):
        selected_rows = self._tableview.get_selected_rows()
        has_selection = len(selected_rows) > 0
        self.edit_button.setEnabled(has_selection)
        self.remove_button.setEnabled(has_selection)
        self.move_up_button.setEnabled(has_selection)
        self.move_down_button.setEnabled(has_selection)
