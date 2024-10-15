import dataclasses
from typing import Optional, List, Union, Tuple

from qtpy.QtCore import Qt, QSize

from .action import Action, Separator

ToolBarArea = Qt.ToolBarArea
TopToolBarArea = ToolBarArea.TopToolBarArea
BottomToolBarArea = ToolBarArea.BottomToolBarArea
LeftToolBarArea = ToolBarArea.LeftToolBarArea
RightToolBarArea = ToolBarArea.RightToolBarArea

ToolBarAreas = Union[ToolBarArea, int]
AllToolBarAreas = Qt.AllToolBarAreas

ToolButtonStyle = Qt.ToolButtonStyle
ToolButtonIconOnly = ToolButtonStyle.ToolButtonIconOnly
ToolButtonTextBesideIcon = ToolButtonStyle.ToolButtonTextBesideIcon
ToolButtonTextUnderIcon = ToolButtonStyle.ToolButtonTextUnderIcon
ToolButtonFollowStyle = ToolButtonStyle.ToolButtonFollowStyle
ToolButtonTextOnly = ToolButtonStyle.ToolButtonTextOnly


@dataclasses.dataclass(frozen=True)
class ToolBar(object):
    actions: List[Union[Action, Separator]]
    """要添加到工具栏中的动作（`Action`）或分隔符（`Separator`）列表。在工具栏中，动作`Action`以工具栏按钮的形式出现。"""

    moveable: bool = True
    """工具栏是否可以移动。"""

    floatable: bool = True
    """工具栏是否可以漂浮在主窗口之外。"""

    icon_size: Union[int, Tuple[int, int], QSize, None] = None
    """工具栏按钮的图标大小，"""

    initial_area: Optional[ToolBarArea] = None
    """工具栏在窗口上的初始位置。"""

    allowed_areas: Optional[ToolBarAreas] = None
    """窗口上允许工具栏停靠的位置。"""

    button_style: Optional[ToolButtonStyle] = None
    """工具栏按的样式。"""

    def remove_action(self, action: Union[str, Action, Separator]):
        if isinstance(action, str):
            for action_ in self.actions:
                if isinstance(action_, Action):
                    if action_.text == action:
                        action = action_
                        break
            if action in self.actions:
                self.actions.remove(action)
            return
        if action in self.actions:
            self.actions.remove(action)
            return
