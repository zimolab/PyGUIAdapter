import dataclasses
from typing import Optional

from qtpy.QtWidgets import QWidget

from ..constants.color import COLOR_PAGE_BACKGROUND, COLOR_PRIMARY_TEXT
from ..textbrowser import TextBrowserConfig, TextBrowser, LineWrapMode


@dataclasses.dataclass
class DocumentBrowserConfig(TextBrowserConfig):
    """文档浏览器配置类。"""

    text_color: str = COLOR_PRIMARY_TEXT
    background_color: str = COLOR_PAGE_BACKGROUND
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth


class DocumentBrowser(TextBrowser):
    def __init__(
        self, parent: Optional[QWidget], config: Optional[DocumentBrowserConfig]
    ):
        config = config or DocumentBrowserConfig()
        super().__init__(parent, config)
