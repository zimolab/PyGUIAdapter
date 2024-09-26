from typing import Union, Sequence, Optional

import dataclasses

from qtpy.QtWidgets import QWidget

from ..textbrowser import TextBrowserConfig, TextBrowser


DEFAULT_BACKGROUND_COLOR = "#FFFFFF"
DEFAULT_TEXT_COLOR = "#000000"
DEFAULT_FONT_FAMILY = ("Consolas", "Arial", "sans-serif")
DEFAULT_FONT_SIZE = 12


@dataclasses.dataclass
class DocumentBrowserConfig(TextBrowserConfig):
    text_color: str = DEFAULT_TEXT_COLOR
    font_family: Union[Sequence[str], str] = DEFAULT_FONT_FAMILY
    font_size: int = DEFAULT_FONT_SIZE
    background_color: str = DEFAULT_BACKGROUND_COLOR


class DocumentBrowser(TextBrowser):
    def __init__(
        self, parent: Optional[QWidget], config: Optional[DocumentBrowserConfig]
    ):
        config = config or DocumentBrowserConfig()
        super().__init__(parent, config)
