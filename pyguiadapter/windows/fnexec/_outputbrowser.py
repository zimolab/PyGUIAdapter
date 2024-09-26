import dataclasses
from typing import Literal, Optional

from qtpy.QtGui import QTextCursor
from qtpy.QtWidgets import QTextBrowser, QWidget

from ... import utils

DEFAULT_OUTPUT_BACKGROUND = "#380C2A"
DEFAULT_OUTPUT_TEXT_COLOR = "#FFFFFF"
DEFAULT_OUTPUT_FONT_SIZE = 12
DEFAULT_OUTPUT_FONT_FAMILY = "Consolas, Arial, sans-serif"


@dataclasses.dataclass
class OutputBrowserConfig(object):
    background: str = DEFAULT_OUTPUT_BACKGROUND
    text_color: str = DEFAULT_OUTPUT_TEXT_COLOR
    font_size: int = DEFAULT_OUTPUT_FONT_SIZE
    font_family: str = DEFAULT_OUTPUT_FONT_FAMILY
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


class OutputBrowser(QTextBrowser):
    def __init__(
        self, parent: Optional[QWidget], config: Optional[OutputBrowserConfig]
    ):
        super().__init__(parent)
        self._config = config or OutputBrowserConfig()
        self._setup_ui()

    def _setup_ui(self):
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

    def move_cursor_to_end(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def append_output(self, text: str, html: bool = False):
        self.move_cursor_to_end()
        if text and not html:
            self.insertPlainText(text)
            return
        if text:
            self.insertHtml("<div>" + text + "</div>")
        self.insertHtml("<br>")
        # self.move_cursor_to_end()
        self.ensureCursorVisible()

    def contextMenuEvent(self, e):
        """TODO custom context menu actions"""
        super().contextMenuEvent(e)
