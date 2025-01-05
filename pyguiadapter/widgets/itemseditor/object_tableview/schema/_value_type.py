from abc import abstractmethod
from typing import Any, Union, Dict, Optional

from qtpy.QtCore import QModelIndex
from qtpy.QtWidgets import QWidget, QTableWidgetItem

from ._widget_mixin import ValueWidgetMixin, CellWidgetMixin
from ...exceptions import ValidationFailedError
from ...tableview import TableView


class ValueType(object):

    def __init__(self, default_value: Any, *, display_name: Optional[str] = None):

        if not self.validate(default_value):
            raise ValidationFailedError(f"invalid default value: {default_value}")

        self._default_value = default_value
        self._display_name = display_name

    @property
    def default_value(self) -> Any:
        return self._default_value

    @property
    def display_name(self) -> Optional[str]:
        return self._display_name

    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass

    # noinspection PyMethodMayBeStatic
    def hook_item_double_clicked(self) -> bool:
        return False

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def hook_item_clicked(self) -> bool:
        return False

    @abstractmethod
    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        pass

    @abstractmethod
    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        pass

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def create_cell_widget(
        self, parent: QWidget, row: int, col: int, *args, **kwargs
    ) -> Union[QWidget, CellWidgetMixin, None]:
        return None

    def on_item_double_clicked(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        pass

    def on_item_clicked(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        pass

    def before_set_editor_data(
        self,
        parent: TableView,
        editor: Union[QWidget, ValueWidgetMixin],
        index: QModelIndex,
    ):
        pass

    def after_create_item(self, row: int, col: int, item: QTableWidgetItem):
        pass

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        pass

    def after_insert_item(self, row: int, col: int, item: QTableWidgetItem):
        pass


def default_object(schema: Dict[str, ValueType]) -> Dict[str, Any]:
    return {k: v.default_value for k, v in schema.items()}
