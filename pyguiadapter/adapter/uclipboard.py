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
    future = Future()
    _context.sig_clipboard_operation.emit(future, CLIPBOARD_GET_TEXT, None)
    return future.result()


def set_text(text: str):
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
