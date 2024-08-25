from __future__ import annotations

from qtpy.QtGui import QTextCursor
from qtpy.QtWidgets import QWidget, QVBoxLayout

from ._logbrowser import LogBrowserConfig, LogBrowser
from ._progressbar import ProgressBarConfig, ProgressBar


class FnExecuteLogOutputArea(QWidget):
    def __init__(
        self,
        parent: QWidget,
        progressbar_config: ProgressBarConfig | None,
        log_browser_config: LogBrowserConfig,
    ):
        self._progressbar: ProgressBar | None = None
        # noinspection SpellCheckingInspection
        self._log_browser: LogBrowser | None = None

        super().__init__(parent)

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout(self)
        self._layout_main.setContentsMargins(1, 2, 1, 2)
        self._setup_log_browser(log_browser_config)
        self._setup_progressbar(progressbar_config)

    def show_progressbar(self):
        self._progressbar.show()

    def hide_progressbar(self):
        self._progressbar.hide()

    def update_progressbar_config(self, config: ProgressBarConfig):
        self._progressbar.update_config(config)

    def update_progress(self, current_value: int, message: str | None = None):
        self._progressbar.update_progress(current_value, message)

    def clear_log_output(self):
        self._log_browser.clear()

    def append_log_output(self, log_text: str, html: bool = False):
        if log_text and not html:
            self._log_browser.insertPlainText(log_text)
            return
        cursor: QTextCursor = self._log_browser.textCursor()
        if log_text:
            cursor.insertHtml(f"<div>{log_text}</div>")
        cursor.insertHtml("<br>")
        self._log_browser.ensureCursorVisible()
        self._log_browser.moveCursor(QTextCursor.MoveOperation.End)

    # noinspection SpellCheckingInspection
    def _setup_log_browser(self, config: LogBrowserConfig | None):
        self._log_browser = LogBrowser(self, config)
        self._layout_main.addWidget(self._log_browser)

    def _setup_progressbar(self, config: ProgressBarConfig | None):
        self._progressbar = ProgressBar(self, config=config)
        self._layout_main.addWidget(self._progressbar)
