from __future__ import annotations

import dataclasses
import warnings
from collections.abc import Sequence
from concurrent.futures import Future
from typing import Any, Tuple, Type

from qtpy.QtCore import QObject, Signal, Qt, QMutex
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QMessageBox, QWidget

from ._dialog import CustomDialogFactory, BaseCustomDialog
from ..windows.fnexec import FnExecuteWindow


@dataclasses.dataclass
class MessageBoxConfig(object):
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

    current_window_created = Signal(FnExecuteWindow)
    current_window_destroyed = Signal()

    # noinspection SpellCheckingInspection
    uprint = Signal(str, bool)

    show_messagebox = Signal(Future, MessageBoxConfig)
    show_custom_dialog = Signal(Future, object, dict)

    def __init__(self, parent):
        super().__init__(parent)

        self._lock = QMutex()

        self._current_window: FnExecuteWindow | None = None

        self._custom_dialog_factory = CustomDialogFactory()

        # noinspection PyUnresolvedReferences
        self.current_window_created.connect(self._on_current_window_created)
        # noinspection PyUnresolvedReferences
        self.current_window_destroyed.connect(self._on_current_window_destroyed)

        # noinspection PyUnresolvedReferences
        self.uprint.connect(self._on_uprint)

        # noinspection PyUnresolvedReferences
        self.show_messagebox.connect(self._on_show_messagebox)
        # noinspection PyUnresolvedReferences
        self.show_custom_dialog.connect(self._on_show_custom_dialog)

    @property
    def custom_dialog_factory(self) -> CustomDialogFactory:
        return self._custom_dialog_factory

    @property
    def current_window(self) -> FnExecuteWindow | None:
        return self._current_window

    def is_function_cancelled(self) -> bool:
        wind = self.current_window
        if not isinstance(wind, FnExecuteWindow):
            return False
        self._lock.lock()
        executor = wind.current_executor
        cancelled = False
        if executor.is_executing:
            cancelled = executor.is_cancelled
        self._lock.unlock()
        return cancelled

    def reset(self):
        self._try_cleanup_old_window()

    def _try_cleanup_old_window(self):
        if self._current_window is not None:
            try:
                self._current_window.close()
                self._current_window.deleteLater()
            except Exception as e:
                warnings.warn(f"error while closing window: {e}")
            finally:
                self._current_window = None

    def _on_current_window_created(self, window: FnExecuteWindow):
        if not isinstance(window, FnExecuteWindow):
            raise TypeError(f"FnExecuteWindow expected, got {type(window)}")
        self._try_cleanup_old_window()
        self._current_window = window

    def _on_current_window_destroyed(self):
        self._current_window.deleteLater()
        self._current_window = None

    def _on_uprint(self, msg: str, html: bool):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            print(msg)
            return
        win.append_log(msg, html)

    def _on_show_messagebox(self, future: Future, config: MessageBoxConfig):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        msgbox = config.create_messagebox(win)
        ret = msgbox.exec_()
        future.set_result(ret)

    def _on_show_custom_dialog(
        self, future: Future, dialog_class: str | Type[BaseCustomDialog], kwargs: dict
    ):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None0")
            win = None
        dialog = _context.custom_dialog_factory.create(win, dialog_class, **kwargs)
        ret_code = dialog.exec_()
        result = dialog.get_result()
        future.set_result((ret_code, result))


_context = _Context(None)

################################################################################################
# Functions below with a leading '_' are for internal use only. DO NOT USE THEM IN USER'S CODE.#
# Other functions are free to use in user's function code.                                     #
################################################################################################


def _reset():
    global _context
    _context.reset()


# noinspection PyUnresolvedReferences
def _current_window_created(window: FnExecuteWindow):
    global _context
    _context.current_window_created.emit(window)


# noinspection PyUnresolvedReferences
def _current_window_destroyed():
    global _context
    _context.current_window_destroyed.emit()


def get_current_window() -> FnExecuteWindow | None:
    global _context
    return _context.current_window


def is_function_cancelled() -> bool:
    global _context
    return _context.is_function_cancelled()


# noinspection SpellCheckingInspection
def uprint(*args, sep=" ", end="\n", html: bool = False):
    global _context
    text = sep.join([str(arg) for arg in args]) + end
    # noinspection PyUnresolvedReferences
    _context.uprint.emit(text, html)


def show_messagebox(config: MessageBoxConfig) -> Any:
    global _context
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.show_messagebox.emit(result_future, config)
    return result_future.result()


def show_custom_dialog(
    dialog_class: str | Type[BaseCustomDialog], **kwargs
) -> Tuple[int, Any]:
    global _context
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.show_custom_dialog.emit(result_future, dialog_class, kwargs)
    return result_future.result()
