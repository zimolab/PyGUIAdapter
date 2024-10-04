from typing import Literal, Optional

from qtpy.QtWidgets import QWidget, QVBoxLayout

from ...document_browser import DocumentBrowserConfig, DocumentBrowser
from ....utils import set_textbrowser_content


class DocumentArea(QWidget):
    # noinspection SpellCheckingInspection
    def __init__(
        self, parent: QWidget, document_browser_config: Optional[DocumentBrowserConfig]
    ):
        super().__init__(parent)

        self._config = document_browser_config or DocumentBrowserConfig()

        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._document_textbrowser = DocumentBrowser(self, document_browser_config)
        self._layout.addWidget(self._document_textbrowser)

        self.setLayout(self._layout)

    def set_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        set_textbrowser_content(self._document_textbrowser, document, document_format)
