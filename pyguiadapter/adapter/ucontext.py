from __future__ import annotations

import dataclasses
import warnings
from collections.abc import Sequence
from concurrent.futures import Future
from typing import Set, Any, Tuple, Type

from qtpy.QtCore import QObject, Signal, Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QMessageBox, QWidget

from .custom_dialog import CustomDialogFactory, BaseCustomDialog
from ..windows.fnexec import FnExecuteWindow


@dataclasses.dataclass
class DialogConfig(object):
    text: str
    title: str | None = None
    icon: int | QPixmap | None = None
    detailed_text: str | None = None
    informative_text: str | None = None
    text_format: int | Qt.TextFormat | None = None
    buttons: int | QMessageBox.StandardButtons | Sequence[int] | None = None
    default_button: int | QMessageBox.StandardButtons | None = None
    escape_button: int | QMessageBox.StandardButtons | None = None

    def create_messagebox(self, parent: QWidget | None) -> QMessageBox:
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
            if isinstance(self.buttons, (int, QMessageBox.StandardButtons)):
                msgbox.setStandardButtons(self.buttons)
            else:
                buttons = 0
                for button in self.buttons:
                    buttons |= button
                msgbox.setDefaultButton(buttons)

        if self.default_button is not None:
            msgbox.setDefaultButton(self.default_button)

        if self.escape_button is not None:
            msgbox.setEscapeButton(self.escape_button)

        return msgbox


# noinspection PyMethodMayBeStatic,SpellCheckingInspection
class _Context(QObject):
    window_created = Signal(FnExecuteWindow)
    window_destroyed = Signal(FnExecuteWindow)
    # noinspection SpellCheckingInspection
    uprint = Signal(str, bool)
    show_dialog = Signal(Future, DialogConfig)
    show_custom_dialog = Signal(Future, object, dict)

    def __init__(self, parent):
        super().__init__(parent)

        self._windows: Set[FnExecuteWindow] = set()
        self._custom_dialog_factory = CustomDialogFactory()

        # noinspection PyUnresolvedReferences
        self.window_created.connect(self._on_window_created)
        # noinspection PyUnresolvedReferences
        self.window_destroyed.connect(self._on_window_closed)
        # noinspection PyUnresolvedReferences
        self.uprint.connect(self._on_uprint)
        # noinspection PyUnresolvedReferences
        self.show_dialog.connect(self._on_show_dialog)
        # noinspection PyUnresolvedReferences
        self.show_custom_dialog.connect(self._on_show_custom_dialog)

    @property
    def custom_dialog_factory(self) -> CustomDialogFactory:
        return self._custom_dialog_factory

    @property
    def current_window(self) -> FnExecuteWindow | None:
        for window in self._windows:
            if window.isActiveWindow():
                return window
        return None

    def clear_windows(self):
        self._windows.clear()

    def _on_window_created(self, window: FnExecuteWindow):
        if not isinstance(window, FnExecuteWindow):
            raise TypeError(f"expected FnExecuteWindow, got {type(window)}")
        self._windows.add(window)

    def _on_window_closed(self, window: FnExecuteWindow):
        if window not in self._windows:
            return
        self._windows.remove(window)

    def _on_uprint(self, msg: str, html: bool):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("FnExecuteWindow not found")
            print(msg)
            return
        win.append_log(msg, html)

    def _on_show_dialog(self, future: Future, config: DialogConfig):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("FnExecuteWindow not found")
            win = None
        dialog = config.create_messagebox(win)
        ret = dialog.exec_()
        future.set_result(ret)

    def _on_show_custom_dialog(
        self, future: Future, dialog_class: str | Type[BaseCustomDialog], kwargs: dict
    ):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("FnExecuteWindow not found")
            win = None
        dialog = _context.custom_dialog_factory.create(win, dialog_class, **kwargs)
        ret_code = dialog.exec_()
        result = dialog.get_result()
        future.set_result((ret_code, result))


_context = _Context(None)


# noinspection PyUnresolvedReferences
def window_created(window: FnExecuteWindow):
    global _context
    _context.window_created.emit(window)


# noinspection PyUnresolvedReferences
def window_closed(window: FnExecuteWindow):
    global _context
    _context.window_destroyed.emit(window)


def clear_windows():
    global _context
    _context.clear_windows()


def current_window() -> FnExecuteWindow | None:
    return _context.current_window


# noinspection SpellCheckingInspection
def uprint(*args, sep=" ", end="\n", html: bool = False):
    text = sep.join([str(arg) for arg in args]) + end
    # noinspection PyUnresolvedReferences
    _context.uprint.emit(text, html)


def show_dialog(config: DialogConfig) -> Any:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.show_dialog.emit(result_future, config)
    return result_future.result()


def show_custom_dialog(
    dialog_class: str | Type[BaseCustomDialog], **kwargs
) -> Tuple[int, Any]:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.show_custom_dialog.emit(result_future, dialog_class, kwargs)
    return result_future.result()
