import dataclasses
from typing import Optional, Callable, List, Union, Tuple, ForwardRef

from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QAction

from . import utils

ActionCallback = Callable[[ForwardRef("BaseWindow"), QAction], None]


@dataclasses.dataclass
class ActionConfig(object):
    text: str
    on_triggered: Optional[ActionCallback] = None
    on_toggled: Optional[ActionCallback] = None
    icon: utils.IconType = None
    icon_text: Optional[str] = None
    auto_repeat: bool = False
    enabled: bool = True
    checkable: bool = False
    checked: bool = False
    shortcut: Optional[str] = None
    shortcut_context: Optional[Qt.ShortcutContext] = None
    tooltip: Optional[str] = None
    whats_this: Optional[str] = None
    status_tip: Optional[str] = None
    priority: Optional[QAction.Priority] = None
    menu_role: Optional[QAction.MenuRole] = None


@dataclasses.dataclass(frozen=True)
class Separator(object):
    pass


@dataclasses.dataclass(frozen=True)
class MenuConfig(object):
    title: str
    actions: List[Union[ActionConfig, Separator, "MenuConfig"]]
    separators_collapsible: bool = True
    tear_off_enabled: bool = True

    def remove_action(self, action: Union[str, ActionConfig, Separator, "MenuConfig"]):
        if isinstance(action, str):
            for action_ in self.actions:
                if isinstance(action_, ActionConfig):
                    if action_.text == action:
                        action = action_
                        break
                if isinstance(action_, MenuConfig):
                    if action_.title == action:
                        action = action_
                        break
            if action in self.actions:
                self.actions.remove(action)
            return
        if action in self.actions:
            self.actions.remove(action)
            return


@dataclasses.dataclass(frozen=True)
class ToolbarConfig(object):
    actions: List[Union[ActionConfig, Separator]]
    moveable: bool = True
    floatable: bool = True
    horizontal: bool = True
    icon_size: Union[Tuple[int, int], QSize, None] = None
    initial_area: Optional[Qt.ToolBarArea] = None
    allowed_areas: Optional[Qt.ToolBarAreas] = None
    button_style: Optional[Qt.ToolButtonStyle] = None

    def remove_action(self, action: Union[str, ActionConfig, Separator]):
        if isinstance(action, str):
            for action_ in self.actions:
                if isinstance(action_, ActionConfig):
                    if action_.text == action:
                        action = action_
                        break
            if action in self.actions:
                self.actions.remove(action)
            return
        if action in self.actions:
            self.actions.remove(action)
            return
