import dataclasses
from typing import Type, Tuple, Dict, Callable, Any, Optional

from .fn import FnInfo
from .paramwidget import BaseParameterWidget, BaseParameterWidgetConfig
from .windows.fnexec import FnExecuteWindowConfig


@dataclasses.dataclass
class FnBundle(object):
    fn_info: FnInfo
    window_config: FnExecuteWindowConfig
    widget_configs: Dict[
        str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]
    ]
    on_execute_result: Optional[Callable[[Any, Dict[str, Any]], None]] = None
    on_execute_error: Optional[Callable[[Exception, Dict[str, Any]], None]] = None
