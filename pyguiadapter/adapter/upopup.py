from __future__ import annotations

from typing import Sequence, Any, Tuple, Literal

from qtpy.QtGui import QPixmap, QIcon
from qtpy.QtWidgets import (
    QMessageBox,
    QWidget,
    QDialogButtonBox,
    QVBoxLayout,
    QTextBrowser,
)

from .custom_dialog import BaseCustomDialog
from .ucontext import show_dialog, DialogConfig, show_custom_dialog
from .. import utils


class TextBrowserDialog(BaseCustomDialog):

    DEFAULT_SIZE = (585, 523)

    def __init__(
        self,
        parent: QWidget | None,
        text_content: str,
        text_format: Literal["markdown", "plaintext", "html"] = "markdown",
        size: Tuple[int, int] | None = None,
        title: str | None = None,
        icon: utils.IconType = None,
        buttons: int | QDialogButtonBox.StandardButtons | None = QDialogButtonBox.Ok,
        resizeable: bool = True,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self._text_content = text_content
        self._text_format = text_format
        self._size = size or self.DEFAULT_SIZE
        self._title = title
        self._icon = icon
        self._buttons = buttons
        self._resizeable = resizeable

        self._button_box = QDialogButtonBox(self)
        self._textbrowser = QTextBrowser(self)
        self._layout = QVBoxLayout(self)

        self._setup_ui()

    def get_result(self) -> Any:
        return None

    # noinspection PyUnresolvedReferences
    def _setup_ui(self):
        if self._title is not None:
            self.setWindowTitle(self._title)

        if not self._icon:
            icon = utils.get_icon(self._icon) or QIcon()
            self.setWindowIcon(icon)

        if self._size:
            self.resize(*self._size)
            if not self._resizeable:
                self.setFixedSize(*self._size)

        if self._buttons is not None:
            self._button_box.setStandardButtons(self._buttons)
            self._button_box.accepted.connect(self.accept)
            self._button_box.rejected.connect(self.reject)
        else:
            self._button_box.hide()

        if self._text_content:
            self._textbrowser.setOpenLinks(True)
            self._textbrowser.setOpenExternalLinks(True)
            if self._text_format == "markdown":
                self._textbrowser.setMarkdown(self._text_content)
            elif self._text_format == "html":
                self._textbrowser.setHtml(self._text_content)
            elif self._text_format == "plaintext":
                self._textbrowser.setPlainText(self._text_content)
            else:
                self._textbrowser.setText(self._text_content)

        self._layout.addWidget(self._textbrowser)
        self._layout.addWidget(self._button_box)


def show_messagebox(
    text: str,
    icon: int | QPixmap,
    title: str = "Information",
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
    config = DialogConfig(
        text=text,
        title=title,
        icon=icon,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )
    return show_dialog(config)


def show_info_dialog(
    text: str,
    title: str = "Information",
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
    return show_messagebox(
        text=text,
        icon=QMessageBox.Information,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_warning_dialog(
    text: str,
    title: str = "Warning",
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
    return show_messagebox(
        text=text,
        icon=QMessageBox.Warning,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_critical_dialog(
    text: str,
    title: str = "Critical",
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
    return show_messagebox(
        text=text,
        icon=QMessageBox.Critical,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_question_dialog(
    text: str,
    title: str = "Question",
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Yes
    | QMessageBox.No,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
    return show_messagebox(
        text=text,
        icon=QMessageBox.Question,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_text_content(
    text_content: str,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
    size: Tuple[int, int] = None,
    title: str | None = "",
    icon: utils.IconType = None,
    buttons: int | QDialogButtonBox.StandardButtons | None = QDialogButtonBox.Ok,
    resizeable: bool = True,
):
    return show_custom_dialog(
        TextBrowserDialog,
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )
