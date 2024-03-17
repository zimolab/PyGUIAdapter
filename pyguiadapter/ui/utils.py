from PyQt6.QtWidgets import QTextEdit

from pyguiadapter.commons import DocumentFormat
from pyguiadapter.ui.styles import (
    DEFAULT_BG_COLOR,
    DEFAULT_TEXT_COLOR,
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE,
    get_text_edit_stylesheet,
)


def setup_text_edit_stylesheet(
    text_edit: QTextEdit,
    bg_color: str = DEFAULT_BG_COLOR,
    text_color: str = DEFAULT_TEXT_COLOR,
    font_family: str = DEFAULT_FONT_FAMILY,
    font_size: int = DEFAULT_FONT_SIZE,
):
    text_edit.setStyleSheet(
        get_text_edit_stylesheet(
            bg_color=bg_color,
            text_color=text_color,
            font_family=font_family,
            font_size=font_size,
        )
    )


def set_text_edit_text(text_edit: QTextEdit, text: str, text_format: DocumentFormat):
    if text_format == DocumentFormat.HTML:
        text_edit.setHtml(text)
    elif text_format == DocumentFormat.MARKDOWN:
        text_edit.setMarkdown(text)
    else:
        text_edit.setPlainText("")
        text_edit.append(text)
