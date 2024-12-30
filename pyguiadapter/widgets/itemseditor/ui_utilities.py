from typing import Union, Literal, Tuple

from qtpy.QtGui import QColor
from qtpy.QtWidgets import (
    QFrame,
    QWidget,
    QSpacerItem,
    QLayoutItem,
    QLayout,
    QBoxLayout,
)


# Type definitions
# in the context of this module, the concept of `Widget` is used to refer to any item that can be added to a layout, like:
# a QWidget, a QSpacerItem, a QLayout, etc.
Widget = Union[QWidget, QSpacerItem, QLayout, QLayoutItem]


# Utility functions
def clear_layout(layout: QLayout, delete: bool = True):
    for i in reversed(range(layout.count())):

        item: QLayoutItem = layout.takeAt(i)

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


def insert_widget(layout: QBoxLayout, index: int, widget: Widget, **kwargs):
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


def is_valid_color(color: Union[str, tuple, list, QColor]) -> bool:
    if isinstance(color, QColor):
        return True
    if isinstance(color, (list, tuple)):
        if len(color) < 3:
            return False
        return all(0 <= c <= 255 for c in color)
    if isinstance(color, str):
        if len(color) < 7:
            return False
        if color[0] != "#" or not all(c in "0123456789ABCDEFabcdef" for c in color[1:]):
            return False
        return True
    return False


def convert_color(
    c: QColor,
    return_type: Literal["tuple", "str", "QColor"],
    alpha_channel: bool = True,
) -> Union[Tuple[int, int, int, int], Tuple[int, int, int], str, QColor]:
    assert isinstance(c, QColor)
    if return_type == "QColor":
        return c

    if return_type == "tuple":
        if alpha_channel:
            return c.red(), c.green(), c.blue(), c.alpha()
        else:
            return c.red(), c.green(), c.blue()
    if return_type == "str":
        if alpha_channel:
            return f"#{c.red():02x}{c.green():02x}{c.blue():02x}{c.alpha():02x}"
        else:
            return f"#{c.red():02x}{c.green():02x}{c.blue():02x}"

    raise ValueError(f"invalid return_type: {return_type}")


def get_inverted_color(color: QColor) -> QColor:
    return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())


def to_qcolor(color: Union[str, tuple, list, QColor]) -> QColor:
    if isinstance(color, QColor):
        return color
    if isinstance(color, (list, tuple)):
        if len(color) < 3:
            raise ValueError(f"invalid color tuple: {color}")
        c = QColor()
        c.setRgb(*color)
        return c
    if isinstance(color, str):
        alpha = None
        if len(color) >= 9:
            try:
                print(color[7:9], int(color[7:9], 16))
                alpha = int(color[7:9], 16)
            except ValueError:
                raise ValueError(
                    f"unable to parse alpha channel from color string: {color}"
                )
            color = color[:7]
        c = QColor(color)
        if alpha is not None:
            c.setAlpha(alpha)
        return c

    raise ValueError(f"invalid color type: {type(color)}")
