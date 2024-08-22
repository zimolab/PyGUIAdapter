# TODO: implement process-based function executor
from typing import Dict, Any

from .. import fn
from ..executor import BaseFunctionExecutor


class ProcessFunctionExecutor(BaseFunctionExecutor):

    def execute(self, fn_info: fn.FnInfo, arguments: Dict[str, Any]):
        raise NotImplementedError()

    @property
    def is_executing(self) -> bool:
        raise NotImplementedError()

    def try_cancel(self):
        raise NotImplementedError()

    @property
    def is_cancelled(self) -> bool:
        raise NotImplementedError()
