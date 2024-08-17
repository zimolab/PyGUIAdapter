from typing import Literal

from qtpy.QtWidgets import QWidget, QVBoxLayout, QTextBrowser

from .._docbrowser import DocumentBrowserConfig
from ... import utils


class FnDocumentArea(QWidget):
    def __init__(self, parent: QWidget, document_browser_config: DocumentBrowserConfig):
        super().__init__(parent)

        self._document_browser_config = document_browser_config

        self._vlayout_main = QVBoxLayout(self)
        self._vlayout_main.setContentsMargins(0, 0, 0, 0)
        self._textbrowser_fn_document = QTextBrowser(self)
        self._document_browser_config.apply_to(self._textbrowser_fn_document)
        self._vlayout_main.addWidget(self._textbrowser_fn_document)

    def set_fn_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        utils.set_textbrowser_content(
            self._textbrowser_fn_document, document, document_format
        )
