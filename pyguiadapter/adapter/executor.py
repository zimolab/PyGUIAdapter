import copy
import threading
import traceback
from typing import Optional

from PyQt6.QtCore import QThread, pyqtSignal

from .bundle import FunctionBundle


class FunctionExecutor(QThread):
    exception_occurred = pyqtSignal(BaseException)
    result_ready = pyqtSignal(object)
    cancel_requested = pyqtSignal()

    def __init__(self, func_bundle: FunctionBundle, arguments: dict, parent=None):
        super().__init__(parent)
        self._func_bundle = func_bundle
        self._arguments = copy.deepcopy(arguments)

        self._cancel_event: Optional[threading.Event] = None
        if func_bundle.cancelable:
            # noinspection PyUnresolvedReferences
            self.cancel_requested.connect(self._on_cancel_requested)

    def run(self):
        try:
            result = self.on_execute()
        except BaseException as e:
            traceback.print_exc()
            # noinspection PyUnresolvedReferences
            self.exception_occurred.emit(e)
        else:
            # noinspection PyUnresolvedReferences
            self.result_ready.emit(result)

    def on_execute(self):
        arguments = {**self._arguments}
        if self._func_bundle.cancelable:
            self._cancel_event = threading.Event()
            cancel_event_param_name = self._func_bundle.cancel_event_param_name
            arguments[cancel_event_param_name] = self._cancel_event

        ret = self._func_bundle.execute_function(**arguments)
        self._cancel_event = None
        return ret

    def _on_cancel_requested(self):
        if self._cancel_event is None:
            return
        self._cancel_event.set()
