from __future__ import annotations

from typing import List

from qtpy.QtCore import QRect, QMimeData, QSignalBlocker, Qt
from qtpy.QtGui import (
    QTextCursor,
    QKeyEvent,
    QPaintEvent,
    QFontDatabase,
    QPalette,
    QTextDocument,
    QResizeEvent,
    QBrush,
)
from qtpy.QtWidgets import QCompleter, QTextEdit, QWidget

from .QFramedTextAttribute import QFramedTextAttribute
from .QLineNumberArea import QLineNumberArea
from .QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from .QSyntaxStyle import QSyntaxStyle
from .... import utils

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

        self.m_defaultIndent: int = DEFAULT_TAB_WIDTH

        self.m_tabWidth = self._tabWidth()

        self._initDocumentLayoutHandlers()
        self._initFont()
        self._performConnections()

        self.setSyntaxStyle(QSyntaxStyle.defaultStyle())

        self.updateLineNumberAreaWidth(0)

    def getFirstVisibleBlock(self) -> int:
        doc: QTextDocument = self.document()
        cursor = QTextCursor(doc)
        cursor.movePosition(QTextCursor.Start)

        doc: QTextDocument = self.document()

        for i in range(0, doc.blockCount()):
            block = cursor.block()
            r1: QRect = self.viewport().geometry()
            _layout = doc.documentLayout()
            _bRect = _layout.blockBoundingRect(block)
            _x = self.viewport().geometry().x()
            _y = (
                self.viewport().geometry().y()
                - self.verticalScrollBar().sliderPosition()
            )
            _r = _bRect.translate(_x, _y)
            if _r is None:
                continue
            r2 = _r.toRect()
            if r1.intersects(r2):
                return i
            cursor.movePosition(QTextCursor.NextBlock)
        return 0

    def setHighlighter(self, highlighter: QStyleSyntaxHighlighter):
        if self.m_highlighter is not None:
            self.m_highlighter.setDocument(None)
            self.m_highlighter.setSyntaxStyle(None)
            self.m_highlighter.deleteLater()
            self.m_highlighter = None

        self.m_highlighter = highlighter

        if self.m_highlighter:
            self.m_highlighter.setSyntaxStyle(self.m_syntaxStyle)
            self.m_highlighter.setDocument(self.document())

    def setSyntaxStyle(self, syntaxStyle: QSyntaxStyle | None):
        if self.m_syntaxStyle is not None:
            self.m_syntaxStyle.deleteLater()
            self.m_syntaxStyle = None

        self.m_syntaxStyle = syntaxStyle

        self.m_framedAttribute.setSyntaxStyle(syntaxStyle)
        self.m_lineNumberArea.setSyntaxStyle(syntaxStyle)

        if self.m_highlighter:
            self.m_highlighter.setSyntaxStyle(syntaxStyle)

        self.updateStyle()

    def setAutoParentheses(self, enable: bool):
        self.m_autoParentheses = enable

    def autoParentheses(self) -> bool:
        return self.m_autoParentheses

    def setTabReplace(self, enable: bool):
        self.m_replaceTab = enable

    def tabReplace(self) -> bool:
        return self.m_replaceTab

    def setTabReplaceSize(self, val: int):
        self.m_tabReplace = " " * val

    def tabReplaceSize(self) -> int:
        return len(self.m_tabReplace)

    def setAutoIndentation(self, enable: bool):
        self.m_autoIndentation = enable

    def autoIndentation(self) -> bool:
        return self.m_autoIndentation

    def setCompleter(self, completer: QCompleter | None):
        if self.m_completer:
            # noinspection PyUnresolvedReferences
            self.m_completer.activated.disconnect(self.insertCompletion)
            self.m_completer.deleteLater()
            self.m_completer = None
        self.m_completer = completer
        if not self.m_completer:
            return
        self.m_completer.setWidget(self)
        self.m_completer.setCompletionMode(QCompleter.PopupCompletion)
        # noinspection PyUnresolvedReferences
        self.m_completer.activated.connect(self.insertCompletion)

    def completer(self) -> QCompleter | None:
        return self.m_completer

    def insertCompletion(self, s: str):
        if self.m_completer.widget() != self:
            return
        tc: QTextCursor = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        tc.insertText(s)
        self.setTextCursor(tc)

    # noinspection PyUnusedLocal
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

        # FIXME: Sometimes below code will case a infinite loop(in function _handleSelectionQuery)
        #  and i dont know exactly why and how to fix it.
        # if len(selected) > 1 and cursor.selectedText() == selected:
        #     backup = self.textCursor()
        #     self._handleSelectionQuery(cursor)
        #     self.setTextCursor(backup)

    def insertFromMimeData(self, source: QMimeData, **kwargs):
        self.insertPlainText(source.text())

    def paintEvent(self, e: QPaintEvent, **kwargs):
        self.updateLineNumberArea(e.rect())
        super().paintEvent(e)

    def resizeEvent(self, e: QResizeEvent, **kwargs):
        super().resizeEvent(e)
        self._updateLineGeometry()

    def keyPressEvent(self, e: QKeyEvent, **kwargs):
        defaultIndent = self.m_defaultIndent
        completerSkip = self._proceedCompleterBegin(e)
        key = e.key()
        modifiers = e.modifiers()
        if not completerSkip:
            if (
                self.m_replaceTab
                and key == Qt.Key.Key_Tab
                and modifiers == Qt.NoModifier
            ):
                self.insertPlainText(self.m_tabReplace)
                return

            indentationLevel = self.getIndentationSpaces()
            tabCounts = self._tabCounts(indentationLevel)
            if (
                self.m_autoIndentation
                and (key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter)
                and self._charUnderCursor() == "}"
                and self._charUnderCursor(-1) == "{"
            ):
                charsBack = 0
                self.insertPlainText("\n")
                if self.m_replaceTab:
                    self.insertPlainText(" " * (indentationLevel + defaultIndent))
                else:
                    self.insertPlainText("\t" * (tabCounts + 1))
                self.insertPlainText("\n")
                charsBack += 1

                if self.m_replaceTab:
                    self.insertPlainText(indentationLevel * " ")
                    charsBack += indentationLevel
                else:
                    self.insertPlainText(tabCounts * "\t")
                    charsBack += tabCounts
                while charsBack > 0:
                    self.moveCursor(QTextCursor.MoveOperation.Left)
                    charsBack -= 1
                return
            if self.m_replaceTab and key == Qt.Key.Key_Backtab:
                indentationLevel = min(indentationLevel, len(self.m_tabReplace))
                cursor: QTextCursor = self.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                cursor.movePosition(
                    QTextCursor.MoveOperation.Right,
                    QTextCursor.MoveMode.KeepAnchor,
                    indentationLevel,
                )
                cursor.removeSelectedText()
                return

            super().keyPressEvent(e)

            if self.m_autoIndentation and (
                key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter
            ):
                if self.m_replaceTab:
                    self.insertPlainText(indentationLevel * " ")
                else:
                    self.insertPlainText(tabCounts * "\t")

            if self.m_autoParentheses:
                for el in parentheses:
                    if el[0] == e.text():
                        self.insertPlainText(el[1])
                        self.moveCursor(QTextCursor.MoveOperation.Left)
                        break

                    if el[1] == e.text():
                        symbol_ = self._charUnderCursor()
                        if symbol_ == el[1]:
                            self.textCursor().deletePreviousChar()
                            self.moveCursor(QTextCursor.MoveOperation.Right)
                        break

        self._proceedCompleterEnd(e)

    def focusInEvent(self, e, **kwargs):
        if self.m_completer:
            self.m_completer.setWidget(self)
        super().focusInEvent(e)

    def _initDocumentLayoutHandlers(self):
        self.document().documentLayout().registerHandler(
            QFramedTextAttribute.type(), self.m_framedAttribute
        )

    def _initFont(self):
        # noinspection PyArgumentList
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

        # noinspection PyUnresolvedReferences
        self.cursorPositionChanged.connect(self.updateExtraSelection)
        # noinspection PyUnresolvedReferences
        self.selectionChanged.connect(self.onSelectionChanged)

    def _handleSelectionQuery(self, cursor: QTextCursor):
        searchIterator = cursor
        searchIterator.movePosition(QTextCursor.Start)
        searchIterator = self.document().find(cursor.selectedText(), searchIterator)
        while searchIterator.hasSelection():
            self.m_framedAttribute.frame(searchIterator)
            searchIterator = self.document().find(cursor.selectedText(), searchIterator)

    def _updateLineGeometry(self):
        cr = self.contentsRect()
        self.m_lineNumberArea.setGeometry(
            QRect(
                cr.left(),
                cr.top(),
                self.m_lineNumberArea.sizeHint().width(),
                cr.height(),
            )
        )

    def _proceedCompleterBegin(self, e: QKeyEvent) -> bool:
        if self.m_completer and self.m_completer.popup().isVisible():
            key = e.key()
            if key in (
                Qt.Key.Key_Enter,
                Qt.Key.Key_Return,
                Qt.Key.Key_Escape,
                Qt.Key.Key_Tab,
                Qt.Key.Key_Backtab,
            ):
                e.ignore()
                return True
        modifiers = e.modifiers()
        key = e.key()
        isShortcut = (modifiers | Qt.Modifier.CTRL) and (key == Qt.Key.Key_Space)

        return not (not self.m_completer or not isShortcut)

    def _proceedCompleterEnd(self, e: QKeyEvent):
        key = e.key()
        modifiers = e.modifiers()
        ctrlOrShift = modifiers & (Qt.Modifier.CTRL | Qt.Modifier.SHIFT)

        isEmptyText = e.text().strip() == ""

        if (
            not self.m_completer
            or (ctrlOrShift and isEmptyText)
            or key == Qt.Key.Key_Delete
        ):
            return
        eow = r""""(~!@#$%^&*()_+{}|:"<>?,./;'[]\-=)"""
        isShortcut = modifiers & Qt.Modifier.CTRL and key == Qt.Key.Key_Space
        completionPrefix = self._wordUnderCursor()
        text = e.text()
        isContainChar = text[-1] in eow

        if isShortcut and (isEmptyText or len(completionPrefix) < 2 or isContainChar):
            self.m_completer.popup().hide()
            return

        if completionPrefix != self.m_completer.completionPrefix():
            self.m_completer.setCompletionPrefix(completionPrefix)
            self.m_completer.popup().setCurrentIndex(
                self.m_completer.completionModel().index(0, 0)
            )

        cursRect = self.cursorRect()
        cursRect.setWidth(
            self.m_completer.popup().sizeHintForColumn(0)
            + self.m_completer.popup().verticalScrollBar().sizeHint().width()
        )
        self.m_completer.complete(cursRect)

    def _charUnderCursor(self, offset: int = 0) -> str:
        cursor: QTextCursor = self.textCursor()
        doc: QTextDocument = self.document()
        block = cursor.blockNumber()
        index = cursor.positionInBlock()
        text = doc.findBlockByNumber(block).text()

        index += offset

        if index < 0 or index >= len(text):
            return ""
        return text[index]

    def _wordUnderCursor(self) -> str:
        tc: QTextCursor = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def _highlightCurrentLine(self, extraSelection: List[QTextEdit.ExtraSelection]):
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format = self.m_syntaxStyle.getFormat("CurrentLine")
            selection.format.setForeground(QBrush())
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extraSelection.append(selection)

    def _highlightParenthesis(self, extraSelection: List[QTextEdit.ExtraSelection]):
        currentSymbol = self._charUnderCursor()
        prevSymbol = self._charUnderCursor(-1)

        for pair in parentheses:
            position = self.textCursor().position()

            first = pair[0]
            second = pair[1]

            if first == currentSymbol:
                direction = 1
                counterSymbol = second[0]
                activeSymbol = currentSymbol
            elif second == prevSymbol:
                direction = -1
                counterSymbol = first
                activeSymbol = prevSymbol
                position -= 1
            else:
                continue
            counter = 1

            _charCount = self.document().characterCount() - 1
            while counter != 0 and position > 0 and position < _charCount:
                position += direction
                character = self.document().characterAt(position)
                if character == activeSymbol:
                    counter += 1
                elif character == counterSymbol:
                    counter -= 1
                else:
                    pass
            format_ = self.m_syntaxStyle.getFormat("Parentheses")

            if counter == 0:
                selection = QTextEdit.ExtraSelection()
                directionEnum = (
                    QTextCursor.MoveOperation.Left
                    if direction < 0
                    else QTextCursor.MoveOperation.Right
                )
                selection.format = format_
                selection.cursor = QTextCursor(self.textCursor())
                selection.cursor.clearSelection()
                _foundPos = abs(self.textCursor().position() - position)
                selection.cursor.movePosition(
                    directionEnum, QTextCursor.MoveMode.MoveAnchor, _foundPos
                )
                selection.cursor.movePosition(
                    QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1
                )

                extraSelection.append(selection)

                selection2 = QTextEdit.ExtraSelection()
                selection2.format = format_
                selection2.cursor = QTextCursor(self.textCursor())
                selection2.cursor.clearSelection()
                selection2.cursor.movePosition(
                    directionEnum, QTextCursor.MoveMode.KeepAnchor, 1
                )
                extraSelection.append(selection2)

    def getIndentationSpaces(self) -> int:
        blockText = self.textCursor().block().text()
        indentationLevel: int = 0
        bSize_ = len(blockText)
        for i in range(bSize_):
            if blockText[i] not in "\t ":
                break
            if blockText[i] == " ":
                indentationLevel += 1
            else:
                avgCharWidth = self.fontMetrics().averageCharWidth()
                indentationLevel += int(self.m_tabWidth / avgCharWidth)
        return indentationLevel

    def setDefaultIndent(self, indent: int):
        self.m_defaultIndent = max(0, indent)

    def defaultIndent(self) -> int:
        return self.m_defaultIndent

    def _tabCounts(self, indentationLevel: int) -> int:
        avgCharWidth = self.fontMetrics().averageCharWidth()
        counts = int(indentationLevel * avgCharWidth / self.m_tabWidth)
        return counts

    def _tabWidth(self) -> int:
        if utils.compare_qt_version("5.10.0") >= 0:
            return int(self.tabStopDistance())
        else:
            return int(self.tabStopWidth())
