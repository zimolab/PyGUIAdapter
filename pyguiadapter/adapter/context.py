from __future__ import annotations

from typing import List, Set

from qtpy.QtCore import QObject, Signal

from ..windows.fnexec import FnExecuteWindow


# noinspection PyMethodMayBeStatic
class _Context(QObject):
    window_created = Signal(FnExecuteWindow)
    window_destroyed = Signal(FnExecuteWindow)

    def __init__(self, parent):
        super().__init__(parent)

        self._windows: Set[FnExecuteWindow] = set()

        # noinspection PyUnresolvedReferences
        self.window_created.connect(self._on_window_created)
        # noinspection PyUnresolvedReferences
        self.window_destroyed.connect(self._on_window_destroyed)

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

    def _on_window_destroyed(self, window: FnExecuteWindow):
        if not window in self._windows:
            return
        self._windows.remove(window)


_context = _Context(None)


# noinspection PyUnresolvedReferences
def window_created(window: FnExecuteWindow):
    global _context
    _context.window_created.emit(window)


# noinspection PyUnresolvedReferences
def window_destroyed(window: FnExecuteWindow):
    global _context
    _context.window_destroyed.emit(window)


def clear_windows():
    global _context
    _context.clear_windows()


def current_window() -> FnExecuteWindow | None:
    return _context.current_window
