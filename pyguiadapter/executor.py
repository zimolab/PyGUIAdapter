from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict

from qtpy.QtCore import QObject

from . import fn


class AlreadyExecutingError(RuntimeError):
    pass


class ExecuteStateListener(object):
    def before_execute(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_start(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_finish(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_result(
        self, fn_info: fn.FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        pass

    def on_execute_error(
        self, fn_info: fn.FnInfo, arguments: Dict[str, Any], exception: Exception
    ) -> None:
        pass


class BaseFunctionExecutor(QObject):

    def __init__(self, parent: QObject | None, listener: ExecuteStateListener | None):
        super().__init__(parent)

        self._listener = listener

    @property
    def listener(self) -> ExecuteStateListener | None:
        return self._listener

    @abstractmethod
    def execute(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]):
        pass

    @property
    @abstractmethod
    def is_executing(self) -> bool:
        pass

    @abstractmethod
    def try_cancel(self):
        pass
