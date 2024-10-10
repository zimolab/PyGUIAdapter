import warnings
from concurrent.futures import Future
from typing import Any, Type, Optional, Callable

from qtpy.QtCore import QObject, Signal, QMutex

from ..utils import BaseCustomDialog
from ..utils.messagebox import show_messagebox
from ..windows.fnexec import BaseFnExecuteWindow


# noinspection PyMethodMayBeStatic,SpellCheckingInspection
class _Context(QObject):

    sig_current_window_created = Signal(BaseFnExecuteWindow)
    sig_current_window_destroyed = Signal()
    # noinspection SpellCheckingInspection
    sig_uprint = Signal(str, bool, bool)
    # noinspection SpellCheckingInspection
    sig_clear_output = Signal()
    sig_show_messagebox = Signal(Future, dict)
    sig_show_custom_dialog = Signal(Future, object, dict)
    sig_get_input = Signal(Future, object)
    sig_show_progressbar = Signal(dict)
    sig_hide_progressbar = Signal()
    sig_update_progressbar = Signal(int, str)
    sig_clipboard_operation = Signal(Future, int, object)

    def __init__(self, parent):
        super().__init__(parent)

        self._lock = QMutex()
        self._current_window: Optional[BaseFnExecuteWindow] = None

        # noinspection PyUnresolvedReferences
        self.sig_current_window_created.connect(self._on_current_window_created)
        # noinspection PyUnresolvedReferences
        self.sig_current_window_destroyed.connect(self._on_current_window_destroyed)
        # noinspection PyUnresolvedReferences
        self.sig_uprint.connect(self._on_uprint)
        # noinspection PyUnresolvedReferences
        self.sig_clear_output.connect(self._on_clear_output)
        # noinspection PyUnresolvedReferences
        self.sig_show_messagebox.connect(self._on_show_messagebox)
        # noinspection PyUnresolvedReferences
        self.sig_show_custom_dialog.connect(self._on_show_custom_dialog)
        # noinspection PyUnresolvedReferences
        self.sig_get_input.connect(self._on_get_input)
        # noinspection PyUnresolvedReferences
        self.sig_show_progressbar.connect(self._on_show_progressbar)
        # noinspection PyUnresolvedReferences
        self.sig_hide_progressbar.connect(self._on_hide_progressbar)
        # noinspection PyUnresolvedReferences
        self.sig_update_progressbar.connect(self._on_update_progressbar)
        # noinspection PyUnresolvedReferences
        self.sig_clipboard_operation.connect(self._on_clipboard_operation)

    @property
    def current_window(self) -> Optional[BaseFnExecuteWindow]:
        return self._current_window

    def is_function_cancelled(self) -> bool:
        self._lock.lock()
        if not isinstance(self._current_window, BaseFnExecuteWindow):
            self._lock.unlock()
            return False
        cancelled = (
            self._current_window.executor.is_executing
            and self._current_window.executor.is_cancelled
        )
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

    def _on_current_window_created(self, window: BaseFnExecuteWindow):
        if not isinstance(window, BaseFnExecuteWindow):
            raise TypeError(f"FnExecuteWindow expected, got {type(window)}")
        self._try_cleanup_old_window()
        self._current_window = window

    def _on_current_window_destroyed(self):
        self._current_window.deleteLater()
        self._current_window = None

    def _on_uprint(self, msg: str, html: bool, scroll_to_bottom: bool):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            print(msg)
            return
        win.append_output(msg, html, scroll_to_bottom)

    def _on_clear_output(self):
        wind = self.current_window
        if not isinstance(wind, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            return
        wind.clear_output()

    def _on_show_messagebox(self, future: Future, kwargs: dict):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        ret = show_messagebox(win, **kwargs)
        future.set_result(ret)

    def _on_show_custom_dialog(
        self,
        future: Future,
        dialog_class: Type[BaseCustomDialog],
        kwargs: dict,
    ):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        # dialog = dialog_class.new_instance(win, **kwargs)
        # ret_code = dialog.exec_()
        # result = dialog.get_result()
        # dialog.deleteLater()
        # future.set_result((ret_code, result))
        result = dialog_class.show_and_get_result(win, **kwargs)
        future.set_result(result)

    def _on_get_input(
        self, future: Future, get_input_impl: Callable[[BaseFnExecuteWindow], Any]
    ):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        result = get_input_impl(win)
        future.set_result(result)

    def _on_show_progressbar(self, config: dict):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        win.update_progressbar_config(config)
        win.show_progressbar()

    def _on_hide_progressbar(self):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        win.update_progressbar_config({})
        win.hide_progressbar()

    def _on_update_progressbar(self, progress: int, msg: str):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            win = None
        win.update_progress(progress, msg)

    def _on_clipboard_operation(self, future: Future, operation: int, data: object):
        win = self.current_window
        if not isinstance(win, BaseFnExecuteWindow):
            warnings.warn("current_window is None")
            return
        win.on_clipboard_operation(future, operation, data)


_context = _Context(None)

################################################################################################
# Functions below with a leading '_' are for internal use only. DO NOT USE THEM IN USER'S CODE.#
# Other functions are free to use in user's function code.                                     #
################################################################################################


def _reset():
    global _context
    _context.reset()


# noinspection PyUnresolvedReferences
def _current_window_created(window: BaseFnExecuteWindow):
    global _context
    _context.sig_current_window_created.emit(window)


# noinspection PyUnresolvedReferences
def _current_window_destroyed():
    global _context
    _context.sig_current_window_destroyed.emit()


def get_current_window() -> Optional[BaseFnExecuteWindow]:
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
    _context.sig_uprint.emit(text, html, scroll_to_bottom)


def clear_output():
    global _context
    # noinspection PyUnresolvedReferences
    _context.sig_clear_output.emit()
