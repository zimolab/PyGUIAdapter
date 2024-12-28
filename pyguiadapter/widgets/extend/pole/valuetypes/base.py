import enum
from abc import abstractmethod
from typing import Optional, Any, Union

from qtpy.QtCore import QModelIndex
from qtpy.QtWidgets import QWidget, QStyleOptionViewItem, QLayout, QTableWidget


class ValueWidgetMixin(object):

    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def set_value(self, value: Any):
        pass

    def on_destroy(self):
        pass

    def cast_value(self, original_value: Any) -> Any:
        raise ValueError(f"invalid value: {original_value}")


class HookType(enum.Enum):
    ItemDelegate = 1
    CellDoubleClicked = 2


class ValueTypeBase(object):
    def __init__(self, default_value: Any):
        self._default_value = default_value

    @property
    def hook_type(self) -> HookType:
        return HookType.ItemDelegate

    @property
    def default_value(self) -> Any:
        return self._default_value

    @abstractmethod
    def on_create_editor(
        self,
        parent: QWidget,
        option: Optional[QStyleOptionViewItem],
        index: Optional[QModelIndex],
        **kwargs,
    ) -> Optional[QWidget]:
        pass

    @abstractmethod
    def on_create_edit(self, parent: QWidget, **kwargs) -> Union[QWidget, QLayout]:
        pass

    def on_cell_double_clicked(
        self, parent: QTableWidget, row: int, col: int, **kwargs
    ):
        pass
