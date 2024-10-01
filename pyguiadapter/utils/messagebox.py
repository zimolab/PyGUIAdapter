import dataclasses
from typing import Any, Literal, Tuple, Type, Optional, Union

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import (
    QWidget,
    QDialogButtonBox,
    QTextBrowser,
    QVBoxLayout,
    QMessageBox,
)

from ._core import get_traceback
from .dialog import BaseCustomDialog
from ._ui import IconType, get_icon

StandardButton: Type[QMessageBox.StandardButton] = QMessageBox.StandardButton
StandardButtons: Type[QMessageBox.StandardButtons] = QMessageBox.StandardButtons
TextFormat = Qt.TextFormat


#########Standard MessageBox#################
def show_warning_message(
    parent: QWidget,
    message: str,
    title: str = "Warning",
) -> Union[int, StandardButton]:
    return QMessageBox.warning(parent, title, message)


def show_critical_message(
    parent: QWidget,
    message: str,
    title: str = "Critical",
) -> Union[int, StandardButton]:
    return QMessageBox.critical(parent, title, message)


def show_info_message(
    parent: QWidget,
    message: str,
    title: str = "Information",
) -> Union[int, StandardButton]:
    return QMessageBox.information(parent, title, message)


def show_question_message(
    parent: QWidget,
    message: str,
    title: str = "Question",
    buttons: Union[int, StandardButton, StandardButtons, None] = None,
) -> Union[int, StandardButton]:
    if buttons is None:
        return QMessageBox.question(parent, title, message)
    return QMessageBox.question(parent, title, message, buttons)


###########Custom MessageBox#############
@dataclasses.dataclass
class MessageBoxConfig(object):
    text: str = ""
    title: Optional[str] = None
    icon: Union[int, QPixmap, None] = None
    detailed_text: Optional[str] = None
    informative_text: Optional[str] = None
    text_format: Optional[TextFormat] = None
    buttons: Union[StandardButton, StandardButtons, int, None] = None
    default_button: Optional[StandardButton] = None
    escape_button: Optional[StandardButton] = None

    def create_messagebox(self, parent: Optional[QWidget]) -> QMessageBox:
        # noinspection SpellCheckingInspection,PyArgumentList
        msgbox = QMessageBox(parent)
        msgbox.setText(self.text)

        if self.title:
            msgbox.setWindowTitle(self.title)

        if self.icon is not None:
            msgbox.setIcon(self.icon)

        if isinstance(self.icon, QPixmap):
            msgbox.setIconPixmap(self.icon)

        if self.informative_text:
            msgbox.setInformativeText(self.informative_text)

        if self.detailed_text:
            msgbox.setDetailedText(self.detailed_text)

        if self.text_format is not None:
            msgbox.setTextFormat(self.text_format)

        if self.buttons is not None:
            msgbox.setStandardButtons(self.buttons)

        if self.default_button is not None:
            msgbox.setDefaultButton(self.default_button)

        if self.escape_button is not None:
            msgbox.setEscapeButton(self.escape_button)

        return msgbox


def show_messagebox(parent: Optional[QWidget], **kwargs) -> Union[int, StandardButton]:
    config = MessageBoxConfig(**kwargs)
    msg_box = config.create_messagebox(parent)
    ret_code = msg_box.exec_()
    msg_box.deleteLater()
    return ret_code


def show_exception_messagebox(
    parent: Optional[QWidget],
    exception: Exception,
    message: str = "",
    title: str = "Error",
    detail: bool = True,
    show_error_type: bool = True,
    **kwargs,
) -> Union[int, StandardButton]:
    if not detail:
        detail_msg = None
    else:
        detail_msg = get_traceback(exception)

    if show_error_type:
        error_msg = f"{type(exception).__name__}: {exception}"
    else:
        error_msg = str(exception)

    if message:
        error_msg = f"{message}{error_msg}"

    return show_messagebox(
        parent,
        text=error_msg,
        title=title,
        icon=QMessageBox.Critical,
        detailed_text=detail_msg,
        **kwargs,
    )


############Text Dialogs##############
class TextBrowserMessageBox(BaseCustomDialog):

    DEFAULT_SIZE = (585, 523)

    def __init__(
        self,
        parent: Optional[QWidget],
        text_content: str,
        text_format: Literal["markdown", "plaintext", "html"] = "markdown",
        size: Optional[Tuple[int, int]] = None,
        title: Optional[str] = None,
        icon: IconType = None,
        buttons: Union[
            int, QDialogButtonBox.StandardButtons, None
        ] = QDialogButtonBox.Ok,
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
            icon = get_icon(self._icon) or QIcon()
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
