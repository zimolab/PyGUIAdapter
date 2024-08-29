from __future__ import annotations

from qtpy.QtWidgets import QDialog, QWidget


class CodeEditor(QDialog):

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

    def get_text(self):
        pass

    def set_text(self):
        pass

    def set_highlighter(self):
        pass

    def set_completer(self):
        pass

    def set_tab(self, size: int = 4, tab_char: str = ""):
        pass
