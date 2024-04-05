import dataclasses
from typing import Optional

from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.styles import (
    DEFAULT_DOCUMENT_FONT_FAMILY,
    DEFAULT_DOCUMENT_FONT_SIZE,
    DEFAULT_DOCUMENT_BG_COLOR,
    DEFAULT_DOCUMENT_TEXT_COLOR,
)

DEFAULT_ICON_SIZE = 48


@dataclasses.dataclass
class SelectionWindowConfig(WindowConfig):
    icon_mode: bool = True
    icon_size: Optional[int] = DEFAULT_ICON_SIZE
    func_list_label_text: Optional[str] = None
    document_label_text: Optional[str] = None
    select_button_text: Optional[str] = None

    document_font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
    document_font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    document_bg_color: str = DEFAULT_DOCUMENT_BG_COLOR
    document_text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR
