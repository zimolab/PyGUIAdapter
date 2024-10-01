import os.path
import warnings
from typing import Literal, Tuple, Union, Optional

import qtawesome as qta
from qtpy.QtCore import QSize
from qtpy.QtGui import QColor
from qtpy.QtGui import QIcon, QPixmap, QTextCursor
from qtpy.QtWidgets import QTextBrowser, QWidget, QFrame

IconType = Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, type(None)]


# noinspection PyArgumentList
def get_icon(src: IconType, *args, **kwargs) -> Optional[QIcon]:
    if src is None:
        return None
    if isinstance(src, QIcon):
        return src
    if isinstance(src, QPixmap):
        return QIcon(src)
    if isinstance(src, str):
        if os.path.isfile(src) or src.startswith(":/"):
            return QIcon(src)
        return qta.icon(src, *args, **kwargs)
    if isinstance(src, tuple):
        assert len(src) >= 2
        assert isinstance(src[0], str) and isinstance(src[1], (dict, list))
        if isinstance(src[1], dict):
            return qta.icon(src[0], **src[1])
        else:
            return qta.icon(src[0], *src[1])
    else:
        raise ValueError(f"invalid icon type: {type(src)}")


# noinspection SpellCheckingInspection
def set_textbrowser_content(
    textbrowser: QTextBrowser,
    content: str,
    content_format: Literal["markdown", "html", "plaintext"] = "markdown",
):
    content_format = content_format.lower()
    if content_format == "markdown":
        textbrowser.setMarkdown(content)
    elif content_format == "html":
        textbrowser.setHtml(content)
    elif content_format == "plaintext":
        textbrowser.setPlainText("")
        textbrowser.append(content)
    else:
        raise ValueError(f"invalid content format: {content_format}")

    cursor = textbrowser.textCursor()
    cursor.movePosition(
        QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor
    )
    textbrowser.setTextCursor(cursor)


# noinspection SpellCheckingInspection
def hline(parent: QWidget) -> QFrame:
    line = QFrame(parent)
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line


def get_inverted_color(color: QColor) -> QColor:
    return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())


def get_size(size: Union[int, Tuple[int, int], QSize, None]) -> Optional[QSize]:
    if size is None:
        return None
    if isinstance(size, int):
        return QSize(size, size)
    if isinstance(size, tuple):
        assert len(size) == 2
        return QSize(*size)
    if isinstance(size, QSize):
        return size
    warnings.warn(f"invalid size type: {type(size)}")
    return None


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


# noinspection SpellCheckingInspection
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
        return QColor(color)

    raise ValueError(f"invalid color type: {type(color)}")
