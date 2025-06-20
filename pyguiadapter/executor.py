"""
@Time    : 2024.10.20
@File    : executor.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了函数执行器的抽象基类，所有函数执行器都应该继承自该类并实现相应抽象方法。
"""

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
        self, fn_info: FnInfo, arguments: Dict[str, Any], exception: BaseException
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
