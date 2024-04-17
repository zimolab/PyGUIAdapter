import dataclasses
from typing import Optional, Callable, Dict

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenu


@dataclasses.dataclass
class ActionItem(object):
    text: str
    callback: Callable
    shortcut: Optional[str] = None
    icon: Optional[str] = None


Separator = object()


def create_action(action_item: ActionItem) -> QAction:
    action = QAction(action_item.text)
    # noinspection PyUnresolvedReferences
    action.triggered.connect(action_item.callback)
    if action_item.shortcut:
        action.setShortcut(action_item.shortcut)
    if action_item.icon:
        action.setIcon(QIcon(action_item.icon))
    return action


def create_menu_items(
    items: Dict,
    parent_menu: QMenu,
    action_creator: Callable[[ActionItem], QAction] = create_action,
):
    for name, item in items.items():
        if isinstance(item, ActionItem):
            action = action_creator(item)
            action.setParent(parent_menu)
            parent_menu.addAction(action)
        elif isinstance(item, dict):
            sub_menu = QMenu(name)
            sub_menu.setParent(parent_menu)
            create_menu_items(item, parent_menu=sub_menu)
            parent_menu.addMenu(sub_menu)
        elif item is Separator:
            parent_menu.addSeparator()
        else:
            raise ValueError("invalid menu item type")
