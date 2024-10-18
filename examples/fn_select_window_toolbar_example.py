from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.toolbar import ToolBar, ToolButtonTextUnderIcon
from pyguiadapter.utils import messagebox
from pyguiadapter.windows.fnselect import FnSelectWindow


def on_action_test(window: FnSelectWindow, action: Action):
    messagebox.show_info_message(
        window, message=f"Action Triggered!(Action: {action.text})"
    )


def on_action_close(window: FnSelectWindow, _: Action):
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

toolbar = ToolBar(
    actions=[action_test, action_close],
    floatable=True,
    button_style=ToolButtonTextUnderIcon,
)


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run(show_select_window=True, select_window_toolbar=toolbar)
