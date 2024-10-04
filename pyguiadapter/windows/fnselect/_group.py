from typing import Tuple, List, Union, Optional

import qtawesome as qta
from qtpy.QtCore import QSize, Qt, Signal, QModelIndex
from qtpy.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QWidget,
)

from ...bundle import FnBundle
from ...utils import get_icon, get_size

DEFAULT_FN_ICON = "fa5s.cubes"


class FnGroupPage(QWidget):
    sig_current_bundle_changed = Signal(FnBundle, object)
    sig_item_double_clicked = Signal(FnBundle, object)

    def __init__(
        self,
        parent: QWidget,
        icon_mode: bool,
        icon_size: Union[Tuple[int, int], int, QSize, None],
    ):
        super().__init__(parent)
        self._bundles: List[FnBundle] = []

        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._fn_list_widget = QListWidget(self)
        self.set_icon_mode(icon_mode)
        self.set_icon_size(icon_size)
        self._layout.addWidget(self._fn_list_widget)

        # noinspection PyUnresolvedReferences
        self._fn_list_widget.currentItemChanged.connect(self._on_current_item_change)
        # noinspection PyUnresolvedReferences
        self._fn_list_widget.doubleClicked.connect(self._on_double_clicked)

        self.setLayout(self._layout)

    def set_icon_size(self, size: Union[int, Tuple[int, int], QSize]):
        if size is None:
            return
        size = get_size(size)
        if not size:
            raise ValueError(f"invalid icon size: {size}")
        self._fn_list_widget.setIconSize(size)

    def get_icon_size(self) -> Tuple[int, int]:
        size = self._fn_list_widget.iconSize()
        return size.width(), size.height()

    def set_icon_mode(self, enable: bool):
        if enable:
            self._fn_list_widget.setViewMode(QListWidget.IconMode)
        else:
            self._fn_list_widget.setViewMode(QListWidget.ListMode)

    def is_icon_mode(self) -> bool:
        return self._fn_list_widget.viewMode() == QListWidget.IconMode

    def add_bundle(self, bundle: FnBundle):
        if bundle in self._bundles:
            return
        item = self._create_bundle_item(bundle)
        self._bundles.append(bundle)
        self._fn_list_widget.addItem(item)

        if not self.current_bundle():
            self.set_current_index(0)

    def bundles(self) -> Tuple[FnBundle, ...]:
        return tuple(self._bundles)

    def bundles_count(self):
        return self._fn_list_widget.count()

    def bundle_at(self, index: int) -> Optional[FnBundle]:
        item = self._fn_list_widget.item(index)
        if item is None:
            return None
        bundle = item.data(Qt.UserRole)
        if isinstance(bundle, FnBundle):
            return bundle
        return None

    def bundle_index(self, bundle: FnBundle) -> int:
        for i in range(self._fn_list_widget.count()):
            item = self._fn_list_widget.item(i)
            if item is None:
                continue
            if item.data(Qt.UserRole) == bundle:
                return i
        return -1

    def current_bundle(self) -> Optional[FnBundle]:
        current_item = self._fn_list_widget.currentItem()
        if current_item is None:
            return None
        return current_item.data(Qt.UserRole)

    def set_current_index(self, index: int):
        self._fn_list_widget.setCurrentRow(index)

    def remove_bundle(self, bundle: FnBundle):
        idx = self.bundle_index(bundle)
        if idx >= 0:
            item = self._fn_list_widget.takeItem(idx)
            self._delete_item(item)
        if bundle in self._bundles:
            self._bundles.remove(bundle)

    def remove_bundle_at(self, index: int):
        bundle = self.bundle_at(index)
        if bundle is not None:
            item = self._fn_list_widget.takeItem(index)
            self._delete_item(item)
        if bundle in self._bundles:
            self._bundles.remove(bundle)

    def clear_bundles(self):
        for i in range(self._fn_list_widget.count()):
            item = self._fn_list_widget.takeItem(i)
            self._delete_item(item)
        self._bundles.clear()

    @staticmethod
    def _delete_item(item: Optional[QListWidgetItem]):
        if item is None:
            return
        item_widget = item.listWidget()
        if item_widget is not None:
            item_widget.deleteLater()

    def _on_current_item_change(self, current_item: QListWidgetItem):
        if current_item is None:
            return
        bundle = current_item.data(Qt.UserRole)
        if bundle is None:
            return
        # noinspection PyUnresolvedReferences
        self.sig_current_bundle_changed.emit(bundle, self)

    def _on_double_clicked(self, index: QModelIndex):
        item = self._fn_list_widget.item(index.row())
        if item is None:
            return
        bundle = item.data(Qt.UserRole)
        if not isinstance(bundle, FnBundle):
            return
        # noinspection PyUnresolvedReferences
        self.sig_item_double_clicked.emit(bundle, self)

    def _create_bundle_item(self, bundle: FnBundle) -> QListWidgetItem:
        fn = bundle.fn_info
        icon = get_icon(fn.icon) or qta.icon(DEFAULT_FN_ICON)
        item = QListWidgetItem(icon, fn.display_name, self._fn_list_widget)
        item.setData(Qt.UserRole, bundle)
        return item
