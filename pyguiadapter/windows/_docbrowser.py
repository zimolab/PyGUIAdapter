from typing import Literal

import dataclasses

from qtpy.QtWidgets import QTextBrowser

from .. import utils

DEFAULT_DOCUMENT_BACKGROUND = "#FFFFFF"
DEFAULT_DOCUMENT_TEXT_COLOR = "#000000"
DEFAULT_DOCUMENT_FONT_SIZE = 14
DEFAULT_DOCUMENT_FONT_FAMILY = "Consolas, Arial, sans-serif"


@dataclasses.dataclass
class DocumentBrowserConfig:
    background: str = DEFAULT_DOCUMENT_BACKGROUND
    text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR
    font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
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
    ] = "word_wrap"
    fixed_line_wrap_width: int = 80
    open_external_links: bool = True

    def apply_to(self, document_browser: QTextBrowser):
        document_browser_stylesheet = utils.get_textbrowser_stylesheet(
            bg_color=self.background,
            text_color=self.text_color,
            font_size=self.font_size,
            font_family=self.font_family,
        )
        document_browser.setStyleSheet(document_browser_stylesheet)
        utils.set_textbrowser_wrap_mode(
            document_browser,
            line_wrap_mode=self.line_wrap_mode,
            word_wrap_mode=self.word_wrap_mode,
            fixed_line_wrap_width=self.fixed_line_wrap_width,
        )
        if self.open_external_links:
            document_browser.setOpenLinks(True)
            document_browser.setOpenExternalLinks(self.open_external_links)
        else:
            document_browser.setOpenExternalLinks(False)
            document_browser.setOpenLinks(False)
