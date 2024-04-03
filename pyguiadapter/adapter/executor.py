import copy
import traceback

from PyQt6.QtCore import QThread, pyqtSignal

from pyguiadapter.adapter.bundle import FunctionBundle


class FunctionExecutor(QThread):
    exception_occurred = pyqtSignal(BaseException)
    result_ready = pyqtSignal(object)

    def __init__(self, func_bundle: FunctionBundle, arguments: dict, parent=None):
        super().__init__(parent)
        self._func_bundle = func_bundle
        self._arguments = copy.deepcopy(arguments)

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
        return self._func_bundle.execute_function(**self._arguments)
