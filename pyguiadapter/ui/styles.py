import string

DEFAULT_OUTPUT_FONT_FAMILY = "Arial, sans-serif"
DEFAULT_OUTPUT_FONT_SIZE = 16
DEFAULT_OUTPUT_TEXT_COLOR = "#FFFFFF"
DEFAULT_OUTPUT_BG_COLOR = "#380C2A"

DEFAULT_DOCUMENT_FONT_FAMILY = "Arial, sans-serif"
DEFAULT_DOCUMENT_BG_COLOR = "#FFFFFF"
DEFAULT_DOCUMENT_TEXT_COLOR = "#000000"
DEFAULT_DOCUMENT_FONT_SIZE = 16


TEXTEDIT_STYLESHEET = """
QTextEdit{
    background-color: ${bg_color};
    color: ${text_color};
    font-family: ${font_family};
    font-size: ${font_size}px;
}
QScrollBar::vertical{
    background:transparent;
    width: 6px;
    margin: 0px;
 }
QScrollBar::handle:vertical{
    background-color:rgb(158,158,158);
    border: none;
    border-radius: 3px;
 }
QScrollBar::handle:vertical:pressed{
    background:#EC693C;
}
QScrollBar::sub-line:vertical{
    border:none;
}
QScrollBar::add-line:vertical{
    border:none;
}
QScrollBar::sub-page:vertical{
    border:none;
}
QScrollBar::add-page:vertical{
    border:none;
}
"""


def get_textedit_stylesheet(
    bg_color: str = DEFAULT_OUTPUT_BG_COLOR,
    text_color: str = DEFAULT_OUTPUT_TEXT_COLOR,
    font_family: str = DEFAULT_OUTPUT_FONT_FAMILY,
    font_size: int = DEFAULT_OUTPUT_FONT_SIZE,
):
    css = string.Template(TEXTEDIT_STYLESHEET).substitute(
        bg_color=bg_color,
        text_color=text_color,
        font_family=font_family,
        font_size=font_size,
    )
    return css.strip()
