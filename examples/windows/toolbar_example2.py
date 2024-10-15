from qtpy.QtWidgets import QAction

from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.toolbar import ToolBarConfig
from pyguiadapter.windows.fnselect import FnSelectWindow
from pyguiadapter.utils import messagebox


def on_action_test(window: FnSelectWindow, action: QAction):
    messagebox.show_info_message(
        window, message=f"Action Triggered!(Action: {action.text()})"
    )


action_test = Action(
    text="Test", icon="fa.folder-open", on_triggered=on_action_test, shortcut="Ctrl+O"
)


def foo():
    pass


toolbar_config = ToolBarConfig(
    actions=[action_test],
)

if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run(show_select_window=True, select_window_toolbar=toolbar_config)
