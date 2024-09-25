from abc import abstractmethod
from typing import Any, Dict, Optional

from qtpy.QtCore import QObject

from .fn import FnInfo


class ExecuteStateListener(object):
    def before_execute(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_start(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_finish(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_result(
        self, fn_info: FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        pass

    def on_execute_error(
        self, fn_info: FnInfo, arguments: Dict[str, Any], exception: Exception
    ) -> None:
        pass


class BaseFunctionExecutor(QObject):

    def __init__(
        self, parent: Optional[QObject], listener: Optional[ExecuteStateListener]
    ):
        super().__init__(parent)

        self._listener = listener

    @property
    def listener(self) -> Optional[ExecuteStateListener]:
        return self._listener

    @abstractmethod
    def execute(self, fn_info: FnInfo, arguments: Dict[str, Any]):
        pass

    @property
    @abstractmethod
    def is_executing(self) -> bool:
        pass

    @abstractmethod
    def try_cancel(self):
        pass

    @property
    @abstractmethod
    def is_cancelled(self) -> bool:
        pass
