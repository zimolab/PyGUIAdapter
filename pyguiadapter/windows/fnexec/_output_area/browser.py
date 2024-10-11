import dataclasses
from typing import Optional

from qtpy.QtWidgets import QWidget

from ....constants.color import (
    COLOR_TERMINAL_BACKGROUND_CLASSIC,
    COLOR_TERMINAL_TEXT_CLASSIC,
)
from ....textbrowser import TextBrowserConfig, TextBrowser


@dataclasses.dataclass
class OutputBrowserConfig(TextBrowserConfig):
    text_color: str = COLOR_TERMINAL_TEXT_CLASSIC
    background_color: str = COLOR_TERMINAL_BACKGROUND_CLASSIC


class OutputBrowser(TextBrowser):
    def __init__(
        self, parent: Optional[QWidget], config: Optional[OutputBrowserConfig]
    ):
        config = config or OutputBrowserConfig()
        super().__init__(parent, config)
