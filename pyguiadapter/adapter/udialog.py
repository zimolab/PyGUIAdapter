from __future__ import annotations

from typing import Any, Literal, Tuple

from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import (
    QWidget,
    QDialogButtonBox,
    QTextBrowser,
    QVBoxLayout,
    QMessageBox,
)

from .. import utils
from ._dialog import BaseCustomDialog
from .ucontext import show_messagebox, MessageBoxConfig, show_custom_dialog

StandardButton = utils.StandardButton
StandardButtons = utils.StandardButtons


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

        # noinspection PyArgumentList
        self._button_box = QDialogButtonBox(self)
        # noinspection SpellCheckingInspection
        self._textbrowser = QTextBrowser(self)
        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

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


def show_text_file(
    text_file: str,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
    size: Tuple[int, int] = None,
    title: str | None = "",
    icon: utils.IconType = None,
    buttons: int | QDialogButtonBox.StandardButtons | None = QDialogButtonBox.Ok,
    resizeable: bool = True,
):
    text_content = utils.read_text_file(text_file)
    return show_text_content(
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )


def show_about_info():
    """TODO impl show about dialog"""
    pass


def _show_messagebox(
    text: str,
    icon: int | QPixmap,
    title: str = "Information",
    buttons: StandardButton | StandardButtons = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> int | StandardButton:
    config = MessageBoxConfig(
        text=text,
        title=title,
        icon=icon,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )
    return show_messagebox(config)


def show_info_dialog(
    text: str,
    title: str = "Information",
    buttons: StandardButton | StandardButtons = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> int | StandardButton:
    return _show_messagebox(
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
    buttons: StandardButton | StandardButtons = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> int | StandardButton:
    return _show_messagebox(
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
    buttons: StandardButton | StandardButtons = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> int | StandardButton:
    return _show_messagebox(
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
    buttons: StandardButton | StandardButtons = QMessageBox.Yes | QMessageBox.No,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> int | StandardButton:
    return _show_messagebox(
        text=text,
        icon=QMessageBox.Question,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )
