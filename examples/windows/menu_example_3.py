from qtpy.QtWidgets import QAction

from pyguiadapter.action import Action, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import MenuConfig
from pyguiadapter.utils import messagebox
from pyguiadapter.windows.fnselect import FnSelectWindow


def on_action_test(window: FnSelectWindow, action: QAction):
    messagebox.show_info_message(
        window, message=f"Action Triggered!(Action: {action.text()})"
    )


def on_action_close(window: FnSelectWindow, action: QAction):
    ret = messagebox.show_question_message(
        window,
        message="Are you sure to close the application?",
        buttons=messagebox.Yes | messagebox.No,
    )
    if ret == messagebox.Yes:
        window.close()


action_test = Action(
    text="Test", icon="fa.folder-open", on_triggered=on_action_test, shortcut="Ctrl+O"
)
action_close = Action(
    text="Close", icon="fa.close", on_triggered=on_action_close, shortcut="Ctrl+Q"
)


menu_file = MenuConfig(
    title="File",
    actions=[action_test, Separator(), action_close],
)


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run(show_select_window=True, select_window_menus=[menu_file])
