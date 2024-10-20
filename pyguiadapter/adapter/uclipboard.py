"""
@Time    : 2024.10.20
@File    : uclipboard.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 提供了访问系统剪贴板的相关接口
"""

from concurrent.futures import Future

from typing import Optional

from ..window import (
    CLIPBOARD_GET_TEXT,
    CLIPBOARD_SET_TEXT,
    CLIPBOARD_GET_SELECTION_TEXT,
    CLIPBOARD_SET_SELECTION_TEXT,
    CLIPBOARD_SUPPORTS_SELECTION,
    CLIPBOARD_OWNS_CLIPBOARD,
    CLIPBOARD_OWNS_SELECTION,
)
from .ucontext import _context


def get_text() -> Optional[str]:
    """
    获取系统剪贴板中的文本内容。

    Returns:
        系统剪贴板中当前文本，如果剪贴板为空则返回None。
    """
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_GET_TEXT, None)
    return future.result()


def set_text(text: str) -> None:
    """
    设置系统剪贴板中当前文本。

    Args:
        text: 要设置的文本
    Returns:
        无返回值
    """
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_SET_TEXT, text)
    return future.result()


def supports_selection() -> bool:
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_SUPPORTS_SELECTION, None)
    return future.result()


def get_selection_text() -> Optional[str]:
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_GET_SELECTION_TEXT, None)
    return future.result()


def set_selection_text(text: str):
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_SET_SELECTION_TEXT, text)
    return future.result()


def owns_clipboard() -> bool:
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_OWNS_CLIPBOARD, None)
    return future.result()


def owns_selection() -> bool:
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_OWNS_SELECTION, None)
    return future.result()
