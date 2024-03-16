from PyQt6.QtWidgets import QTextBrowser

from pyguiadapter.commons import DocumentFormat
from pyguiadapter.ui.styles import (
    DEFAULT_BG_COLOR,
    DEFAULT_TEXT_COLOR,
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE,
    get_textbrowser_stylesheet,
)


def setup_textbrowser_stylesheet(
    textbrowser: QTextBrowser,
    bg_color: str = DEFAULT_BG_COLOR,
    text_color: str = DEFAULT_TEXT_COLOR,
    font_family: str = DEFAULT_FONT_FAMILY,
    font_size: int = DEFAULT_FONT_SIZE,
):
    textbrowser.setStyleSheet(
        get_textbrowser_stylesheet(
            bg_color=bg_color,
            text_color=text_color,
            font_family=font_family,
            font_size=font_size,
        )
    )


def set_textbrowser_text(
    textbrowser: QTextBrowser, text: str, text_format: DocumentFormat
):
    if text_format == DocumentFormat.HTML:
        textbrowser.setHtml(text)
    elif text_format == DocumentFormat.MARKDOWN:
        textbrowser.setMarkdown(text)
    else:
        textbrowser.setHtml(f"<pre>{text}</pre>")
