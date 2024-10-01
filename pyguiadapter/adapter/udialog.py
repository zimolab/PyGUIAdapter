from concurrent.futures import Future
from typing import Any, Literal, Tuple, Type, Optional, Union

from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (
    QDialogButtonBox,
    QMessageBox,
)

from .ucontext import _context
from ..utils import IconType
from ..utils import io
from ..utils.dialog import BaseCustomDialog
from ..utils.messagebox import TextBrowserMessageBox, StandardButton, StandardButtons


def show_custom_dialog(dialog_class: Type[BaseCustomDialog], **kwargs) -> Any:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.sig_show_custom_dialog.emit(result_future, dialog_class, kwargs)
    return result_future.result()


def _show_messagebox(
    text: str,
    icon: Union[int, QPixmap],
    title: str = "Information",
    buttons: Union[StandardButton, StandardButtons] = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> Union[int, StandardButton]:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    args = dict(
        text=text,
        title=title,
        icon=icon,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )
    _context.sig_show_messagebox.emit(result_future, args)
    return result_future.result()


def show_info_messagebox(
    text: str,
    title: str = "Information",
    buttons: Union[StandardButton, StandardButtons] = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.Ok,
    **kwargs,
) -> Union[int, StandardButton]:
    return _show_messagebox(
        text=text,
        icon=QMessageBox.Information,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_warning_messagebox(
    text: str,
    title: str = "Warning",
    buttons: Union[StandardButton, StandardButtons] = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.Ok,
    **kwargs,
) -> Union[int, StandardButton]:
    return _show_messagebox(
        text=text,
        icon=QMessageBox.Warning,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_critical_messagebox(
    text: str,
    title: str = "Critical",
    buttons: Union[StandardButton, StandardButtons] = QMessageBox.Ok,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> Union[int, StandardButton]:
    return _show_messagebox(
        text=text,
        icon=QMessageBox.Critical,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_question_messagebox(
    text: str,
    title: str = "Question",
    buttons: Union[StandardButton, StandardButtons] = QMessageBox.Yes | QMessageBox.No,
    default_button: StandardButton = QMessageBox.NoButton,
    **kwargs,
) -> Union[int, StandardButton]:
    return _show_messagebox(
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
    title: Optional[str] = "",
    icon: IconType = None,
    buttons: Union[int, QDialogButtonBox.StandardButtons, None] = QDialogButtonBox.Ok,
    resizeable: bool = True,
):
    return show_custom_dialog(
        TextBrowserMessageBox,
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
    title: Optional[str] = "",
    icon: IconType = None,
    buttons: Union[int, QDialogButtonBox.StandardButtons, None] = QDialogButtonBox.Ok,
    resizeable: bool = True,
):
    text_content = io.read_text_file(text_file)
    return show_text_content(
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )
