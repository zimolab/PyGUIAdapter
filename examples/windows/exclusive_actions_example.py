from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QAction

import qdarktheme

from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import Menu
from pyguiadapter.windows.fnselect import FnSelectWindow


def exclusive_action_example():
    pass


def on_app_start(app: QApplication):
    qdarktheme.setup_theme("auto")


def on_action_auto(win: FnSelectWindow, action: QAction):
    if action.isChecked():
        qdarktheme.setup_theme("auto")


def on_action_light(win: FnSelectWindow, action: QAction):
    if action.isChecked():
        qdarktheme.setup_theme("light")


def on_action_dark(win: FnSelectWindow, action: QAction):
    if action.isChecked():
        qdarktheme.setup_theme("dark")


action_auto = Action(
    text="auto",
    on_toggled=on_action_auto,
    checkable=True,
    checked=True,
)

action_light = Action(
    text="light",
    on_toggled=on_action_light,
    checkable=True,
)

action_dark = Action(
    text="dark",
    on_toggled=on_action_dark,
    checkable=True,
)

menu_theme = Menu(
    title="Theme",
    actions=[action_auto, action_light, action_dark],
    exclusive=True,
)

if __name__ == "__main__":
    adapter = GUIAdapter(on_app_start=on_app_start)
    adapter.add(exclusive_action_example)
    adapter.run(show_select_window=True, select_window_menus=[menu_theme])
