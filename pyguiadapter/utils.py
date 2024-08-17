from __future__ import annotations

import os.path
import re
import string
from typing import Literal, List, Set, Tuple, Any, Union

from qtpy.QtWidgets import QTextBrowser, QWidget, QMessageBox, QFrame
from qtpy.QtGui import QIcon, QPixmap, QTextCursor, QTextOption

import qtawesome as qta

TEXTBROWSER_CSS = """
QTextEdit{
    background-color: ${bg_color};
    color: ${text_color};
    font-family: ${font_family};
    font-size: ${font_size}pt;
}
QScrollBar::vertical{
    background:transparent;
    width: 6px;
    margin: 0px;
 }
QScrollBar::handle:vertical{
    background-color:rgb(158,158,158);
    border: none;
    border-radius: 3px;
 }
QScrollBar::handle:vertical:pressed{
    background:#EC693C;
}
QScrollBar::sub-line:vertical{
    border:none;
}
QScrollBar::add-line:vertical{
    border:none;
}
QScrollBar::sub-page:vertical{
    border:none;
}
QScrollBar::add-page:vertical{
    border:none;
}
"""

IconType = Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, type(None)]


def get_icon(src: IconType, *args, **kwargs) -> QIcon | None:
    if src is None:
        return None
    if isinstance(src, QIcon):
        return QIcon(src)
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


def get_textbrowser_stylesheet(
    bg_color: str, text_color: str, font_size: int, font_family: str
):
    css = string.Template(TEXTBROWSER_CSS).substitute(
        bg_color=bg_color,
        text_color=text_color,
        font_size=font_size,
        font_family=font_family,
    )
    return css.strip()


def set_textbrowser_wrap_mode(
    textbrowser: QTextBrowser,
    line_wrap_mode: Literal[
        "no_wrap", "widget_width", "fixed_pixel_width", "fixed_column_width"
    ] = "widget_width",
    word_wrap_mode: Literal[
        "no_wrap",
        "word_wrap",
        "manual_wrap",
        "wrap_anywhere",
        "wrap_at_word_boundary_or_anywhere",
    ] = "word_wrap",
    fixed_line_wrap_width: int = 80,
):
    if line_wrap_mode == "no_wrap":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
    elif line_wrap_mode == "widget_width":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.WidgetWidth)
    elif line_wrap_mode == "fixed_pixel_width":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.FixedPixelWidth)
        textbrowser.setLineWrapColumnOrWidth(fixed_line_wrap_width)
    elif line_wrap_mode == "fixed_column_width":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.FixedColumnWidth)
        textbrowser.setLineWrapColumnOrWidth(fixed_line_wrap_width)
    else:
        raise ValueError(f"invalid line wrap mode: {line_wrap_mode}")

    if word_wrap_mode == "no_wrap":
        textbrowser.setWordWrapMode(QTextOption.NoWrap)
    elif word_wrap_mode == "word_wrap":
        textbrowser.setWordWrapMode(QTextOption.WordWrap)
    elif word_wrap_mode == "manual_wrap":
        textbrowser.setWordWrapMode(QTextOption.ManualWrap)
    elif word_wrap_mode == "wrap_anywhere":
        textbrowser.setWordWrapMode(QTextOption.WrapAnywhere)
    elif word_wrap_mode == "wrap_at_word_boundary_or_anywhere":
        textbrowser.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
    else:
        raise ValueError(f"invalid word wrap mode: {word_wrap_mode}")


def show_warning_message(
    parent: QWidget,
    message: str,
    title: str = "Warning",
) -> int:
    return QMessageBox.warning(parent, title, message)


def hline(parent: QWidget) -> QFrame:
    line = QFrame(parent)
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line


def _marks(marks: str | List[str] | Tuple[str] | Set[str]) -> Set[str]:
    if not isinstance(marks, (list, tuple, set, str)):
        raise TypeError(f"unsupported types for marks: {type(marks)}")
    if isinstance(marks, str):
        if marks.strip() == "":
            raise ValueError("marks must be a non-empty string")
        return {marks}

    if len(marks) <= 0:
        raise ValueError("at least one mark must be provided")

    tmp = set()
    for mark in marks:
        if not isinstance(mark, str):
            raise TypeError(f"a mark must be a string: {type(mark)}")
        if mark.strip() == "":
            raise ValueError("an empty-string mark found")
        tmp.add(mark)
    return tmp


def _block_pattern(
    start_marks: str | List[str] | Tuple[str] | Set[str],
    end_marks: str | List[str] | Tuple[str] | Set[str],
) -> str:
    start_marks = _marks(start_marks)
    end_marks = _marks(end_marks)

    start_mark_choices = "|".join(start_marks)
    end_mark_choices = "|".join(end_marks)
    pattern = (
        rf"^(\s*(?:{start_mark_choices})\s*(.*\n.+)^\s*(?:{end_mark_choices})\s*\n)"
    )
    return pattern


def extract_text_block(
    text: str,
    start_marks: str | List[str] | Tuple[str] | Set[str],
    end_marks: str | List[str] | Tuple[str] | Set[str],
) -> str | None:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if result:
        return result.group(2)
    return None


def remove_text_block(
    text: str,
    start_marks: str | List[str] | Tuple[str] | Set[str],
    end_marks: str | List[str] | Tuple[str] | Set[str],
) -> str:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if not result:
        return text
    return re.sub(
        pattern, repl="", string=text, flags=re.MULTILINE | re.DOTALL | re.UNICODE
    )


def hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False
