"""
This module implements a universal ItemViewFrameBase class which has the following layout structure:

┌─────────────────────────────────────────────────────────────────────┐
│   ┌─────────────────────────────────────────────┐ ┌───────────────┐ │
│   │                                             │ │               │ │
│   │                                             │ │ Top Widgets   │ │
│   │                                             │ │    Area       │ │
│   │                                             │ │               │ │
│   │                                             │ │               │ │
│   │                                             │ │               │ │
│   │                                             │ │ Side Widgets  │ │
│   │            Item View Area                   │ │     Area      │ │
│   │                                             │ │               │ │
│   │                                             │ │               │ │
│   │                                             │ │ Bottom Widgets│ │
│   │                                             │ │      Area     │ │
│   │                                             │ │               │ │
│   │                                             │ │               │ │
│   │                                             │ │               │ │
│   │                                             │ │               │ │
│   └─────────────────────────────────────────────┘ └───────────────┘ │
│                          The   Frame                                │
└─────────────────────────────────────────────────────────────────────┘

It also provides a subclass of ItemViewFrameBase called CommonItemsViewFrameBase which contains a group of commonly used
buttons such as "Add", "Edit", "Clear", "Up", "Down", in the side widgets area.

"""

import dataclasses
from abc import abstractmethod
from typing import Optional, Literal, Any

from qtpy.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QAbstractItemView,
    QLayoutItem,
    QMessageBox,
)

from ._itemeditor import ItemEditorBase
from ._itemsview import ItemsViewInterface
from ..commons import (
    Widget,
    clear_layout,
    insert_widget,
    index_of_widget,
    remove_widget_at,
)

ADD_BUTTON_TEXT = "Add"
EDIT_BUTTON_TEXT = "Edit"
REMOVE_BUTTON_TEXT = "Remove"
CLEAR_BUTTON_TEXT = "Clear"
UP_BUTTON_TEXT = "Up"
DOWN_BUTTON_TEXT = "Down"


@dataclasses.dataclass
class ItemsViewFrameConfig(object):
    add_button_text: str = ADD_BUTTON_TEXT
    edit_button_text: str = EDIT_BUTTON_TEXT
    remove_button_text: str = REMOVE_BUTTON_TEXT
    clear_button_text: str = CLEAR_BUTTON_TEXT
    move_up_button_text: str = UP_BUTTON_TEXT
    move_down_button_text: str = DOWN_BUTTON_TEXT


class ItemsViewFrameBase(QFrame):

    def __init__(self, parent: Optional[QWidget], config: ItemsViewFrameConfig):
        self._config = config

        self._add_button: Optional[QPushButton] = None
        self._edit_button: Optional[QPushButton] = None
        self._remove_button: Optional[QPushButton] = None
        self._clear_button: Optional[QPushButton] = None
        self._move_up_button: Optional[QPushButton] = None
        self._move_down_button: Optional[QPushButton] = None

        super().__init__(parent)

        # layouts
        self._main_layout = QHBoxLayout()
        self._side_widgets_layout = QVBoxLayout()
        self._top_widgets_layout = QVBoxLayout()
        self._bottom_widgets_layout = QVBoxLayout()
        # side panel widget
        self._side_widgets_panel = QWidget(self)

        # create the item view
        self._items_view = self.on_create_items_view()

        # layout all the widgets
        self._setup_layout()

        # setup ui
        self._setup_ui()

    def _setup_layout(self):
        self.setLayout(self._main_layout)
        self._main_layout.addWidget(self._items_view, 9)
        self._setup_side_widgets_layout()
        # self._main_layout.addLayout(self._side_widgets_layout, 1)
        self._main_layout.addWidget(self._side_widgets_panel, 1)

    def _setup_side_widgets_layout(self):
        self._side_widgets_panel.setLayout(self._side_widgets_layout)
        self._side_widgets_layout.setContentsMargins(0, 0, 0, 0)
        # add a spacer
        self._side_widgets_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )
        # add top widgets layout
        self._top_widgets_layout.setContentsMargins(0, 0, 0, 0)
        self._side_widgets_layout.addLayout(self._top_widgets_layout)

        # add a spacer
        self._side_widgets_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )
        # add bottom widgets layout
        self._bottom_widgets_layout.setContentsMargins(0, 0, 0, 0)
        self._side_widgets_layout.addLayout(self._bottom_widgets_layout)

        # add a spacer
        self._side_widgets_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

    def _setup_ui(self):
        if self._config.add_button_text is not None:
            self._add_button = QPushButton(self._side_widgets_panel)
            self._add_button.setText(self._config.add_button_text)
            # noinspection PyUnresolvedReferences
            self._add_button.clicked.connect(self.on_add_button_clicked)
            self.append_top_widget(self._add_button)

        if self._config.edit_button_text is not None:
            self._edit_button = QPushButton(self._side_widgets_panel)
            self._edit_button.setText(self._config.edit_button_text)
            # noinspection PyUnresolvedReferences
            self._edit_button.clicked.connect(self.on_edit_button_clicked)
            self.append_top_widget(self._edit_button)

        if self._config.remove_button_text is not None:
            self._remove_button = QPushButton(self._side_widgets_panel)
            self._remove_button.setText(self._config.remove_button_text)
            # noinspection PyUnresolvedReferences
            self._remove_button.clicked.connect(self.on_remove_button_clicked)
            self.append_top_widget(self._remove_button)

        if self._config.clear_button_text is not None:
            self._clear_button = QPushButton(self._side_widgets_panel)
            self._clear_button.setText(self._config.clear_button_text)
            # noinspection PyUnresolvedReferences
            self._clear_button.clicked.connect(self.on_clear_button_clicked)
            self.append_top_widget(self._clear_button)

        if self._config.move_up_button_text is not None:
            self._move_up_button = QPushButton(self._side_widgets_panel)
            self._move_up_button.setText(self._config.move_up_button_text)
            # noinspection PyUnresolvedReferences
            self._move_up_button.clicked.connect(self.on_move_up_button_clicked)
            self.append_bottom_widget(self._move_up_button)

        if self._config.move_down_button_text is not None:
            self._move_down_button = QPushButton(self._side_widgets_panel)
            self._move_down_button.setText(self._config.move_down_button_text)
            # noinspection PyUnresolvedReferences
            self._move_down_button.clicked.connect(self.on_move_down_button_clicked)
            self.append_bottom_widget(self._move_down_button)

    @abstractmethod
    def on_create_items_view(self) -> QAbstractItemView:
        pass

    @property
    def add_button(self) -> Optional[QPushButton]:
        return self._add_button

    @property
    def edit_button(self) -> Optional[QPushButton]:
        return self._edit_button

    @property
    def remove_button(self) -> Optional[QPushButton]:
        return self._remove_button

    @property
    def clear_button(self) -> Optional[QPushButton]:
        return self._clear_button

    @property
    def move_up_button(self) -> Optional[QPushButton]:
        return self._move_up_button

    @property
    def move_down_button(self) -> Optional[QPushButton]:
        return self._move_down_button

    @property
    def main_layout(self) -> QHBoxLayout:
        return self._main_layout

    @property
    def side_widgets_panel(self) -> QWidget:
        return self._side_widgets_panel

    @property
    def side_widgets_layout(self) -> QVBoxLayout:
        return self._side_widgets_layout

    @property
    def top_widgets_layout(self) -> QVBoxLayout:
        return self._top_widgets_layout

    @property
    def bottom_widgets_layout(self) -> QVBoxLayout:
        return self._bottom_widgets_layout

    def hide_side_widgets(self):
        self._side_widgets_panel.hide()

    def show_side_widgets(self):
        self._side_widgets_panel.show()

    def index_of_top_widget(self, widget: QWidget) -> int:
        return self._find_side_widget(widget, "top")

    def index_of_bottom_widget(self, widget: QWidget) -> int:
        return self._find_side_widget(widget, "bottom")

    def has_top_widget(self, widget: Widget) -> bool:
        return self._find_side_widget(widget, "top") >= 0

    def has_bottom_widget(self, widget: QWidget) -> bool:
        return self._find_side_widget(widget, "bottom") >= 0

    def has_side_widget(self, widget: QWidget) -> bool:
        return self.has_top_widget(widget) or self.has_bottom_widget(widget)

    def top_widget_at(self, index: int) -> QLayoutItem:
        if self._bottom_widgets_layout.count() <= index < 0:
            raise IndexError("index out of range")
        return self._top_widgets_layout.itemAt(index)

    def bottom_widget_at(self, index: int) -> QLayoutItem:
        if self._bottom_widgets_layout.count() <= index < 0:
            raise IndexError("index out of range")
        return self._bottom_widgets_layout.itemAt(index)

    def top_widgets_count(self) -> int:
        return self._top_widgets_layout.count()

    def bottom_widgets_count(self) -> int:
        return self._bottom_widgets_layout.count()

    def side_widgets_count(self) -> int:
        return self._top_widgets_layout.count() + self._bottom_widgets_layout.count()

    def insert_top_widget(self, index: int, widget: Widget, **kwargs):
        self._insert_side_widget(index, widget, "top", **kwargs)

    def insert_top_widget_before(self, widget: Widget, ref_widget: Widget, **kwargs):
        return self._insert_side_widget_before(widget, ref_widget, "top", **kwargs)

    def insert_top_widget_after(self, widget: Widget, ref_widget: Widget, **kwargs):
        return self._insert_side_widget_after(widget, ref_widget, "top", **kwargs)

    def insert_bottom_widget_before(self, widget: Widget, ref_widget: Widget, **kwargs):
        return self._insert_side_widget_before(widget, ref_widget, "bottom", **kwargs)

    def insert_bottom_widget_after(self, widget: Widget, ref_widget: Widget, **kwargs):
        return self._insert_side_widget_after(widget, ref_widget, "bottom", **kwargs)

    def append_top_widget(self, widget: Widget, **kwargs):
        self._insert_side_widget(-1, widget, "top", **kwargs)

    def insert_bottom_widget(self, index: int, widget: Widget, **kwargs):
        self._insert_side_widget(index, widget, "bottom", **kwargs)

    def append_bottom_widget(self, widget: Widget, **kwargs):
        self._insert_side_widget(-1, widget, "bottom", **kwargs)

    def remove_top_widget(self, widget: Widget, delete: bool = True) -> int:
        return self._remove_side_widget(widget, "top", delete)

    def remove_bottom_widget(self, widget: Widget, delete: bool = True) -> int:
        return self._remove_side_widget(widget, "bottom", delete)

    def remove_side_widget(self, widget: Widget, delete: bool = True) -> int:
        return self._remove_side_widget(widget, "side", delete)

    def remove_top_widget_at(self, index: int, delete: bool = True):
        return self._remove_side_widget_at(index, "top", delete)

    def remove_bottom_widget_at(self, index: int, delete: bool = True):
        return self._remove_side_widget_at(index, "bottom", delete)

    def clear_top_widgets(self):
        clear_layout(self._top_widgets_layout)

    def clear_bottom_widgets(self):
        clear_layout(self._top_widgets_layout)

    def clear_side_widgets(self):
        self.clear_top_widgets()
        self.clear_bottom_widgets()

    def on_add_button_clicked(self):
        pass

    def on_remove_button_clicked(self):
        pass

    def on_clear_button_clicked(self):
        pass

    def on_edit_button_clicked(self):
        pass

    def on_move_up_button_clicked(self):
        pass

    def on_move_down_button_clicked(self):
        pass

    def _find_side_widget(
        self, widget: QWidget, which_area: Literal["top", "bottom"]
    ) -> int:
        assert widget is not None
        target = (
            self._top_widgets_layout
            if which_area == "top"
            else self._bottom_widgets_layout
        )
        return index_of_widget(target, widget)

    def _insert_side_widget(
        self, index: int, widget: Widget, which_area: Literal["top", "bottom"], **kwargs
    ):
        assert widget is not None
        target = (
            self._top_widgets_layout
            if which_area == "top"
            else self._bottom_widgets_layout
        )

        if target != -1 and (target.count() <= index < 0):
            raise IndexError("index out of range")
        insert_widget(target, index, widget, **kwargs)

    def _remove_side_widget(
        self, widget: Widget, which_area: Literal["top", "bottom", "side"], delete: bool
    ):
        if which_area == "top":
            index = self._find_side_widget(widget, "top")
            area = "top"
        elif which_area == "bottom":
            index = self._find_side_widget(widget, "bottom")
            area = "bottom"
        else:
            index = self._find_side_widget(widget, "top")
            area = "top"
            if index < 0:
                index = self._find_side_widget(widget, "bottom")
                area = "bottom"
        if index >= 0:
            # noinspection PyTypeChecker
            self._remove_side_widget_at(index, area, delete)
        return index

    def _remove_side_widget_at(
        self, index: int, which_area: Literal["top", "bottom"], delete: bool
    ):
        target = (
            self._top_widgets_layout
            if which_area == "top"
            else self._bottom_widgets_layout
        )
        if target.count() <= index < 0:
            raise IndexError("index out of range")

        remove_widget_at(target, index, delete)

    def _insert_side_widget_before(
        self,
        new_widget: Widget,
        ref_widget: Widget,
        which_area: Literal["top", "bottom"],
        **kwargs,
    ):
        ref_index = self._find_side_widget(ref_widget, which_area)
        if ref_index < 0:
            raise ValueError("widget not found")
        self._insert_side_widget(ref_index, new_widget, which_area, **kwargs)

    def _insert_side_widget_after(
        self,
        new_widget: Widget,
        ref_widget: Widget,
        which_area: Literal["top", "bottom"],
        **kwargs,
    ):
        ref_index = self._find_side_widget(ref_widget, which_area)
        if ref_index < 0:
            raise ValueError("widget not found")
        count = (
            self.top_widgets_count()
            if which_area == "top"
            else self.bottom_widgets_count()
        )

        target_index = ref_index + 1
        target_index = min(target_index, count)
        self._insert_side_widget(target_index, new_widget, which_area, **kwargs)


class CommonItemsViewFrameBase(ItemsViewFrameBase):

    def __init__(self, parent: Optional[QWidget], config: ItemsViewFrameConfig):
        super().__init__(parent, config)

    @property
    @abstractmethod
    def items_view(self) -> ItemsViewInterface:
        pass

    def on_create_items_view(self) -> QAbstractItemView:
        if self._items_view is None:
            raise NotImplementedError()
        if self._items_view.parent() != self:
            self._items_view.setParent(self)
        return self._items_view

    def show_no_selected_items_message(self):
        QMessageBox.warning(self, "Warning", "No selected items!")

    def show_no_items_message(self):
        QMessageBox.warning(self, "Warning", "No items has been added!")

    def show_remove_confirm_message(self, remove_count: int) -> bool:
        _ = remove_count  # unused
        message = "Are you sure to remove the selected items?"
        reply = QMessageBox.question(
            self, "Message", message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            return True
        return False

    def show_clear_confirm_message(self) -> bool:
        message = "Are you sure to remove all items?"
        reply = QMessageBox.question(
            self, "Message", message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            return True
        return False

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def before_add_row(self, row_data: Any) -> bool:
        return True

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def before_update_row(self, row: int, old_data: Any, new_data: Any) -> bool:
        return True

    @abstractmethod
    def create_add_item_editor(self) -> ItemEditorBase:
        pass

    @abstractmethod
    def create_edit_item_editor(self) -> ItemEditorBase:
        pass

    def on_add_button_clicked(self):
        editor = self.create_add_item_editor()
        result, ok = editor.start(None)
        if ok and self.before_add_row(result):
            self.items_view.append_row(result)
        editor.close()
        editor.deleteLater()

    def on_clear_button_clicked(self):
        count = self.items_view.row_count()
        if count <= 0:
            self.show_no_items_message()
            return
        if not self.show_clear_confirm_message():
            return
        self.items_view.remove_all_rows()

    def on_remove_button_clicked(self):
        rows_to_remove = self.items_view.get_selected_rows()
        if not rows_to_remove:
            self.show_no_selected_items_message()
            return
        remove_count = len(rows_to_remove)
        if not self.show_remove_confirm_message(remove_count):
            return
        self.items_view.remove_rows(rows_to_remove)

    def on_edit_button_clicked(self):
        selected_row = self.items_view.get_selected_row()
        if selected_row < 0:
            self.show_no_selected_items_message()
            return
        editor = self.create_edit_item_editor()
        old_data = self.items_view.get_row_data(selected_row)
        new_data, ok = editor.start(old_data)
        if ok and self.before_update_row(selected_row, old_data, new_data):
            self.items_view.set_row_data(selected_row, new_data)
        editor.close()
        editor.deleteLater()

    def on_move_up_button_clicked(self):
        selected_row = self.items_view.get_selected_row()
        if selected_row < 0:
            self.show_no_selected_items_message()
            return
        self.items_view.move_row_up(selected_row)

    def on_move_down_button_clicked(self):
        selected_row = self.items_view.get_selected_row()
        if selected_row < 0:
            self.show_no_selected_items_message()
            return
        self.items_view.move_row_down(selected_row)
