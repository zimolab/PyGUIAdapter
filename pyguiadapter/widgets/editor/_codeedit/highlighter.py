from __future__ import annotations

from typing import List

from qtpy.QtCore import QObject
from qtpy.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format_char(color: str, style: str = ""):
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if "bold" in style:
        _format.setFontWeight(QFont.Bold)
    if "italic" in style:
        _format.setFontItalic(True)

    return _format


class Highlighter(QSyntaxHighlighter):

    KEYWORDS: List[str] = NotImplemented
    OPERATORS: List[str] = NotImplemented
    BRACES: List[str] = NotImplemented

    def __init__(self, parent: QObject | None):
        super().__init__(parent)

    def highlightBlock(self, text: str):
        super().highlightBlock(text)
