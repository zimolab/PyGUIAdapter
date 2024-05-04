import abc
import os.path
from mako.template import Template
from typing import Union

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextBrowser,
    QWidget,
    QLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)

from .popup_info import *
from ..commons import get_res_file

DEFAULT_COMMON_WIDTH = 500
DEFAULT_COMMON_HEIGHT = 600

APP_ABOUT_INFO_TPL = "app_about_info_tpl.tpl"


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
            self._popup_info.window_width,
            self._popup_info.window_height,
            self._popup_info.resizeable,
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

    def _setup_window_size(
        self, width: Optional[int], height: Optional[int], resizeable: bool
    ):
        if not width or width < 0:
            width = DEFAULT_COMMON_WIDTH
        if not height or height < 0:
            height = DEFAULT_COMMON_HEIGHT
        self.resize(width, height)

        if resizeable is not True:
            self.setFixedSize(self.size())

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
        if buttons is None:
            self._button_box.setHidden(True)
            return

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
        self._text_display_widget.setOpenExternalLinks(
            popup_info.open_external_link is True
        )
        self._text_display_widget.setText(popup_info.text)
        return self._text_display_widget


class AboutPopupWindow(BasePopupWindow):
    def __init__(self, popup_info: AboutPopupInfo, parent):
        super().__init__(popup_info, parent)

        self._content_layout: Optional[QHBoxLayout] = None

    def create_popup_content(
        self, popup_info: AboutPopupInfo
    ) -> Union[QWidget, QLayout]:
        self._content_layout = QHBoxLayout(self)
        self._add_app_logo(popup_info.app_logo)
        self._add_app_info(
            app_name=popup_info.app_name,
            app_copyright=popup_info.app_copyright,
            app_fields=popup_info.app_fields,
            open_external_link=popup_info.open_external_link,
        )
        return self._content_layout

    def _add_app_logo(self, app_logo: Optional[str]):
        if not app_logo or not os.path.isfile(app_logo):
            return

        app_logo_pixmap = QPixmap(app_logo)

        if app_logo_pixmap is None:
            return

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHeightForWidth(True)

        app_logo_label = QLabel(self)
        app_logo_label.setSizePolicy(size_policy)
        app_logo_label.setBaseSize(128, 128)
        app_logo_label.setMaximumWidth(156)
        app_logo_label.setMaximumHeight(156)
        app_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_logo_label.setScaledContents(True)

        app_logo_label.setPixmap(app_logo_pixmap)

        self._content_layout.addWidget(app_logo_label)

    def _add_app_info(
        self,
        app_name: Optional[str],
        app_copyright: Optional[str],
        app_fields: Optional[dict],
        open_external_link: Optional[bool],
    ):
        app_name = app_name or ""
        app_copyright = app_copyright or ""
        app_fields = app_fields or {}

        app_info_label = QLabel(self)
        app_info_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        app_info_label.setTextFormat(Qt.TextFormat.AutoText)
        app_info_label.setOpenExternalLinks(open_external_link is True)

        app_info_text = self._gen_app_info_text(app_name, app_copyright, app_fields)
        app_info_label.setText(app_info_text)

        self._content_layout.addWidget(app_info_label)

    @staticmethod
    def _gen_app_info_text(app_name: str, app_copyright: str, app_fields: dict) -> str:
        tpl_file = get_res_file(APP_ABOUT_INFO_TPL)

        with open(tpl_file, "r", encoding="utf-8") as tpl_file:
            tpl_text = tpl_file.read()
            template = Template(tpl_text)
            return template.render(
                app_name=app_name, app_copyright=app_copyright, app_fields=app_fields
            )
