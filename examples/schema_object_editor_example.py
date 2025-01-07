from pyguiadapter.action import Action, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.itemseditor import ObjectEditorConfig
from pyguiadapter.itemseditor.valuetypes import (
    StringValue,
    PasswordEchoOnEditMode,
    BoolValue,
    ChoiceValue,
)
from pyguiadapter.menu import Menu
from pyguiadapter.utils import messagebox, show_schema_object_editor
from pyguiadapter.windows.fnselect import FnSelectWindow


setting_schema = {
    "username": StringValue(
        default_value="admin", display_name="Username", placeholder="Enter Username"
    ),
    "password": StringValue(
        default_value="123456",
        display_name="Password",
        placeholder="Enter Password",
        echo_mode=PasswordEchoOnEditMode,
        clear_button=True,
    ),
    "remember_me": BoolValue(
        default_value=True, display_name="Remember Me", true_text="Yes", false_text="No"
    ),
    "language": ChoiceValue(
        default_value=0,
        choices=["English", "Chinese", "Japanese", "Korean", "French"],
        display_name="Language",
    ),
    "theme": ChoiceValue(
        default_value="light",
        choices=["light", "dark", "system"],
        display_name="Theme",
    ),
    "port": StringValue(
        default_value="8080",
        display_name="Port",
        validator="^[0-9]+$",
        max_length=5,
        placeholder="Enter Port",
    ),
    "host": StringValue(
        default_value="localhost",
        display_name="Host",
        placeholder="Enter Host",
        max_length=100,
    ),
}

settings = {
    "username": "admin",
    "password": "123456",
    "remember_me": True,
    "language": 0,
    "theme": "light",
    "port": "8080",
    "host": "localhost",
}


def on_action_settings(window: FnSelectWindow, action: Action):
    new_settings, ok = show_schema_object_editor(
        window,
        schema=setting_schema,
        obj=settings,
        config=ObjectEditorConfig(
            window_title="Settings", center_container_title="configurations"
        ),
    )
    if not ok:
        return
    settings.update(new_settings)


def on_action_close(window: FnSelectWindow, _: Action):
    ret = messagebox.show_question_message(
        window,
        message="Are you sure to close the application?",
        buttons=messagebox.Yes | messagebox.No,
    )
    if ret == messagebox.Yes:
        window.close()


action_settings = Action(
    text="Configurations",
    icon="msc.settings-gear",
    on_triggered=on_action_settings,
    shortcut="Ctrl+O",
)
action_close = Action(
    text="Close", icon="fa.close", on_triggered=on_action_close, shortcut="Ctrl+Q"
)


menu_file = Menu(
    title="File",
    actions=[action_settings, Separator(), action_close],
)


def foo():
    uprint("current settings:")
    uprint(settings)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run(show_select_window=True, select_window_menus=[menu_file])
