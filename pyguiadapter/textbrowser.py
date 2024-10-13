import dataclasses
from typing import Optional, Sequence, Union

from qtpy.QtGui import QTextOption, QColor, QPalette, QTextCursor
from qtpy.QtWidgets import QTextBrowser, QWidget

from .constants.color import COLOR_BASE_BACKGROUND, COLOR_BASE_TEXT
from .constants.font import FONT_LARGE

LineWrapMode = QTextBrowser.LineWrapMode
WordWrapMode = QTextOption.WrapMode


@dataclasses.dataclass
class TextBrowserConfig(object):
    text_color: str = COLOR_BASE_TEXT
    font_family: Union[Sequence[str], str] = None
    font_size: Optional[int] = FONT_LARGE
    background_color: str = COLOR_BASE_BACKGROUND
    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    line_wrap_width: int = 88
    word_wrap_mode: WordWrapMode = WordWrapMode.WordWrap
    open_external_links: bool = True
    stylesheet: str = ""


class TextBrowser(QTextBrowser):
    def __init__(self, parent: Optional[QWidget], config: Optional[TextBrowserConfig]):
        self._config: TextBrowserConfig = config or TextBrowserConfig()
        super().__init__(parent)
        self._apply_config()

    def move_cursor_to_end(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def append_output(self, content: str, html: bool = False, html_tag: str = "div"):
        self.move_cursor_to_end()
        if content and not html:
            self.insertPlainText(content)
            return
        if content:
            self.insertHtml(f"<{html_tag}>" + content + f"</{html_tag}>")
        self.insertHtml("<br />")
        self.ensureCursorVisible()

    def _apply_config(self):
        palette = self.palette()
        if self._config.background_color:
            palette.setColor(QPalette.Base, QColor(self._config.background_color))

        if self._config.text_color:
            palette.setColor(QPalette.Text, QColor(self._config.text_color))
        self.setPalette(palette)

        font = self.font()
        if self._config.font_family:
            if isinstance(self._config.font_family, str):
                font.setFamily(self._config.font_family)
            else:
                font.setFamilies(self._config.font_family)
        if self._config.font_size:
            font.setPixelSize(self._config.font_size)
        self.setFont(font)

        self.setLineWrapMode(self._config.line_wrap_mode)
        if self._config.line_wrap_mode in (
            LineWrapMode.FixedPixelWidth,
            LineWrapMode.WidgetWidth,
        ):
            assert self._config.line_wrap_width > 0
            self.setLineWrapColumnOrWidth(self._config.line_wrap_width)
        self.setWordWrapMode(self._config.word_wrap_mode)

        self.setOpenLinks(self._config.open_external_links)
        self.setOpenExternalLinks(self._config.open_external_links)

        if self._config.stylesheet:
            self.setStyleSheet(self._config.stylesheet)
