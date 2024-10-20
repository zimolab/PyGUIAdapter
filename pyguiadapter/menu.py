"""
@Time    : 2024.10.20
@File    : menu.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义菜单配置类
"""

import dataclasses
from typing import List, Union

from .action import Action, Separator


@dataclasses.dataclass(frozen=True)
class Menu(object):
    """该类用于配置窗口菜单栏上的菜单。"""

    title: str
    """菜单的标题。"""

    actions: List[Union[Action, Separator, "Menu"]]
    """菜单下的菜单项（`Action`）、分隔符（`Separator`）或子菜单（`Menu`）"""

    separators_collapsible: bool = True
    """是否将连续的分隔符合并。为`True`时连续分隔符将被合并为一个，同时，位于菜单开头或结尾的分隔符也会被隐藏。"""

    tear_off_enabled: bool = True
    """菜单可以被“撕下”。为`True`时，菜单将包含一个特殊的“撕下”项（通常显示为菜单顶部的虚线），当触发它时，会创建一个菜单的副本。这个“撕下”的副本
    会存在于一个单独的窗口中，并且包含与原始菜单相同的菜单项。"""

    exclusive: bool = False
    """是否将菜单下的菜单项（`Action`）添加到一个互斥组中。只有当前菜单下`checkable`属性为`True`的菜单项（`Action`）才会被添加的互斥组中。"""

    def remove_action(self, action: Union[str, Action, Separator, "Menu"]):
        if isinstance(action, str):
            for action_ in self.actions:
                if isinstance(action_, Action):
                    if action_.text == action:
                        action = action_
                        break
                if isinstance(action_, Menu):
                    if action_.title == action:
                        action = action_
                        break
            if action in self.actions:
                self.actions.remove(action)
            return
        if action in self.actions:
            self.actions.remove(action)
            return
