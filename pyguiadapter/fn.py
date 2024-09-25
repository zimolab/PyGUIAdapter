import dataclasses
from typing import Callable, Literal, Any, Dict, List, Type, Optional, ForwardRef

from . import utils


@dataclasses.dataclass
class ParameterInfo(object):
    default_value: Any
    type: Type
    typename: str
    type_args: List[Any] = dataclasses.field(default_factory=list)
    description: Optional[str] = None


@dataclasses.dataclass
class FnInfo(object):
    fn: Callable
    display_name: str
    document: str = ""
    document_format: Literal["markdown", "html", "plaintext"] = "markdown"
    icon: utils.IconType = None
    group: Optional[str] = None
    parameters: Dict[str, ParameterInfo] = dataclasses.field(default_factory=dict)
    cancelable: bool = False
    executor: Optional[ForwardRef("BaseFunctionExecutor")] = None
