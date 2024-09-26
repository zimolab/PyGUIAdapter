import dataclasses
from typing import Optional, Union, Sequence

from qtpy.QtWidgets import QWidget

DEFAULT_BACKGROUND_COLOR = "#380C2A"
DEFAULT_TEXT_COLOR = "#FFFFFF"
DEFAULT_FONT_FAMILY = ("Consolas", "Arial", "sans-serif")
DEFAULT_FONT_SIZE = 12

from ...textbrowser import TextBrowserConfig, TextBrowser


@dataclasses.dataclass
class OutputBrowserConfig(TextBrowserConfig):
    text_color: str = DEFAULT_TEXT_COLOR
    font_family: Union[Sequence[str], str] = DEFAULT_FONT_FAMILY
    font_size: int = DEFAULT_FONT_SIZE
    background_color: str = DEFAULT_BACKGROUND_COLOR


class OutputBrowser(TextBrowser):
    def __init__(
        self, parent: Optional[QWidget], config: Optional[OutputBrowserConfig]
    ):
        config = config or OutputBrowserConfig()
        super().__init__(parent, config)
