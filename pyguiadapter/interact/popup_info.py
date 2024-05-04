import dataclasses
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialogButtonBox

DEFAULT_TEXT_POPUP_WIDTH = 585
DEFAULT_TEXT_POPUP_HEIGHT = 523


@dataclasses.dataclass
class BasePopupInfo(object):
    window_title: Optional[str] = dataclasses.field(default=None)
    window_icon: Optional[str] = dataclasses.field(default=None)
    window_width: Optional[int] = dataclasses.field(default=None)
    window_height: Optional[int] = dataclasses.field(default=None)
    buttons: QDialogButtonBox.StandardButton = dataclasses.field(
        default=QDialogButtonBox.StandardButton.Ok
    )
    buttons_orientation: Qt.Orientation = dataclasses.field(
        default=Qt.Orientation.Horizontal
    )


@dataclasses.dataclass
class TextPopupInfo(BasePopupInfo):
    text: str = ""
    open_external_link: bool = True
