import dataclasses
from collections import OrderedDict


from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialogButtonBox

DEFAULT_TEXT_POPUP_WIDTH = 585
DEFAULT_TEXT_POPUP_HEIGHT = 523

DEFAULT_ABOUT_POPUP_WIDTH = 460
DEFAULT_ABOUT_POPUP_HEIGHT = 240


@dataclasses.dataclass
class BasePopupInfo(object):
    window_title: Optional[str] = None
    window_icon: Optional[str] = None
    window_width: Optional[int] = None
    window_height: Optional[int] = None
    buttons: Optional[QDialogButtonBox.StandardButton] = (
        QDialogButtonBox.StandardButton.Ok
    )
    buttons_orientation: Optional[Qt.Orientation] = None
    resizeable: bool = False


@dataclasses.dataclass
class TextPopupInfo(BasePopupInfo):
    text: str = ""
    open_external_link: bool = True
    window_width: Optional[int] = DEFAULT_TEXT_POPUP_WIDTH
    window_height: Optional[int] = DEFAULT_TEXT_POPUP_HEIGHT
    resizeable: bool = True


@dataclasses.dataclass
class AboutPopupInfo(BasePopupInfo):
    app_name: Optional[str] = None
    app_copyright: Optional[str] = None
    app_logo: Optional[str] = None
    app_fields: Optional[dict] = dataclasses.field(default_factory=OrderedDict)
    open_external_link: bool = True
    window_width: Optional[int] = DEFAULT_ABOUT_POPUP_WIDTH
    window_height: Optional[int] = DEFAULT_ABOUT_POPUP_HEIGHT
    window_title: Optional[str] = "About"
    buttons: Optional[QDialogButtonBox.StandardButton] = dataclasses.field(
        default=QDialogButtonBox.StandardButton.Close
    )
