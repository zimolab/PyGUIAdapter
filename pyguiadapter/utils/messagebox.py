import dataclasses
import traceback
from typing import Type, Optional, Union

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QMessageBox, QWidget

from ._core import get_traceback

StandardButton: Type[QMessageBox.StandardButton] = QMessageBox.StandardButton
StandardButtons: Type[QMessageBox.StandardButtons] = QMessageBox.StandardButtons
TextFormat = Qt.TextFormat


@dataclasses.dataclass
class MessageBoxConfig(object):
    text: str
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


def show_exception_message(
    parent: Optional[QWidget],
    exception: Exception,
    message: str = "",
    title: str = "Error",
    detail: bool = True,
    show_error_type: bool = True,
    **kwargs,
) -> Union[int, StandardButton]:
    traceback.print_exc()
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
    msgbox = MessageBoxConfig(
        title=title,
        text=error_msg,
        icon=QMessageBox.Critical,
        detailed_text=detail_msg,
        **kwargs,
    ).create_messagebox(parent)
    return msgbox.exec_()
