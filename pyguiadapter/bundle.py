import dataclasses
from typing import Type, Tuple, Dict, Callable, Any, Optional, List, Union

from .action import Separator
from .menu import MenuConfig
from .toolbar import ToolBarConfig
from .fn import FnInfo
from .paramwidget import BaseParameterWidget, BaseParameterWidgetConfig
from .window import BaseWindowEventListener
from .windows.fnexec import FnExecuteWindowConfig


@dataclasses.dataclass
class FnBundle(object):
    fn_info: FnInfo
    widget_configs: Dict[
        str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]
    ]
    window_config: FnExecuteWindowConfig
    window_listener: Optional[BaseWindowEventListener]
    window_toolbar: Optional[ToolBarConfig]
    window_menus: Optional[List[Union[MenuConfig, Separator]]]
    on_execute_result: Optional[Callable[[Any, Dict[str, Any]], None]] = None
    on_execute_error: Optional[Callable[[Exception, Dict[str, Any]], None]] = None
