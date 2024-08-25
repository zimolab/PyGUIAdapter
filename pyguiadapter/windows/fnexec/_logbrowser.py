from __future__ import annotations

import dataclasses
from typing import Literal

from qtpy.QtWidgets import QTextBrowser, QWidget

from ... import utils

DEFAULT_LOG_OUTPUT_BACKGROUND = "#380C2A"
DEFAULT_LOG_OUTPUT_TEXT_COLOR = "#FFFFFF"
DEFAULT_LOG_OUTPUT_FONT_SIZE = 14
DEFAULT_LOG_OUTPUT_FONT_FAMILY = "Consolas, Arial, sans-serif"


@dataclasses.dataclass
class LogBrowserConfig(object):
    background: str = DEFAULT_LOG_OUTPUT_BACKGROUND
    text_color: str = DEFAULT_LOG_OUTPUT_TEXT_COLOR
    font_size: int = DEFAULT_LOG_OUTPUT_FONT_SIZE
    font_family: str = DEFAULT_LOG_OUTPUT_FONT_FAMILY
    line_wrap_mode: Literal[
        "no_wrap",
        "widget_width",
        "fixed_pixel_width",
        "fixed_column_width",
    ] = "widget_width"
    word_wrap_mode: Literal[
        "no_wrap",
        "word_wrap",
        "manual_wrap",
        "wrap_anywhere",
        "wrap_at_word_boundary_or_anywhere",
    ] = "no_wrap"
    fixed_line_wrap_width: int = 80


class LogBrowser(QTextBrowser):
    def __init__(self, parent: QWidget | None, config: LogBrowserConfig | None):
        super().__init__(parent)
        self._config = config or LogBrowserConfig()

        self._setup()

    def _setup(self):
        utils.set_textbrowser_wrap_mode(
            self,
            word_wrap_mode=self._config.word_wrap_mode,
            line_wrap_mode=self._config.line_wrap_mode,
            fixed_line_wrap_width=self._config.fixed_line_wrap_width,
        )
        stylesheet = utils.get_textbrowser_stylesheet(
            bg_color=self._config.background,
            text_color=self._config.text_color,
            font_size=self._config.font_size,
            font_family=self._config.font_family,
        )
        self.setStyleSheet(stylesheet)

    def contextMenuEvent(self, e):
        """TODO custom context menu actions"""
        super().contextMenuEvent(e)
