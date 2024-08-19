from __future__ import annotations

import dataclasses
from typing import Callable, Literal, Any, Dict, List, Type

from . import executor
from . import utils


@dataclasses.dataclass
class ParameterInfo(object):
    default_value: Any
    typename: str
    type_args: List[Any] = dataclasses.field(default_factory=list)
    description: str | None = None


@dataclasses.dataclass
class FnInfo(object):
    fn: Callable
    display_name: str
    document: str = ""
    document_format: Literal["markdown", "html", "plaintext"] = "markdown"
    icon: utils.IconType = None
    group: str | None = None
    parameters: Dict[str, ParameterInfo] = dataclasses.field(default_factory=dict)
    cancelable: bool = False
    cancel_event_parameter_name: str = "cancel_event"
    executor: Type[executor.BaseFunctionExecutor] | None = None

    def is_cancelable(self) -> bool:
        if not self.cancelable:
            return False
        if not isinstance(self.cancel_event_parameter_name, str):
            return False
        return self.cancel_event_parameter_name.strip() != ""
