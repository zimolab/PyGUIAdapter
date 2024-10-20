"""
@Time    : 2024.10.20
@File    : utoast.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 提供toast消息弹窗相关的功能
"""

from typing import Optional

from .ucontext import _context
from ..toast import ToastConfig

# noinspection PyProtectedMember
from ..windows.fnexec._base import BaseFnExecuteWindow


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


_context.sig_show_toast.connect(_on_show_toast)
_context.sig_clear_toasts.connect(_on_clear_toasts)


def show_toast(
    message: str,
    duration: int = 3000,
    config: Optional[ToastConfig] = None,
    clear: bool = False,
) -> None:
    """
    显示toast消息

    Args:
        message: toast消息内容
        duration: toast显示时间，单位为毫秒
        config: toast配置
        clear: 是否清除之前的toast消息

    Returns:
        无返回值
    """
    _context.sig_show_toast.emit(message, duration, config, clear)


def clear_toasts() -> None:
    """
    清除所有已发出的toast消息。

    Returns:
        无返回值
    """
    _context.sig_clear_output.emit()
