from __future__ import annotations

import dataclasses
from typing import Type, Tuple, Dict, Callable, Any

from .fn import FnInfo
from .paramwidget import BaseParameterWidget, BaseParameterWidgetConfig
from .windows.fnexec import _window


@dataclasses.dataclass
class FnBundle(object):
    fn_info: FnInfo
    window_config: _window.FnExecuteWindowConfig
    widget_configs: Dict[
        str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]
    ]
    on_execute_result: Callable[[Any, Dict[str, Any]], None] | None = None
    on_execute_error: Callable[[Exception, Dict[str, Any]], None] | None = None
