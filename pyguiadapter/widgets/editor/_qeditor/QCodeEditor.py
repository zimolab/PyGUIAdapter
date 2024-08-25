from __future__ import annotations

from typing import List

from qtpy.QtCore import QRect, QMimeData, QSignalBlocker, QRectF
from qtpy.QtGui import (
    QTextCursor,
    QKeyEvent,
    QTextBlock,
    QPaintEvent,
    QFontDatabase,
    QAbstractTextDocumentLayout,
    QTextCharFormat,
    QShortcut,
    QPalette,
)
from qtpy.QtWidgets import QCompleter, QTextEdit, QWidget, QScrollBar, QAbstractItemView
from .QLineNumberArea import QLineNumberArea
from .QSyntaxStyle import QSyntaxStyle
from .QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from .QFramedTextAttribute import QFramedTextAttribute

DEFAULT_TAB_WIDTH = 4

parentheses = [
    ("(", ")"),
    ("{", "}"),
    ("[", "]"),
    ('"', '"'),
    ("'", "'"),
]


# noinspection PyPep8Naming
class QCodeEditor(QTextEdit):

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.m_highlighter: QStyleSyntaxHighlighter | None = None
        self.m_syntaxStyle: QSyntaxStyle | None = None
        self.m_lineNumberArea: QLineNumberArea = QLineNumberArea(self)
        self.m_completer: QCompleter | None = None
        self.m_framedAttribute: QFramedTextAttribute = QFramedTextAttribute(self)
        self.m_autoIndentation: bool = True
        self.m_autoParentheses: bool = True
        self.m_replaceTab: bool = True
        self.m_tabReplace: str = " " * DEFAULT_TAB_WIDTH

        self._initDocumentLayoutHandlers()
        self._initFont()
        self._performConnections()

        self.setSyntaxStyle(QSyntaxStyle.defaultStyle())

    def getFirstVisibleBlock(self) -> int:
        pass

    def setHighlighter(self, highlighter: QStyleSyntaxHighlighter):
        if self.m_highlighter is not None:
            self.m_highlighter.setDocument(None)
        self.m_highlighter = highlighter
        if self.m_highlighter:
            self.m_highlighter.setSyntaxStyle(self.m_syntaxStyle)
            self.m_highlighter.setDocument(self.document())

    def setSyntaxStyle(self, syntaxStyle: QSyntaxStyle):
        self.m_syntaxStyle = syntaxStyle

        self.m_framedAttribute.setSyntaxStyle(syntaxStyle)
        self.m_lineNumberArea.setSyntaxStyle(syntaxStyle)

        if self.m_highlighter:
            self.m_highlighter.setSyntaxStyle(syntaxStyle)

        self.updateStyle()

    def setAutoParentheses(self, enable: bool):
        pass

    def autoParentheses(self) -> bool:
        pass

    def setTabReplace(self, enable: bool):
        pass

    def tabReplace(self) -> bool:
        pass

    def setTabReplaceSize(self, val: int):
        pass

    def tabReplaceSize(self) -> int:
        pass

    def setAutoIndentation(self, enable: bool):
        pass

    def autoIndentation(self) -> bool:
        pass

    def setCompleter(self, completer: QCompleter):
        pass

    def completer(self) -> QCompleter:
        pass

    def insertCompletion(self, s: str):
        pass

    def updateLineNumberAreaWidth(self, w: int):
        self.setViewportMargins(self.m_lineNumberArea.sizeHint().width(), 0, 0, 0)

    def updateLineNumberArea(self, rect: QRect):
        self.m_lineNumberArea.update(
            0, rect.y(), self.m_lineNumberArea.sizeHint().width(), rect.height()
        )

    def updateExtraSelection(self):
        extra = []
        self._highlightCurrentLine(extra)
        self._highlightParenthesis(extra)
        self.setExtraSelections(extra)

    def updateStyle(self):
        if self.m_highlighter:
            self.m_highlighter.rehighlight()

        if self.m_syntaxStyle:
            currentPalette = self.palette()
            currentPalette.setColor(
                QPalette.ColorRole.Text,
                self.m_syntaxStyle.getFormat("Text").foreground().color(),
            )

            currentPalette.setColor(
                QPalette.Base,
                self.m_syntaxStyle.getFormat("Text").background().color(),
            )

            currentPalette.setColor(
                QPalette.Highlight,
                self.m_syntaxStyle.getFormat("Selection").background().color(),
            )

            self.setPalette(currentPalette)

        self.updateExtraSelection()

    def onSelectionChanged(self):
        selected = self.textCursor().selectedText()
        cursor = self.textCursor()

        if cursor.isNull():
            return
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)

        blocker = QSignalBlocker(self)
        self.m_framedAttribute.clear(cursor)

        if len(selected) > 1 and cursor.selectedText() == selected:
            backup = self.textCursor()
            self._handleSelectionQuery(cursor)
            self.setTextCursor(backup)

    def insertFromMimeData(self, source: QMimeData):
        pass

    def paintEvent(self, e):
        pass

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._updateLineGeometry()

    def keyPressEvent(self, e):
        pass

    def focusInEvent(self, e):
        pass

    def _initDocumentLayoutHandlers(self):
        document = self.document()
        if not document:
            return
        document.documentLayout().registerHandler(
            QFramedTextAttribute.type(), self.m_framedAttribute
        )

    def _initFont(self):
        fnt = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fnt.setFixedPitch(True)
        fnt.setPointSize(20)
        self.setFont(fnt)

    def _performConnections(self):
        doc = self.document()
        doc.blockCountChanged.connect(self.updateLineNumberAreaWidth)

        def _vbar_changed(_):
            self.m_lineNumberArea.update()

        vbar = self.verticalScrollBar()
        vbar.valueChanged.connect(_vbar_changed)

        self.cursorPositionChanged.connect(self.updateExtraSelection)
        self.selectionChanged.connect(self.onSelectionChanged)

    def _handleSelectionQuery(self, cursor: QTextCursor):
        searchIterator = QTextCursor(cursor)
        searchIterator.movePosition(QTextCursor.Start)
        searchIterator = self.document().find(cursor.selectedText(), searchIterator)
        while searchIterator.hasSelection():
            self.m_framedAttribute.frame(searchIterator)
            searchIterator = self.document().find(cursor.selectedText(), searchIterator)

    def _updateLineGeometry(self):
        cr = self.contentsRect()
        self.m_lineNumberArea.setGeometry(
            QRectF(
                cr.left(),
                cr.top(),
                self.m_lineNumberArea.sizeHint().width(),
                cr.height(),
            )
        )

    def _proceedCompleterBegin(self, e: QKeyEvent) -> bool:
        pass

    def _proceedCompleterEnd(self, e: QKeyEvent):
        pass

    def _charUnderCursor(self, offset: int = 0) -> str:
        pass

    def _wordUnderCursor(self) -> str:
        pass

    def _highlightCurrentLine(self, extraSelection: List[QTextEdit.ExtraSelection]):
        pass

    def _highlightParenthesis(self, extraSelection: List[QTextEdit.ExtraSelection]):
        pass

    def getIndentationSpaces(self) -> int:
        pass
