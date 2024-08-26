from __future__ import annotations

from qtpy.QtGui import QSyntaxHighlighter, QTextDocument

from . import QSyntaxStyle


# noinspection PyPep8Naming
class QStyleSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument | None = None):
        super().__init__(document)

        self.m_syntaxStyle: QSyntaxStyle.QSyntaxStyle | None = None

    def setSyntaxStyle(self, style: QSyntaxStyle.QSyntaxStyle | None):
        self.m_syntaxStyle = style

    def syntaxStyle(self) -> QSyntaxStyle.QSyntaxStyle | None:
        return self.m_syntaxStyle
