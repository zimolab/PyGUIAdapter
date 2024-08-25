from __future__ import annotations

from qtpy.QtCore import QObject, QSizeF, QRectF
from qtpy.QtGui import (
    QTextObjectInterface,
    QTextDocument,
    QTextFormat,
    QPainter,
    QTextCursor,
    QFontMetrics,
    QTextCharFormat,
)

from .QSyntaxStyle import QSyntaxStyle

ObjectReplacementCharacter = 0xFFFC


# noinspection PyPep8Naming
class QFramedTextAttribute(QObject, QTextObjectInterface):

    FramedString = 1

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self.m_style: QSyntaxStyle | None = None

    # noinspection PyShadowingBuiltins
    def intrinsicSize(
        self, doc: QTextDocument, posInDocument: int, format: QTextFormat
    ) -> QSizeF:
        # noinspection PyArgumentList
        return QSizeF(0.0, 0.0)

    # noinspection PyShadowingBuiltins
    def drawObject(
        self,
        painter: QPainter,
        rect: QRectF,
        doc: QTextDocument,
        posInDocument: int,
        format: QTextFormat,
    ):
        textCharFormat = format.toCharFormat()

        font = textCharFormat.font()
        metrics = QFontMetrics(font)

        string = format.property(self.FramedString).toString()
        stringSize = metrics.boundingRect(string).size()

        # noinspection PyArgumentList
        drawRect = QRectF(rect.topLeft(), stringSize)
        drawRect.moveTop(rect.top() - stringSize.height())
        drawRect.adjust(0, 4, 0, 4)

        painter.setPen(self.m_style.getFormat("Occurrences").background().color())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundRect(drawRect, 4, 4)

    def frame(self, cursor: QTextCursor):
        text = cursor.document().findBlockByNumber(cursor.blockNumber()).text()
        format_ = QTextCharFormat()
        format_.setObjectType(self.type())
        format_.setProperty(self.FramedString, cursor.selectedText())

        if cursor.selectionEnd() > cursor.selectionStart():
            cursor.setPosition(cursor.selectionStart())
        else:
            cursor.setPosition(cursor.selectionEnd())
        cursor.insertText(chr(ObjectReplacementCharacter), format_)

    def clear(self, cursor: QTextCursor):
        doc = cursor.document()

        for blockIndex in range(0, doc.blockCount()):
            block = doc.findBlockByNumber(blockIndex)
            formats = block.textFormats()
            offset = 0

            for f in formats:
                if f.format.objectType() == self.type():
                    cursor.setPosition(block.position() + f.start() - offset)
                    cursor.deleteChar()
                    offset += 1

    def setSyntaxStyle(self, syntaxStyle: QSyntaxStyle):
        self.m_style = syntaxStyle

    def syntaxStyle(self) -> QSyntaxStyle:
        return self.m_style

    @classmethod
    def type(cls) -> int:
        return QTextFormat.UserFormat + 1
