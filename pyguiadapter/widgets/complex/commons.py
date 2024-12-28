from typing import Union

from qtpy.QtWidgets import (
    QFrame,
    QWidget,
    QSpacerItem,
    QLayoutItem,
    QLayout,
)


class ValidationFailedError(ValueError):
    pass


class AlreadyExistError(ValueError):
    pass


class NotFoundError(ValueError):
    pass


# Type definitions
# in the context of this module, the concept of `Widget` is used to refer to any item that can be added to a layout, like:
# a QWidget, a QSpacerItem, a QLayout, etc.
Widget = Union[QWidget, QSpacerItem, QLayout, QLayoutItem]


# Utility functions
def clear_layout(layout: QLayout, delete: bool = True):
    for i in reversed(range(layout.count())):

        item: QLayout = layout.takeAt(i)

        spacer = item.spacerItem()
        if spacer is not None:
            del spacer
            del item
            continue

        widget: QWidget = item.widget()
        if widget is not None:
            if delete:
                widget.deleteLater()
            del item
            continue

        layout: QLayout = item.layout()
        if layout is not None:
            clear_layout(layout, delete)
            del item
            continue

        del item


def h_line(parent: QWidget) -> QFrame:
    line = QFrame(parent)
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    return line


def v_line(parent: QWidget) -> QFrame:
    line = QFrame(parent)
    line.setFrameShape(QFrame.VLine)
    line.setFrameShadow(QFrame.Sunken)
    return line


def add_widget(layout: QLayout, widget: Widget, **kwargs):
    pass


def index_of_widget(layout: QLayout, widget: Widget) -> int:
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if isinstance(widget, QSpacerItem) and widget == item.spacerItem():
            return i
        elif isinstance(widget, QLayoutItem) and widget == item:
            return i
        elif isinstance(widget, QWidget) and widget == item.widget():
            return i
        elif isinstance(widget, QLayout) and widget == item.layout():
            return i
        else:
            continue
    return -1


def remove_widget_at(layout: QLayout, index: int, delete: bool = True):
    item = layout.takeAt(index)
    if item is None:
        return

    spacer = item.spacerItem()
    if spacer is not None:
        del spacer
        del item
        return

    widget: QWidget = item.widget()
    if widget is not None:
        if delete:
            widget.deleteLater()
        del item
        return

    layout: QLayout = item.layout()
    if layout is not None:
        clear_layout(layout, delete)
        del item
        return


def insert_widget(layout: QLayout, index: int, widget: Widget, **kwargs):
    if isinstance(widget, QSpacerItem):
        layout.insertSpacerItem(index, widget)
    elif isinstance(widget, QLayoutItem):
        layout.insertItem(index, widget)
    elif isinstance(widget, QWidget):
        layout.insertWidget(index, widget, **kwargs)
    elif isinstance(widget, QLayout):
        layout.insertLayout(index, widget, **kwargs)
    else:
        raise TypeError(f"unsupported widget type: {type(widget)}")
