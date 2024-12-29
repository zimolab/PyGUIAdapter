from typing import Optional, Union, Literal

from qtpy.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGroupBox,
    QAbstractItemView,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)

from .itemsview import CommonItemsViewInterface
from .ui_utilities import (
    insert_widget,
    remove_widget_at,
    clear_layout,
    index_of_widget,
    Widget,
)


class ItemsViewContainer(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget],
        items_view: Union[CommonItemsViewInterface, QAbstractItemView],
        control_widgets_position: Literal["top", "bottom", "left", "right"] = "right",
        items_view_title: str = "",
    ):
        super().__init__(parent)

        self._items_view = items_view
        self._control_widgets_position = control_widgets_position

        self._items_view_box = QGroupBox(self)
        self._items_view_box.setTitle(items_view_title)
        self._setup_items_view_box()

        self._controls_widget_panel = QWidget(self)
        self._setup_controls_widget_panel()

        self._layout: Union[QVBoxLayout, QHBoxLayout, None] = None
        self._setup_layout()

    @property
    def items_view(self) -> Union[CommonItemsViewInterface, QAbstractItemView]:
        return self._items_view

    @property
    def control_widgets_position(self) -> Literal["top", "bottom", "left", "right"]:
        return self._control_widgets_position

    @property
    def control_widgets_panel(self) -> QWidget:
        return self._controls_widget_panel

    def hide_control_widgets_panel(self):
        self._controls_widget_panel.hide()

    def show_control_widgets_panel(self):
        self._controls_widget_panel.show()

    def add_control_widget(self, widget: Widget, **kwargs):
        self.insert_control_widget(-1, widget, **kwargs)

    def insert_control_widget(self, index: int, widget: Widget, **kwargs):
        if isinstance(widget, QWidget):
            widget.setParent(self._controls_widget_panel)
        insert_widget(self._controls_widget_panel.layout(), index, widget, **kwargs)

    def insert_control_widget_after(
        self, widget: Widget, after_widget: Widget, **kwargs
    ):
        after_widget_index = self.index_of_control_widget(after_widget)
        if after_widget_index < 0:
            raise ValueError(f"after_widget not found in control widgets panel")
        insert_pos = after_widget_index + 1
        self.insert_control_widget(
            min(insert_pos, self.control_widget_count()), widget, **kwargs
        )

    def remove_control_widget(self, widget: Widget, delete: bool = True) -> bool:
        index = self.index_of_control_widget(widget)
        if index < 0:
            return False
        remove_widget_at(self._controls_widget_panel.layout(), index, delete)
        return True

    def remove_all_control_widgets(self):
        clear_layout(self._controls_widget_panel.layout())

    def index_of_control_widget(self, widget: Widget) -> int:
        return index_of_widget(self._controls_widget_panel.layout(), widget)

    def control_widget_count(self) -> int:
        return self._controls_widget_panel.layout().count()

    def _setup_layout(self):
        if self._control_widgets_position in ("top", "bottom"):
            self._layout = QVBoxLayout()
        elif self._control_widgets_position in ("left", "right"):
            self._layout = QHBoxLayout()
        else:
            raise ValueError(
                f"invalid control widgets position: {self._control_widgets_position}"
            )
        self.setLayout(self._layout)
        if self._control_widgets_position in ("top", "left"):
            self._layout.addWidget(self._controls_widget_panel)
            self._layout.addWidget(self._items_view_box)
        else:
            self._layout.addWidget(self._items_view_box)
            self._layout.addWidget(self._controls_widget_panel)

    def _setup_items_view_box(self):
        layout = QVBoxLayout()
        self._items_view.setParent(self._items_view_box)
        layout.addWidget(self._items_view)
        self._items_view_box.setLayout(layout)

    def _setup_controls_widget_panel(self):
        if self._control_widgets_position in ("top", "bottom"):
            layout = QHBoxLayout()
            self._controls_widget_panel.setLayout(layout)
        elif self._control_widgets_position in ("left", "right"):
            layout = QVBoxLayout()
            self._controls_widget_panel.setLayout(layout)
        else:
            raise ValueError(
                f"invalid control widgets position: {self._control_widgets_position}"
            )


class ControlButtonHooks(object):
    def on_add_button_clicked(self, source: QPushButton) -> bool:
        pass

    def on_edit_button_clicked(self, source: QPushButton) -> bool:
        pass

    def on_remove_button_clicked(self, source: QPushButton) -> bool:
        pass

    def on_clear_button_clicked(self, source: QPushButton) -> bool:
        pass

    def on_move_up_button_clicked(self, source: QPushButton) -> bool:
        pass

    def on_move_down_button_clicked(self, source: QPushButton) -> bool:
        pass


class CommonItemsViewContainer(ItemsViewContainer):
    # noinspection PyUnresolvedReferences
    def __init__(
        self,
        parent: Optional[QWidget],
        items_view: Union[CommonItemsViewInterface, QAbstractItemView],
        control_widgets_position: Literal["top", "bottom", "left", "right"] = "right",
        items_view_title: str = "",
        add_button_text: str = "Add",
        edit_button_text: str = "Edit",
        remove_button_text: str = "Remove",
        clear_button_text: str = "Clear",
        move_up_button_text: str = "Up",
        move_down_button_text: str = "Down",
        control_button_hooks: Optional[ControlButtonHooks] = None,
    ):
        super().__init__(
            parent,
            items_view,
            control_widgets_position,
            items_view_title,
        )

        self._control_button_hooks = control_button_hooks

        self._control_spacer_1 = self.create_control_spacer()
        self.add_control_widget(self._control_spacer_1)

        self._move_up_button = QPushButton(move_up_button_text)
        self._move_up_button.clicked.connect(self.on_move_up_button_clicked)
        self.add_control_widget(self._move_up_button)

        self._move_down_button = QPushButton(move_down_button_text)
        self._move_down_button.clicked.connect(self.on_move_down_button_clicked)
        self.add_control_widget(self._move_down_button)

        self._control_spacer_2 = self.create_control_spacer()
        self.add_control_widget(self._control_spacer_2)

        self._add_button = QPushButton(add_button_text)
        self._add_button.clicked.connect(self.on_add_button_clicked)
        self.add_control_widget(self._add_button)

        self._edit_button = QPushButton(edit_button_text)
        self._edit_button.clicked.connect(self.on_edit_button_clicked)
        self.add_control_widget(self._edit_button)

        self._remove_button = QPushButton(remove_button_text)
        self._remove_button.clicked.connect(self.on_remove_button_clicked)
        self.add_control_widget(self._remove_button)

        self._clear_button = QPushButton(clear_button_text)
        self._clear_button.clicked.connect(self.on_clear_button_clicked)
        self.add_control_widget(self._clear_button)

        self._control_spacer_3 = self.create_control_spacer()
        self.add_control_widget(self._control_spacer_3)

    @property
    def control_spacer_1(self) -> QSpacerItem:
        return self._control_spacer_1

    @property
    def control_spacer_2(self) -> QSpacerItem:
        return self._control_spacer_2

    @property
    def control_spacer_3(self) -> QSpacerItem:
        return self._control_spacer_3

    @property
    def add_button(self) -> QPushButton:
        return self._add_button

    @property
    def edit_button(self) -> QPushButton:
        return self._edit_button

    @property
    def remove_button(self) -> QPushButton:
        return self._remove_button

    @property
    def clear_button(self) -> QPushButton:
        return self._clear_button

    @property
    def move_up_button(self) -> QPushButton:
        return self._move_up_button

    @property
    def move_down_button(self) -> QPushButton:
        return self._move_down_button

    def on_add_button_clicked(self):
        if self._control_button_hooks is not None:
            ret = self._control_button_hooks.on_add_button_clicked(self._add_button)
            if ret:
                return

    def on_edit_button_clicked(self):
        if self._control_button_hooks is not None:
            ret = self._control_button_hooks.on_edit_button_clicked(self._edit_button)
            if ret:
                return

    def on_remove_button_clicked(self):
        if self._control_button_hooks is not None:
            ret = self._control_button_hooks.on_remove_button_clicked(
                self._remove_button
            )
            if ret:
                return

    def on_clear_button_clicked(self):
        if self._control_button_hooks is not None:
            self._control_button_hooks.on_clear_button_clicked(self._clear_button)

    def on_move_up_button_clicked(self):
        if self._control_button_hooks is not None:
            ret = self._control_button_hooks.on_move_up_button_clicked(
                self._move_up_button
            )
            if ret:
                return

    def on_move_down_button_clicked(self):
        if self._control_button_hooks is not None:
            ret = self._control_button_hooks.on_move_down_button_clicked(
                self._move_down_button
            )
            if ret:
                return

    def create_control_spacer(self) -> QSpacerItem:
        if self.control_widgets_position in ("top", "bottom"):
            return QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        return QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
