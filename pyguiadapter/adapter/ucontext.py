from __future__ import annotations

import warnings
from collections.abc import Callable
from concurrent.futures import Future
from typing import Any, Type

from qtpy.QtCore import QObject, Signal, QMutex

from ._dialog import CustomDialogFactory, BaseCustomDialog
from ..utils import MessageBoxConfig
from ..windows.fnexec import FnExecuteWindow


# noinspection PyMethodMayBeStatic,SpellCheckingInspection
class _Context(QObject):

    current_window_created = Signal(FnExecuteWindow)
    current_window_destroyed = Signal()
    # noinspection SpellCheckingInspection
    uprint = Signal(str, bool, bool)
    show_messagebox = Signal(Future, MessageBoxConfig)
    show_custom_dialog = Signal(Future, object, dict)
    get_input_requested = Signal(Future, object)
    show_progressbar = Signal(dict)
    hide_progressbar = Signal()
    update_progress = Signal(int, str)

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
        # noinspection PyUnresolvedReferences
        self.get_input_requested.connect(self._on_get_input_requested)
        # noinspection PyUnresolvedReferences
        self.show_progressbar.connect(self._on_show_progressbar)
        # noinspection PyUnresolvedReferences
        self.hide_progressbar.connect(self._on_hide_progressbar)
        # noinspection PyUnresolvedReferences
        self.update_progress.connect(self._on_update_progress)

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

    def _on_uprint(self, msg: str, html: bool, scroll_to_bottom: bool):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            print(msg)
            return
        win.append_output(msg, html, scroll_to_bottom)

    def _on_show_messagebox(self, future: Future, config: MessageBoxConfig):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        msgbox = config.create_messagebox(win)
        ret = msgbox.exec_()
        msgbox.deleteLater()
        future.set_result(ret)

    def _on_show_custom_dialog(
        self, future: Future, dialog_class: str | Type[BaseCustomDialog], kwargs: dict
    ):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        dialog = _context.custom_dialog_factory.create(win, dialog_class, **kwargs)
        ret_code = dialog.exec_()
        result = dialog.get_result()
        dialog.deleteLater()
        future.set_result((ret_code, result))

    def _on_get_input_requested(
        self, future: Future, get_input_impl: Callable[[FnExecuteWindow], Any]
    ):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        result = get_input_impl(win)
        future.set_result(result)

    def _on_show_progressbar(self, config: dict):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        win.update_progressbar_config(config)
        win.show_progressbar()

    def _on_hide_progressbar(self):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        win.update_progressbar_config({})
        win.hide_progressbar()

    def _on_update_progress(self, progress: int, msg: str):
        win = self.current_window
        if not isinstance(win, FnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        win.update_progress(progress, msg)


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
def uprint(*args, sep=" ", end="\n", html: bool = False, scroll_to_bottom: bool = True):
    global _context
    text = sep.join([str(arg) for arg in args]) + end
    # noinspection PyUnresolvedReferences
    _context.uprint.emit(text, html, scroll_to_bottom)
