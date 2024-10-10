from typing import Optional

from .ucontext import _context
from ..toast import ToastConfig
from ..windows.fnexec import BaseFnExecuteWindow


def _on_show_toast(
    message: str, duration: int, config: Optional[ToastConfig], clear: bool
) -> None:
    wind = _context.current_window
    if not isinstance(wind, BaseFnExecuteWindow):
        return
    wind.show_toast(message, duration, config, clear)
    wind = None


def _on_clear_toasts() -> None:
    wind = _context.current_window
    if not isinstance(wind, BaseFnExecuteWindow):
        return
    wind.clear_toasts()
    wind = None


def show_toast(
    message: str,
    duration: int = 3000,
    config: Optional[ToastConfig] = None,
    clear: bool = False,
) -> None:
    _context.sig_show_toast.emit(message, duration, config, clear)


def clear_toasts():
    _context.sig_clear_output.emit()


_context.sig_show_toast.connect(_on_show_toast)
_context.sig_clear_toasts.connect(_on_clear_toasts)
