from abc import abstractmethod
from typing import Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QDialogButtonBox,
    QWidget,
    QGroupBox,
    QAbstractButton,
)

from pyguiadapter.widgets.complex.itemsview_base import ItemsViewFrameBase

StandardButtons = QDialogButtonBox.StandardButtons

DEFAULT_DIALOG_BUTTONS = QDialogButtonBox.Ok | QDialogButtonBox.Cancel


class DialogBasedItemsViewEditor(QDialog):

    def __init__(
        self,
        parent: Optional[QWidget],
        dialog_buttons: Optional[StandardButtons] = DEFAULT_DIALOG_BUTTONS,
        items_view_title: Optional[str] = None,
    ):
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._container = QGroupBox(self)
        self._container.setTitle(items_view_title)
        self._layout.addWidget(self._container)

        self._container_layout = QVBoxLayout()
        self._container_layout.setContentsMargins(0, 0, 0, 0)
        self._container.setLayout(self._container_layout)

        self._items_view_frame = self.create_items_view_frame()
        self._container_layout.addWidget(self._items_view_frame)

        if dialog_buttons:
            self._dialog_button_box = QDialogButtonBox(self)
            self._dialog_button_box.setStandardButtons(dialog_buttons)
            self._dialog_button_box.clicked.connect(self.on_dialog_button_clicked)
            self._layout.addWidget(self._dialog_button_box)

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

    @property
    def items_view_frame(self) -> ItemsViewFrameBase:
        return self._items_view_frame

    @abstractmethod
    def create_items_view_frame(self) -> ItemsViewFrameBase:
        pass

    def on_dialog_button_clicked(self, button: QAbstractButton):
        pass
