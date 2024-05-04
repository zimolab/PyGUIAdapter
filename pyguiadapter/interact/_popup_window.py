import abc
import os.path
from typing import Union

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QWidget, QLayout

from .popup_info import *

DEFAULT_COMMON_WIDTH = 500
DEFAULT_COMMON_HEIGHT = 600


class BasePopupWindow(QDialog):
    def __init__(self, popup_info: BasePopupInfo, parent):
        super().__init__(parent)
        self._popup_info = popup_info

        self._button_box = QDialogButtonBox(self)
        self._layout = QVBoxLayout(self)

        self._setup_ui()

    @abc.abstractmethod
    def create_popup_content(
        self, popup_info: BasePopupInfo
    ) -> Union[QWidget, QLayout]:
        pass

    # noinspection PyUnresolvedReferences
    def setup_button_box(self, button_box: QDialogButtonBox):
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def _setup_ui(self):
        if self._popup_info.window_title:
            self.setWindowTitle(self._popup_info.window_title)
        self._set_window_icon(self._popup_info.window_icon)

        self._setup_window_size(
            self._popup_info.window_width, self._popup_info.window_height
        )

        self._setup_button_box(
            self._popup_info.buttons, self._popup_info.buttons_orientation
        )

        content = self.create_popup_content(self._popup_info)
        if isinstance(content, QWidget):
            self._layout.addWidget(content)
        elif isinstance(content, QLayout):
            self._layout.addLayout(content)
        else:
            raise TypeError(f"unsupported content type: {type(content)}")
        self._layout.addWidget(self._button_box)

    def _setup_window_size(self, width: Optional[int], height: Optional[int]):
        if not width or width < 0:
            width = DEFAULT_COMMON_WIDTH
        if not height or height < 0:
            height = DEFAULT_COMMON_HEIGHT
        self.resize(width, height)

    def _set_window_icon(self, icon_path: Union[str]):
        if not icon_path or not os.path.isfile(icon_path):
            return
        icon = QIcon(icon_path)
        if not icon:
            return
        self.setWindowIcon(icon)

    def _setup_button_box(
        self,
        buttons: Optional[QDialogButtonBox.StandardButton],
        orientation: Optional[Qt.Orientation],
    ):
        if orientation:
            self._button_box.setOrientation(orientation)

        if buttons:
            self._button_box.setStandardButtons(buttons)
        self.setup_button_box(self._button_box)


class TextPopupWindow(BasePopupWindow):
    def __init__(self, popup_info: TextPopupInfo, parent):
        super().__init__(popup_info, parent)

        self._text_display_widget: Optional[QTextBrowser] = None

    def create_popup_content(
        self, popup_info: TextPopupInfo
    ) -> Union[QWidget, QLayout]:
        self._text_display_widget = QTextBrowser(self)
        self._text_display_widget.setText(popup_info.text)
        return self._text_display_widget
