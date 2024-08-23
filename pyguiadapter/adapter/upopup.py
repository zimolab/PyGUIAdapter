from __future__ import annotations

from typing import Sequence

from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QMessageBox

from .ucontext import show_messagebox, MessageBoxConfig


def _show_messagebox(
    text: str,
    icon: int | QPixmap,
    title: str = "Information",
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
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
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
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
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
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
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Ok,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
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
    buttons: int | QMessageBox.StandardButtons | Sequence[int] = QMessageBox.Yes
    | QMessageBox.No,
    default_button: int = QMessageBox.NoButton,
    **kwargs,
) -> int | QMessageBox.StandardButton:
    return _show_messagebox(
        text=text,
        icon=QMessageBox.Question,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )
