import json

from qtpy.QtWidgets import QAction

from pyguiadapter.action import ActionConfig, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.toolbar import (
    ToolBarConfig,
    RightToolBarArea,
    LeftToolBarArea,
    ToolButtonTextUnderIcon,
    TopToolBarArea,
)
from pyguiadapter.utils import filedialog, inputdialog, messagebox
from pyguiadapter.window import SimpleWindowEventListener
from pyguiadapter.windows.fnexec import FnExecuteWindow


def toolbar_example():
    pass


###################Action Callbacks#########################
def on_action_open(window: FnExecuteWindow, action: QAction):
    print("on_action_open()")
    ret = filedialog.get_open_file(
        parent=window,
        title="Open File",
        start_dir="./",
        filters="JSON files(*.json);;All files(*.*)",
    )
    if ret:
        messagebox.show_info_message(window, f"File will be opened: {ret}")


def on_action_save(window: FnExecuteWindow, action: QAction):
    print("on_action_save()")
    ret = filedialog.get_save_file(
        parent=window,
        title="Save File",
        start_dir="./",
        filters="JSON files(*.json);;All files(*.*)",
    )
    if ret:
        messagebox.show_info_message(window, f"File will be saved to: {ret}")


def on_action_settings(window: FnExecuteWindow, action: QAction):
    default_settings = {
        "opt1": 1,
        "opt2": "2",
        "opt3": True,
    }
    new_settings = inputdialog.input_json_object(
        parent=window,
        title="Settings",
        icon="fa.cog",
        size=(600, 400),
        ok_button_text="Save",
        cancel_button_text="Cancel",
        initial_text=json.dumps(default_settings, indent=4, ensure_ascii=False),
        auto_indent=True,
        indent_size=4,
        auto_parentheses=True,
        line_wrap_mode=inputdialog.LineWrapMode.WidgetWidth,
        line_wrap_width=88,
    )
    if isinstance(new_settings, dict):
        messagebox.show_info_message(window, f"new settings: {new_settings}")


def on_action_confirm_quit(window: FnExecuteWindow, action: QAction):
    print("on_action_confirm_close(): ", action.isChecked())


def on_action_close(window: FnExecuteWindow, action: QAction):
    print("on_action_close()")
    window.close()


###################~Action Callbacks#########################


if __name__ == "__main__":
    ###################Actions#############################
    action_open = ActionConfig(
        text="Open",
        icon="fa.folder-open",
        on_triggered=on_action_open,
        shortcut="Ctrl+O",
    )
    action_save = ActionConfig(
        text="Save",
        icon="fa.save",
        on_triggered=on_action_save,
        shortcut="Ctrl+S",
    )

    action_settings = ActionConfig(
        text="Settings",
        icon="fa.cog",
        on_triggered=on_action_settings,
        shortcut="Ctrl+,",
    )

    action_quit = ActionConfig(
        text="Quit",
        icon="fa.power-off",
        on_triggered=on_action_close,
        shortcut="Ctrl+Q",
    )
    action_confirm_quit = ActionConfig(
        text="Confirm Quit",
        icon="fa.question-circle",
        checkable=True,
        checked=False,
        on_toggled=on_action_confirm_quit,
    )
    ###################~Actions#############################

    ####################ToolBar#############################
    toolbar = ToolBarConfig(
        actions=[
            action_open,
            action_save,
            action_settings,
            Separator(),
            action_confirm_quit,
            action_quit,
        ],
        moveable=True,
        floatable=True,
        initial_area=RightToolBarArea,
        allowed_areas=RightToolBarArea | LeftToolBarArea | TopToolBarArea,
        button_style=ToolButtonTextUnderIcon,
    )
    ###################~ToolBar#############################

    ################Window Event Listener###################
    def on_window_create(window: FnExecuteWindow):
        print("on_window_create()")
        # make action_confirm_quit checked after the select window is created
        window.set_action_state(action_confirm_quit, True)

    def on_window_close(window: FnExecuteWindow) -> bool:
        # get the state of action_confirm_quit
        # if it is checked, show a question message box to ask if the user really wants to close the window
        # if it is not checked, return True to close the window directly.
        state = window.query_action_state(action_confirm_quit)
        if state:
            # access the
            ret = messagebox.show_question_message(
                window,
                message="Do you really want to close the window?",
                title="Quit",
                buttons=messagebox.Yes | messagebox.No,
            )
            return ret == messagebox.Yes
        return True

    window_listener = SimpleWindowEventListener(
        on_create=on_window_create, on_close=on_window_close
    )
    #################Window Event Listener##################

    adapter = GUIAdapter()
    adapter.add(
        toolbar_example, window_toolbar=toolbar, window_listener=window_listener
    )
    adapter.run()
