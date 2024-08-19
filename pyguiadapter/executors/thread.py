from __future__ import annotations

import threading
import traceback
import warnings
from collections import OrderedDict
from typing import Any, Dict

from qtpy.QtCore import QObject, QThread, Signal

from ..executor import BaseFunctionExecutor, ExecuteStateListener, AlreadyExecutingError
from ..fn import FnInfo


class _WorkerThread(QThread):

    result_ready = Signal(FnInfo, dict, object)
    error_raised = Signal(FnInfo, dict, Exception)
    cancel_requested = Signal()

    # noinspection PyUnresolvedReferences
    def __init__(
        self,
        parent: QObject | None,
        fn_info: FnInfo,
        arguments: Dict[str, Any],
    ):
        super().__init__(parent)
        self._fn_info = fn_info
        self._arguments = OrderedDict(arguments)
        self._cancel_event: threading.Event | None = None

        if fn_info.is_cancelable():
            self.cancel_requested.connect(self._on_cancel_requested)

    # noinspection PyUnresolvedReferences
    def run(self):
        try:
            result = self._on_execute()
        except Exception as e:
            traceback.print_exc()
            self.error_raised.emit(self._fn_info, self._arguments, e)
        else:
            self.result_ready.emit(self._fn_info, self._arguments, result)

    def request_cancel(self):
        if not self._fn_info.is_cancelable():
            warnings.warn("function is not cancelable")
            return
        if self._cancel_event is None:
            warnings.warn("cancel event is not created")
            return
        # noinspection PyUnresolvedReferences
        self.cancel_requested.emit()

    def _on_execute(self) -> Any:
        arguments = self._arguments.copy()
        if self._fn_info.is_cancelable():
            self._cancel_event = threading.Event()
            arguments[self._fn_info.cancel_event_parameter_name] = self._cancel_event
        func = self._fn_info.fn
        result = func(**arguments)
        self._cancel_event = None
        return result

    def _on_cancel_requested(self):
        if not self._fn_info.is_cancelable():
            warnings.warn("current function is not cancellable")
            return
        if self._cancel_event is None:
            warnings.warn("cancel event is not created")
            return
        self._cancel_event.set()


class ThreadedFunctionExecutor(BaseFunctionExecutor):
    def __init__(self, parent: QObject | None, listener: ExecuteStateListener | None):
        super().__init__(parent, listener)

        self._worker_thread: _WorkerThread | None = None

    @property
    def is_executing(self) -> bool:
        return self._worker_thread is not None

    # noinspection PyUnresolvedReferences
    def execute(self, fn_info: FnInfo, arguments: Dict[str, Any]):
        if self.is_executing:
            raise AlreadyExecutingError("function is already executing")

        def _callback_on_execute_start():
            self._on_execute_start(fn_info, arguments)

        def _callback_on_execute_finish():
            self._on_execute_finish(fn_info, arguments)

        self._reset_worker_thread()
        self._before_execute(fn_info, arguments)
        try:
            self._worker_thread = _WorkerThread(self, fn_info, arguments)
            self._worker_thread.started.connect(_callback_on_execute_start)
            self._worker_thread.finished.connect(_callback_on_execute_finish)
            self._worker_thread.error_raised.connect(self._on_execute_error)
            self._worker_thread.result_ready.connect(self._on_execute_result)
            self._worker_thread.start()
        except Exception as e:
            traceback.print_exc()
            self._on_execute_error(fn_info, arguments, e)
            self._on_execute_finish(fn_info, arguments)

    def try_cancel(self):
        if not self.is_executing:
            warnings.warn("function is not executing")
            return
        self._worker_thread.request_cancel()

    def _before_execute(self, fn_info: FnInfo, arguments: Dict[str, Any]):
        if self._listener:
            self._listener.before_execute(fn_info, arguments)

    def _on_execute_error(
        self, fn_info: FnInfo, arguments: Dict[str, Any], error: Exception
    ):
        if self._listener:
            self._listener.on_execute_error(fn_info, arguments, error)

    def _on_execute_start(self, fn_info: FnInfo, arguments: Dict[str, Any]):
        if self._listener:
            self._listener.on_execute_start(fn_info, arguments)

    def _on_execute_finish(self, fn_info: FnInfo, arguments: Dict[str, Any]):
        self._reset_worker_thread()
        if self._listener:
            self._listener.on_execute_finish(fn_info, arguments)

    def _on_execute_result(
        self, fn_info: FnInfo, arguments: Dict[str, Any], result: Any
    ):
        if self._listener:
            self._listener.on_execute_result(fn_info, arguments, result)

    def _reset_worker_thread(self):
        if self._worker_thread is not None:
            self._worker_thread.setParent(None)
            self._worker_thread.deleteLater()
            self._worker_thread = None
