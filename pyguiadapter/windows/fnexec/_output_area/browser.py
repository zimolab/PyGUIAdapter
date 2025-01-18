import dataclasses
from typing import Optional, Union, Sequence

from qtpy.QtWidgets import QWidget

from ....constants.color import (
    COLOR_TERMINAL_BACKGROUND_CLASSIC,
    COLOR_TERMINAL_TEXT_CLASSIC,
)
from ....constants.font import FONT_FAMILY
from ....textbrowser import TextBrowserConfig, TextBrowser


@dataclasses.dataclass
class OutputBrowserConfig(TextBrowserConfig):
    """输出浏览器配置类。"""

    text_color: str = COLOR_TERMINAL_TEXT_CLASSIC
    font_family: Union[Sequence[str], str, None] = FONT_FAMILY
    background_color: str = COLOR_TERMINAL_BACKGROUND_CLASSIC


class OutputBrowser(TextBrowser):
    def __init__(
        self, parent: Optional[QWidget], config: Optional[OutputBrowserConfig]
    ):
        config = config or OutputBrowserConfig()
        super().__init__(parent, config)
