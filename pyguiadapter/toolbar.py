import dataclasses
from typing import Optional, List, Union, Tuple

from qtpy.QtCore import Qt, QSize

from .action import ActionConfig, Separator

ToolBarArea = Qt.ToolBarArea
ToolBarAreas = Union[Qt.ToolBarArea, Qt.ToolBarAreas, int, type(None)]
TopToolBarArea = Qt.TopToolBarArea
BottomToolBarArea = Qt.BottomToolBarArea
LeftToolBarArea = Qt.LeftToolBarArea
RightToolBarArea = Qt.RightToolBarArea
AllToolBarAreas = Qt.AllToolBarAreas

ToolButtonStyle = Qt.ToolButtonStyle
ToolButtonIconOnly = ToolButtonStyle.ToolButtonIconOnly
ToolButtonTextBesideIcon = ToolButtonStyle.ToolButtonTextBesideIcon
ToolButtonTextUnderIcon = ToolButtonStyle.ToolButtonTextUnderIcon
ToolButtonFollowStyle = ToolButtonStyle.ToolButtonFollowStyle
ToolButtonTextOnly = ToolButtonStyle.ToolButtonTextOnly


@dataclasses.dataclass(frozen=True)
class ToolBarConfig(object):
    actions: List[Union[ActionConfig, Separator]]
    moveable: bool = True
    floatable: bool = True
    icon_size: Union[int, Tuple[int, int], QSize, None] = None
    initial_area: Optional[ToolBarArea] = None
    allowed_areas: ToolBarAreas = None
    button_style: Optional[ToolButtonStyle] = None

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