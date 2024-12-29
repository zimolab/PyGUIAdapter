from abc import abstractmethod
from typing import Optional, List, Any, Tuple

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
)

from .ui_utilities import Widget, insert_widget


class BaseItemEditor(QDialog):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        center_container_title: str = "",
        dialog_button_box: bool = True,
        top_spacer: bool = True,
        bottom_spacer: bool = True,
    ):
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        if top_spacer:
            self._layout.addSpacerItem(
                QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )

        # center area
        self._center_container = QGroupBox(self)
        self._layout.addWidget(self._center_container, 9)

        if center_container_title:
            self._center_container.setTitle(center_container_title)

        self._center_layout = QVBoxLayout()
        self._center_container.setLayout(self._center_layout)
        # add center widget
        self._center_widget = self.on_create_center_widget(self._center_container)
        insert_widget(self._center_layout, -1, self._center_widget)

        # bottom area
        self._bottom_layout = QHBoxLayout()
        self._layout.addLayout(self._bottom_layout, 1)
        self._spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_layout.addSpacerItem(self._spacer)
        # add user widgets on bottom area
        for widget in self.user_bottom_widgets():
            insert_widget(self._bottom_layout, -1, widget)

        if dialog_button_box:
            self._dialog_button_box = QDialogButtonBox(self)
            self._dialog_button_box.setOrientation(Qt.Horizontal)
            self._dialog_button_box.setStandardButtons(
                QDialogButtonBox.Cancel | QDialogButtonBox.Ok
            )
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.accepted.connect(self.on_accept)
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.rejected.connect(self.on_reject)
            self._bottom_layout.addWidget(self._dialog_button_box)

        if bottom_spacer:
            self._layout.addSpacerItem(
                QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )

    @property
    def center_container(self) -> QGroupBox:
        return self._center_container

    @property
    def center_layout(self) -> QVBoxLayout:
        return self._center_layout

    @property
    def bottom_layout(self) -> QHBoxLayout:
        return self._bottom_layout

    def layout(self) -> QVBoxLayout:
        return self._layout

    @abstractmethod
    def user_bottom_widgets(self) -> List[Widget]:
        pass

    @abstractmethod
    def set_data(self, data: Any):
        pass

    @abstractmethod
    def get_data(self) -> Any:
        pass

    @abstractmethod
    def on_create_center_widget(self, parent: QWidget) -> QWidget:
        pass

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()

    def start(self, data: Any) -> Tuple[Any, bool]:
        self.set_data(data)
        ret = self.exec_()
        if ret == QDialog.Accepted:
            return self.get_data(), True
        else:
            return data, False


class BaseScrollableItemEditor(BaseItemEditor):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        center_container_title: str = "",
        dialog_button_box: bool = True,
    ):
        self._scroller: Optional[QScrollArea] = None
        self._scroller_content: Optional[QWidget] = None
        self._scroller_content_layout: Optional[QVBoxLayout] = None

        super().__init__(
            parent,
            center_container_title,
            dialog_button_box,
            top_spacer=False,
            bottom_spacer=False,
        )

    def user_bottom_widgets(self) -> List[Widget]:
        return []

    def on_create_center_widget(self, parent: QWidget) -> QScrollArea:
        if self._scroller is None:
            self._scroller = QScrollArea(parent)
            self._scroller.setWidgetResizable(True)
            self._scroller_content = QWidget(self._scroller)
            self._scroller.setWidget(self._scroller_content)
            self.on_create_item_widgets(self._scroller_content)
        return self._scroller

    @abstractmethod
    def set_data(self, data: Any):
        pass

    @abstractmethod
    def get_data(self) -> Any:
        pass

    @abstractmethod
    def on_create_item_widgets(self, parent: QWidget):
        pass
