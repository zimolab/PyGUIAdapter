"""
@Time    : 2024.10.20
@File    : action.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了动作（`Action`）配置类、分割符（`Separator`）类以及相关常量。
"""

import dataclasses
from typing import Optional, Callable, ForwardRef

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QAction

from .utils import IconType

Priority = QAction.Priority
HighPriority = QAction.HighPriority
NormalPriority = QAction.NormalPriority
LowPriority = QAction.LowPriority

MenuRole = QAction.MenuRole
NoRole = QAction.NoRole
TextHeuristicRole = QAction.TextHeuristicRole
ApplicationSpecificRole = QAction.ApplicationSpecificRole
AboutQtRole = QAction.AboutQtRole
AboutRole = QAction.AboutRole
PreferencesRole = QAction.PreferencesRole
QuitRole = QAction.QuitRole

ShortcutContext = Qt.ShortcutContext
WidgetShortcut = Qt.WidgetShortcut
WidgetWithChildrenShortcut = Qt.WidgetWithChildrenShortcut
WindowShortcut = Qt.WindowShortcut
ApplicationShortcut = Qt.ApplicationShortcut

BaseWindow_ = ForwardRef("BaseWindow")
Action_ = ForwardRef("Action")

ActionTriggeredCallback = Callable[[BaseWindow_, Action_], None]
ActionToggledCallback = Callable[[BaseWindow_, Action_, bool], None]


@dataclasses.dataclass
class Action(object):
    """该类用于创建动作（`Action`），在工具栏（`ToolBar`）中一个`Action`代表一个工具栏按钮，在菜单（`Menu`）中，一个`Action`代表一个菜单项。"""

    text: str
    """动作（`Action`）的描述性文本。"""

    on_triggered: Optional[ActionTriggeredCallback] = None
    """回调函数，在动作（`Action`）被触发时回调。"""

    on_toggled: Optional[ActionToggledCallback] = None
    """回调函数，在动作（`Action`）的`checked`状态发生切换时回调。"""

    icon: IconType = None
    """动作（`Action`）的图标。"""

    icon_text: Optional[str] = None
    """动作（`Action`）的图标文本。"""

    auto_repeat: bool = True
    """此属性表示动作（`Action`）是否可以自动重复。如果设置为`True`，并且系统启用了键盘自动重复功能，那么当用户持续按下键盘快捷键组合时，该动作将自动重复。"""

    enabled: bool = True
    """动作（`Action`）是否处于启用状态。"""

    checkable: bool = False
    """动作（`Action`）是否为**`可选中动作`**。`可选中动作`具有`选中`和`未选中`两种状态，在状态发生切换时，将触发`on_toggled`回调函数。"""

    checked: bool = False
    """动作（`Action`）是否处于`选中`状态。"""

    shortcut: Optional[str] = None
    """动作（`Action`）的快捷键。"""

    shortcut_context: Optional[ShortcutContext] = None
    """动作（`Action`）快捷键的上下文。"""

    tooltip: Optional[str] = None
    """动作（`Action`）的工具提示，工具提示是在用户将鼠标悬停在动作上时显示的额外信息。"""

    whats_this: Optional[str] = None
    """动作（`Action`）的“What’s This?” 帮助文本。"""

    status_tip: Optional[str] = None
    """动作（`Action`）的状态提示文本，状态提示文本将显示在动作所在窗口的状态栏中。"""

    priority: Optional[Priority] = None
    """动作（`Action`）在用户界面的优先级。"""

    menu_role: Optional[MenuRole] = None
    """动作（`Action`）菜单角色（menu role）。在macOS应用程序菜单中，每个动作都有一个角色，该角色指示了动作在菜单中的用途。默认情况下，所有动作
    都具有TextHeuristicRole角色，这意味着动作是根据其文本内容被添加到菜单中的"""


@dataclasses.dataclass(frozen=True)
class Separator(object):
    """代表了一个分割符，开发者可以用其来分割工具栏上和菜单栏上的动作（`Action`）"""

    pass
