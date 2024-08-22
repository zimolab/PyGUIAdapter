from __future__ import annotations

from typing import Tuple, List

import qtawesome as qta
from qtpy.QtCore import QSize, Qt, Signal, QModelIndex
from qtpy.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QWidget,
)

from ... import utils
from ...bundle import FnBundle

DEFAULT_FN_ICON = "fa5s.cubes"


class FnGroupPage(QWidget):
    current_bundle_changed = Signal(FnBundle, object)
    item_double_clicked = Signal(FnBundle, object)

    def __init__(
        self,
        parent: QWidget,
        icon_mode: bool,
        icon_size: Tuple[int, int] | QSize | None,
    ):
        super().__init__(parent)
        self._bundles: List[FnBundle] = []

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._listwidget = QListWidget(self)
        if icon_mode:
            self._listwidget.setViewMode(QListWidget.IconMode)
        else:
            self._listwidget.setViewMode(QListWidget.ListMode)

        if icon_size is not None:
            if isinstance(icon_size, tuple):
                icon_size = QSize(icon_size[0], icon_size[1])
            self._listwidget.setIconSize(icon_size)
        self._layout.addWidget(self._listwidget)

        # noinspection PyUnresolvedReferences
        self._listwidget.currentItemChanged.connect(self._on_current_item_change)
        # noinspection PyUnresolvedReferences
        self._listwidget.doubleClicked.connect(self._on_double_clicked)

    def add_bundle(self, bundle: FnBundle):
        if bundle in self._bundles:
            return
        item = self._create_bundle_item(bundle)
        self._bundles.append(bundle)
        self._listwidget.addItem(item)

        if not self.current_bundle():
            self.set_current_index(0)

    def bundles(self) -> Tuple[FnBundle, ...]:
        return tuple(self._bundles)

    def bundles_count(self):
        return self._listwidget.count()

    def bundle_at(self, index: int) -> FnBundle | None:
        item = self._listwidget.item(index)
        if item is None:
            return None
        bundle = item.data(Qt.UserRole)
        if isinstance(bundle, FnBundle):
            return bundle
        return None

    def bundle_index(self, bundle: FnBundle) -> int:
        for i in range(self._listwidget.count()):
            item = self._listwidget.item(i)
            if item is None:
                continue
            if item.data(Qt.UserRole) == bundle:
                return i
        return -1

    def current_bundle(self) -> FnBundle | None:
        current_item = self._listwidget.currentItem()
        if current_item is None:
            return None
        return current_item.data(Qt.UserRole)

    def set_current_index(self, index: int):
        self._listwidget.setCurrentRow(index)

    def remove_bundle(self, bundle: FnBundle):
        idx = self.bundle_index(bundle)
        if idx >= 0:
            item = self._listwidget.takeItem(idx)
            self._delete_item(item)
        if bundle in self._bundles:
            self._bundles.remove(bundle)

    def remove_bundle_at(self, index: int):
        bundle = self.bundle_at(index)
        if bundle is not None:
            item = self._listwidget.takeItem(index)
            self._delete_item(item)
        if bundle in self._bundles:
            self._bundles.remove(bundle)

    def clear_bundles(self):
        for i in range(self._listwidget.count()):
            item = self._listwidget.takeItem(i)
            self._delete_item(item)
        self._bundles.clear()

    @staticmethod
    def _delete_item(item: QListWidgetItem | None):
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
        self.current_bundle_changed.emit(bundle, self)

    def _on_double_clicked(self, index: QModelIndex):
        item = self._listwidget.item(index.row())
        if item is None:
            return
        bundle = item.data(Qt.UserRole)
        if not isinstance(bundle, FnBundle):
            return
        # noinspection PyUnresolvedReferences
        self.item_double_clicked.emit(bundle, self)

    def _create_bundle_item(self, bundle: FnBundle) -> QListWidgetItem:
        fn = bundle.fn_info
        icon = utils.get_icon(fn.icon) or qta.icon(DEFAULT_FN_ICON)
        item = QListWidgetItem(icon, fn.display_name, self._listwidget)
        item.setData(Qt.UserRole, bundle)
        return item
