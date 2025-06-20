from pyguiadapter.action import Action, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import Menu
from pyguiadapter.toolbar import ToolBar
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox, filedialog


def on_action_about(window: FnExecuteWindow, _: Action):
    messagebox.show_info_message(
        parent=window,
        message="This is an example of toolbar and menu with custom actions.",
        title="About",
    )


def on_action_close(window: FnExecuteWindow, _: Action):
    ret = messagebox.show_question_message(
        window, "Are you sure you want to quit?", buttons=messagebox.Yes | messagebox.No
    )
    if ret == messagebox.Yes:
        window.close()


def on_action_open(window: FnExecuteWindow, _: Action):
    ret = filedialog.get_open_file(
        window,
        title="Open File",
        start_dir="./",
        filters="JSON files(*.json);;Python files(*.py);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be opened: {ret}")


def on_action_save(window: FnExecuteWindow, _: Action):
    ret = filedialog.get_save_file(
        window,
        title="Save File",
        start_dir="./",
        filters="JSON files(*.json);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be saved: {ret}")


def on_action_auto_theme(window: FnExecuteWindow, _: Action, checked: bool):
    if checked:
        messagebox.show_info_message(window, "Auto theme is selected.")


def on_action_light_theme(window: FnExecuteWindow, _: Action, checked: bool):
    if checked:
        messagebox.show_info_message(window, "Light theme is selected.")


def on_action_dark_theme(window: FnExecuteWindow, _: Action, checked: bool):
    if checked:
        messagebox.show_info_message(window, "Dark theme is selected.")


action_about = Action(
    text="About",
    icon="fa.info-circle",
    on_triggered=on_action_about,
)

action_open = Action(
    text="Open",
    icon="fa.folder-open",
    shortcut="Ctrl+O",
    on_triggered=on_action_open,
)

action_save = Action(
    text="Save",
    icon="fa.save",
    shortcut="Ctrl+S",
    on_triggered=on_action_save,
)

action_close = Action(
    text="Quit",
    icon="fa.close",
    shortcut="Ctrl+Q",
    on_triggered=on_action_close,
)

action_auto_them = Action(
    text="Auto",
    checkable=True,
    checked=True,
    on_toggled=on_action_auto_theme,
)

action_light_theme = Action(
    text="Light",
    checkable=True,
    on_toggled=on_action_light_theme,
)

action_dark_theme = Action(
    text="Dark",
    checkable=True,
    on_toggled=on_action_dark_theme,
)

submenu_theme = Menu(
    title="Theme",
    actions=[action_auto_them, action_light_theme, action_dark_theme],
    exclusive=True,
)
menu_file = Menu(
    title="File",
    actions=[
        action_open,
        action_save,
        Separator(),
        action_close,
        Separator(),
        submenu_theme,
    ],
)
menu_help = Menu(
    title="Help",
    actions=[action_about],
)


def menu_toolbar_example(arg1: int, arg2: str, arg3: bool):
    """
    This example shows how to add and config toolbar and menus to the window.
    @param arg1:
    @param arg2:
    @param arg3:
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        menu_toolbar_example,
        window_toolbar=ToolBar(
            actions=[action_open, action_save, Separator(), action_close]
        ),
        window_menus=[menu_file, menu_help],
    )
    adapter.run()
