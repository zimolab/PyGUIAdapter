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


# if __name__ == "__main__":
#     app = QApplication([])
#     m = {
#         "File": {
#             "New": ActionItem("New", lambda: print("New"), shortcut="Ctrl+N"),
#             "Open": ActionItem("Open", lambda: print("Open")),
#             "Save": ActionItem("Save", lambda: print("Save")),
#             "Save As": ActionItem("Save As", lambda: print("Save As")),
#             "Close": ActionItem("Close", lambda: print("Close")),
#             "Exit": ActionItem("Exit", lambda: print("Exit")),
#             "sep_1": Separator,
#             "About": {
#                 "About": ActionItem("About", lambda: print("About")),
#                 "Help": ActionItem("Help", lambda: print("Help")),
#                 "sep_1": Separator,
#                 "License": ActionItem("License", lambda: print("License")),
#                 "Version": ActionItem("Version", lambda: print("Version")),
#             },
#         },
#         "Edit": {
#             "Undo": ActionItem("Undo", lambda: print("Undo")),
#         },
#     }
#     window = QMainWindow()
#     window.setMenuBar(QMenuBar())
#     ms = create_menus(m, window)
#     for menu_name, menu in ms.items():
#         window.menuBar().addMenu(menu)
#     window.show()
#     app.exec()
