from typing import Optional

from qtpy.QtWidgets import QWidget, QVBoxLayout

from .browser import OutputBrowserConfig, OutputBrowser
from .progressbar import ProgressBarConfig, ProgressBar


class OutputArea(QWidget):
    def __init__(
        self, parent: QWidget, output_browser_config: Optional[OutputBrowserConfig]
    ):
        self._progressbar: Optional[ProgressBar] = None
        self._output_browser: Optional[OutputBrowser] = None

        super().__init__(parent)

        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._output_browser = OutputBrowser(
            self, output_browser_config or OutputBrowserConfig()
        )
        self._layout.addWidget(self._output_browser)

        self._progressbar = ProgressBar(self)
        self._layout.addWidget(self._progressbar)
        self.setLayout(self._layout)

    def show_progressbar(self):
        self._progressbar.show()

    def hide_progressbar(self):
        self._progressbar.hide()

    def update_progressbar_config(self, config: ProgressBarConfig):
        self._progressbar.update_config(config)

    def update_progress(self, current_value: int, message: Optional[str] = None):
        self._progressbar.update_progress(current_value, message)

    def clear_output(self):
        self._output_browser.clear()

    def append_output(self, text: str, html: bool = False):
        self._output_browser.append_output(text, html)

    def scroll_to_bottom(self):
        scroll_bar = self._output_browser.verticalScrollBar()
        if scroll_bar:
            scroll_bar.setValue(scroll_bar.maximum())
