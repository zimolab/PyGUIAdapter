import threading
import traceback
import warnings
from collections import OrderedDict
from typing import Any, Dict, Optional

from qtpy.QtCore import QObject, QThread, Signal

from ..exceptions import FunctionExecutingError
from ..executor import BaseFunctionExecutor, ExecuteStateListener
from ..fn import FnInfo


class _WorkerThread(QThread):

    result_ready = Signal(FnInfo, dict, object)
    error_raised = Signal(FnInfo, dict, Exception)
    cancel_requested = Signal()

    # noinspection PyUnresolvedReferences
    def __init__(
        self,
        parent: Optional[QObject],
        fn_info: FnInfo,
        arguments: Dict[str, Any],
    ):
        super().__init__(parent)
        self._fn_info = fn_info
        self._arguments = OrderedDict(arguments)

        self._cancel_event = threading.Event()
        self.cancel_requested.connect(self._on_cancel_requested)

    def is_cancel_event_set(self) -> bool:
        return self._cancel_event.is_set()

    # noinspection PyUnresolvedReferences
    def run(self):
        try:
            self._cancel_event.clear()
            result = self._on_execute()
        except Exception as e:
            traceback.print_exc()
            self.error_raised.emit(self._fn_info, self._arguments, e)
        else:
            self.result_ready.emit(self._fn_info, self._arguments, result)
        finally:
            self._cancel_event.clear()

    def _on_execute(self) -> Any:
        arguments = self._arguments.copy()
        func = self._fn_info.fn
        result = func(**arguments)
        return result

    def _on_cancel_requested(self):
        self._cancel_event.set()


class ThreadFunctionExecutor(BaseFunctionExecutor):

    def __init__(
        self, parent: Optional[QObject], listener: Optional[ExecuteStateListener]
    ):
        super().__init__(parent, listener)

        self._worker_thread: Optional[_WorkerThread] = None

    @property
    def is_executing(self) -> bool:
        return self._worker_thread is not None

    @property
    def is_cancelled(self) -> bool:
        if not self.is_executing:
            return False
        return self._worker_thread.is_cancel_event_set()

    # noinspection PyUnresolvedReferences
    def execute(self, fn_info: FnInfo, arguments: Dict[str, Any]):
        if self.is_executing:
            raise FunctionExecutingError("function is already executing")

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
        if self.is_cancelled:
            warnings.warn("function is already cancelled")
            return
        # noinspection PyUnresolvedReferences
        self._worker_thread.cancel_requested.emit()

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
