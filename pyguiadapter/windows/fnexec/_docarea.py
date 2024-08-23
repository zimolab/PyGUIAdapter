from typing import Literal

from qtpy.QtWidgets import QWidget, QVBoxLayout, QTextBrowser

from .._docbrowser import DocumentBrowserConfig
from ... import utils


class FnDocumentArea(QWidget):
    # noinspection SpellCheckingInspection
    def __init__(self, parent: QWidget, document_browser_config: DocumentBrowserConfig):
        super().__init__(parent)

        self._config = document_browser_config

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout(self)
        self._layout_main.setContentsMargins(0, 0, 0, 0)
        self._document_textbrowser = QTextBrowser(self)
        self._config.apply_to(self._document_textbrowser)

        self._layout_main.addWidget(self._document_textbrowser)

    def update_document(
        self,
        document: str,
        document_format: Literal["markdown", "html", "plaintext"],
    ):
        utils.set_textbrowser_content(
            self._document_textbrowser, document, document_format
        )
