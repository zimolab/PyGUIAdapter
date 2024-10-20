"""
@Time    : 2024.10.20
@File    : bundle.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了FnBundle类，用于封装函数信息、参数配置、窗口配置、窗口事件监听器、窗口工具栏、窗口菜单等信息。方便传参。仅限于内部使用。
"""

import dataclasses
from typing import Type, Tuple, Dict, Callable, Any, Optional, List, Union

from .action import Separator
from .menu import Menu
from .toolbar import ToolBar
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
    window_toolbar: Optional[ToolBar]
    window_menus: Optional[List[Union[Menu, Separator]]]
    on_execute_result: Optional[Callable[[Any, Dict[str, Any]], None]] = None
    on_execute_error: Optional[Callable[[Exception, Dict[str, Any]], None]] = None
