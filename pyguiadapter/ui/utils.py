from PyQt6.QtWidgets import QTextEdit

from pyguiadapter.commons import DocumentFormat
from pyguiadapter.ui.styles import (
    DEFAULT_OUTPUT_BG_COLOR,
    DEFAULT_OUTPUT_TEXT_COLOR,
    DEFAULT_OUTPUT_FONT_FAMILY,
    DEFAULT_OUTPUT_FONT_SIZE,
    get_textedit_stylesheet,
)


def setup_textedit_stylesheet(
    textedit: QTextEdit,
    bg_color: str = DEFAULT_OUTPUT_BG_COLOR,
    text_color: str = DEFAULT_OUTPUT_TEXT_COLOR,
    font_family: str = DEFAULT_OUTPUT_FONT_FAMILY,
    font_size: int = DEFAULT_OUTPUT_FONT_SIZE,
):
    textedit.setStyleSheet(
        get_textedit_stylesheet(
            bg_color=bg_color,
            text_color=text_color,
            font_family=font_family,
            font_size=font_size,
        )
    )


def set_textedit_text(textedit: QTextEdit, text: str, text_format: DocumentFormat):
    if text_format == DocumentFormat.HTML:
        textedit.setHtml(text)
    elif text_format == DocumentFormat.MARKDOWN:
        textedit.setMarkdown(text)
    else:
        textedit.setPlainText("")
        textedit.append(text)
