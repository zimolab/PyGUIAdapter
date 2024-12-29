import dataclasses
from typing import Optional, Dict

from qtpy.QtWidgets import QWidget, QAbstractItemView

from ._view import ObjectTableView, ObjectTableViewConfig
from ..itemsview_base import ItemsViewFrameBase, ItemsViewFrameConfig
from ..schema import ValueTypeBase


@dataclasses.dataclass
class ObjectTableViewFrameConfig(ItemsViewFrameConfig):
    tableview_config: ObjectTableViewConfig = dataclasses.field(
        default_factory=ObjectTableViewConfig
    )


class ObjectTableViewFrame(ItemsViewFrameBase):

    def __init__(
        self,
        parent: Optional[QWidget],
        object_schema: Dict[str, ValueTypeBase],
        config: Optional[ObjectTableViewFrameConfig] = None,
    ):
        self._config = config or ObjectTableViewFrameConfig()

        self._object_schema = object_schema.copy()

        self._tableview: Optional[ObjectTableView] = None

        super().__init__(parent, self._config)

    @property
    def tableview(self) -> ObjectTableView:
        return self._tableview

    def on_create_items_view(self) -> QAbstractItemView:
        if not self._tableview:
            self._tableview = ObjectTableView(
                self, self._object_schema, config=self._config.tableview_config
            )
        return self._tableview

    def _setup_ui(self):
        super()._setup_ui()

    def on_add_button_clicked(self):
        pass

    def on_remove_button_clicked(self):
        pass

    def on_clear_button_clicked(self):
        pass

    def on_move_up_button_clicked(self):
        pass

    def on_move_down_button_clicked(self):
        pass
