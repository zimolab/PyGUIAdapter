from typing import Optional

from qtpy.QtGui import QTextCursor
from qtpy.QtWidgets import QWidget, QVBoxLayout

from ._outputbrowser import OutputBrowserConfig, OutputBrowser
from ._progressbar import ProgressBarConfig, ProgressBar


class FnExecuteOutputArea(QWidget):
    def __init__(
        self,
        parent: QWidget,
        progressbar_config: Optional[ProgressBarConfig],
        output_browser_config: OutputBrowserConfig,
    ):
        self._progressbar: Optional[ProgressBar] = None
        self._doc_browser: Optional[OutputBrowser] = None

        super().__init__(parent)

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout()
        self.setLayout(self._layout_main)
        self._layout_main.setContentsMargins(1, 2, 1, 2)
        self._setup_doc_browser(output_browser_config)
        self._setup_progressbar(progressbar_config)

    def show_progressbar(self):
        self._progressbar.show()

    def hide_progressbar(self):
        self._progressbar.hide()

    def update_progressbar_config(self, config: ProgressBarConfig):
        self._progressbar.update_config(config)

    def update_progress(self, current_value: int, message: Optional[str] = None):
        self._progressbar.update_progress(current_value, message)

    def clear_output(self):
        self._doc_browser.clear()

    def append_output(self, text: str, html: bool = False):
        if text and not html:
            self._doc_browser.insertPlainText(text)
            return
        cursor: QTextCursor = self._doc_browser.textCursor()
        if text:
            cursor.insertHtml(f"<div>{text}</div>")
        cursor.insertHtml("<br>")
        self._doc_browser.moveCursor(QTextCursor.End)
        self._doc_browser.ensureCursorVisible()

    def scroll_to_bottom(self):
        scroll_bar = self._doc_browser.verticalScrollBar()
        if scroll_bar:
            scroll_bar.setValue(scroll_bar.maximum())

    # noinspection SpellCheckingInspection
    def _setup_doc_browser(self, config: Optional[OutputBrowserConfig]):
        self._doc_browser = OutputBrowser(self, config)
        self._layout_main.addWidget(self._doc_browser)

    def _setup_progressbar(self, config: Optional[ProgressBarConfig]):
        self._progressbar = ProgressBar(self, config=config)
        self._layout_main.addWidget(self._progressbar)
