import dataclasses
from typing import Optional, Callable, ForwardRef

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QAction

from .utils import IconType

Priority = QAction.Priority
MenuRole = QAction.MenuRole
ShortcutContext = Qt.ShortcutContext

BaseWindow_ = ForwardRef("BaseWindow")
Action_ = ForwardRef("Action")

ActionTriggeredCallback = Callable[[BaseWindow_, Action_], None]
ActionToggledCallback = Callable[[BaseWindow_, Action_, bool], None]


@dataclasses.dataclass
class Action(object):
    text: str
    on_triggered: Optional[ActionTriggeredCallback] = None
    on_toggled: Optional[ActionToggledCallback] = None
    icon: IconType = None
    icon_text: Optional[str] = None
    auto_repeat: bool = False
    enabled: bool = True
    checkable: bool = False
    checked: bool = False
    shortcut: Optional[str] = None
    shortcut_context: Optional[ShortcutContext] = None
    tooltip: Optional[str] = None
    whats_this: Optional[str] = None
    status_tip: Optional[str] = None
    priority: Optional[Priority] = None
    menu_role: Optional[MenuRole] = None


@dataclasses.dataclass(frozen=True)
class Separator(object):
    pass
