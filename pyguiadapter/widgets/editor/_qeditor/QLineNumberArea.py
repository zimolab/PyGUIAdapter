from __future__ import annotations

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QPaintEvent, QPainter
from qtpy.QtWidgets import QWidget

from . import QCodeEditor
from . import QSyntaxStyle


# noinspection PyPep8Naming
class QLineNumberArea(QWidget):

    def __init__(self, parent: QCodeEditor.QCodeEditor | None = None):
        super().__init__(parent)

        self.m_syntaxStyle: QSyntaxStyle.QSyntaxStyle | None = None
        self.m_codeEditParent: QCodeEditor.QCodeEditor | None = parent

    def sizeHint(self) -> QSize:
        if self.m_codeEditParent is None:
            return super().sizeHint()

        digits = 1
        max_ = max(1, self.m_codeEditParent.document().blockCount())
        while max_ >= 10:
            max_ /= 10.0
            digits += 1
        space = 13 + self.m_codeEditParent.fontMetrics().width("0") * digits
        return QSize(space, 0)

    def setSyntaxStyle(self, style: QSyntaxStyle.QSyntaxStyle | None):
        self.m_syntaxStyle = style

    def syntaxStyle(self) -> QSyntaxStyle.QSyntaxStyle | None:
        return self.m_syntaxStyle

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        painter.fillRect(
            event.rect(), self.m_syntaxStyle.getFormat("Text").background().color()
        )
        blockNumber = self.m_codeEditParent.getFirstVisibleBlock()
        block = self.m_codeEditParent.document().findBlockByNumber(blockNumber)
        top = int(
            self.m_codeEditParent.document()
            .documentLayout()
            .blockBoundingRect(block)
            .translated(0, -self.m_codeEditParent.verticalScrollBar().value())
            .top()
        )
        bottom = top + int(
            self.m_codeEditParent.document()
            .documentLayout()
            .blockBoundingRect(block)
            .height()
        )
        currentLine = (
            self.m_syntaxStyle.getFormat("CurrentLineNumber").foreground().color()
        )
        otherLines = self.m_syntaxStyle.getFormat("LineNumber").foreground().color()
        painter.setFont(self.m_codeEditParent.font())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(currentLine if currentLine else otherLines)
                painter.drawText(
                    -5,
                    top,
                    self.sizeHint().width(),
                    self.m_codeEditParent.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )
            block = block.next()
            top = bottom
            bottom = top + int(
                self.m_codeEditParent.document()
                .documentLayout()
                .blockBoundingRect(block)
                .height()
            )
            blockNumber += 1
