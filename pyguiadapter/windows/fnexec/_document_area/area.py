from typing import Literal, Optional, Callable

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

        self._on_parameter_anchor_clicked: Optional[Callable[[str], None]] = None
        self._on_group_anchor_clicked: Optional[Callable[[str], None]] = None

        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._doc_browser = DocumentBrowser(self, document_browser_config)
        self._doc_browser.sig_parameter_anchor_clicked.connect(
            self._on_parameter_anchor_clicked_internal
        )
        self._doc_browser.sig_group_anchor_clicked.connect(
            self._on_group_anchor_clicked_internal
        )
        self._layout.addWidget(self._doc_browser)

        self.setLayout(self._layout)

    def set_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        set_textbrowser_content(self._doc_browser, document, document_format)

    def _on_parameter_anchor_clicked_internal(self, anchor: str):
        if self._on_parameter_anchor_clicked:
            self._on_parameter_anchor_clicked(anchor)

    def _on_group_anchor_clicked_internal(self, anchor: str):
        if self._on_group_anchor_clicked:
            self._on_group_anchor_clicked(anchor)

    def on_parameter_anchor_clicked(self, callback: Callable[[str], None]):
        self._on_parameter_anchor_clicked = callback

    def on_group_anchor_clicked(self, callback: Callable[[str], None]):
        self._on_group_anchor_clicked = callback
