from __future__ import annotations

from typing import List

from qtpy.QtCore import QSize, QRect, Qt, Signal
from qtpy.QtGui import QPainter, QColor, QTextFormat, QTextCursor, QKeyEvent
from qtpy.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QApplication

FONT_SIZE = 14
FONT_FAMILY = "Consolas, Arial, sans-serif"
STYLESHEET = "CodeEditor {font-family: ${font_family};font-size: ${font_size}pt;}"


class LineNumberArea(QWidget):
    def __init__(self, edit: "CodeEdit"):
        super().__init__(edit)
        self._code_edit = edit

    def sizeHint(self):
        return QSize(self._code_edit.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_edit.line_number_area_paint_event(event)


class CodeEdit(QPlainTextEdit):

    indented = Signal(object)
    unindented = Signal(object)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.line_number_area = LineNumberArea(self)

        self._connect()

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        self._indent_char = " "
        self._indent_width = 4

    def keyPressEvent(self, event: QKeyEvent):
        start_line, end_line = self.get_selection_range()
        # indent event
        if event.key() == Qt.Key_Tab and (end_line - start_line) > 0:
            lines = range(start_line, end_line + 1)
            # noinspection PyUnresolvedReferences
            self.indented.emit(lines)
            return

        # un-indent event
        elif event.key() == Qt.Key_Backtab:
            lines = range(start_line, end_line + 1)
            # noinspection PyUnresolvedReferences
            self.unindented.emit(lines)
            return
        elif event.key() == Qt.Key_Tab:
            self.insert_at_cursor(self.indent_char * self.indent_width)
            return
        elif event.key() == Qt.Key_Backspace:
            self.remove_indent_at_cursor()
            return
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    @property
    def indent_char(self) -> str:
        return self._indent_char

    @property
    def indent_width(self) -> int:
        return self._indent_width

    def set_indent(self, indent_char: str, tab_width: int):
        self._indent_char = indent_char
        self._indent_width = tab_width

    def clear_selection(self):
        pos = self.textCursor().selectionEnd()
        self.textCursor().movePosition(pos)

    def get_selection_range(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return 0, 0

        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()

        cursor.setPosition(start_pos)
        start_line = cursor.blockNumber()
        cursor.setPosition(end_pos)
        end_line = cursor.blockNumber()

        return start_line, end_line

    def remove_line_start(self, string: str, line_number: int):
        # noinspection PyArgumentList
        cursor = QTextCursor(self.document().findBlockByLineNumber(line_number))
        cursor.select(QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        if text.startswith(string):
            cursor.removeSelectedText()
            cursor.insertText(text.split(string, 1)[-1])

    def insert_line_start(self, string: str, line_number: int):
        # noinspection PyArgumentList
        cursor = QTextCursor(self.document().findBlockByLineNumber(line_number))
        self.setTextCursor(cursor)
        self.textCursor().insertText(string)

    def insert_at_cursor(self, string: str):
        cursor = self.textCursor()
        cursor.insertText(string)

    def do_indent(self, lines: List[int]):
        for line in lines:
            self.insert_line_start(self.indent_char * self.indent_width, line)

    def undo_indent(self, lines: List[int]):
        for line in lines:
            self.remove_line_start(self.indent_char * self.indent_width, line)

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    # noinspection PyArgumentList
    def line_number_area_paint_event(self, event):
        # noinspection PyArgumentList
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                width = self.line_number_area.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
        painter.end()

    # noinspection PyUnusedLocal
    def update_line_number_area_width(self, new_block_count: int):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            # noinspection PyArgumentList
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def _connect(self):
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        # noinspection PyUnresolvedReferences
        self.indented.connect(self.do_indent)
        # noinspection PyUnresolvedReferences
        self.unindented.connect(self.undo_indent)


if __name__ == "__main__":
    app = QApplication([])
    editor = CodeEdit(None)
    editor.show()
    editor.resize(800, 600)
    app.exec()
