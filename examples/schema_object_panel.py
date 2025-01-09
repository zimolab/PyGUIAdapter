from typing import Any, Dict

from qtpy.QtWidgets import QWidget

from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.itemseditor.valuetypes import (
    StringValue,
    IntValue,
    ChoiceValue,
    PasswordEchoOnEditMode,
    FloatValue,
    BoolValue,
    FileValue,
)
from pyguiadapter.toolbar import ToolBar
from pyguiadapter.utils import (
    messagebox,
    show_schema_object_panel,
    SchemaObjectPanelConfig,
)
from pyguiadapter.windows.fnexec import FnExecuteWindow

student_profile_schema = {
    "name": StringValue(default_value="Undefined", display_name="Name"),
    "age": IntValue(default_value=16, display_name="Age", min_value=16, max_value=20),
    "grade": ChoiceValue(
        default_value="A",
        choices=["A", "B", "C", "D", "E"],
    ),
    "password": StringValue(
        default_value="Admin123",
        display_name="ID Password",
        echo_mode=PasswordEchoOnEditMode,
        clear_button=True,
        password_symbol="*",
        max_password_symbols=10,
    ),
    "scores": FloatValue(
        default_value=0.0,
        display_name="Average Scores",
        min_value=0.0,
        max_value=100.0,
        step=0.5,
        suffix=" (avg)",
        display_affix=True,
    ),
    "is_active": BoolValue(
        default_value=True, display_name="Active", true_text="Yes", false_text="No"
    ),
    "photo": FileValue(
        default_value="Not Provided",
        display_name="Photo",
        title="Select a photo",
        file_filters="JPG Files (*.jpg);;PNG Files (*.png);;All Files (*.*)",
    ),
}

student_profile = {
    "name": "John Doe",
    "age": 18,
    "grade": "B",
    "password": "MyPassword123",
    "scores": 99.5,
    "is_active": True,
    "photo": "/path/to/john_doe.jpg",
}


def _accept_hook(editor: QWidget, obj: Dict[str, Any]) -> bool:
    password = obj.get("password")
    if len(password) < 6:
        messagebox.show_warning_message(
            editor,
            message="Password should be at least 6 characters long.",
            title="Warning",
        )
        return False
    return True


def on_action_schema_object_panel(window: FnExecuteWindow, action: Action):
    _ = action  # unused
    new_settings, ok = show_schema_object_panel(
        window,
        schema=student_profile_schema,
        obj=student_profile,
        config=SchemaObjectPanelConfig(
            title="Student Profile",
            center_container_title="Personal Information",
            icon="ei.adult",
        ),
        accept_hook=_accept_hook,
    )
    if not ok:
        return
    student_profile.update(new_settings)


action_profile = Action(
    text="Profile",
    icon="ei.adult",
    on_triggered=on_action_schema_object_panel,
    shortcut="Ctrl+O",
)

toolbar = ToolBar(actions=[action_profile], moveable=False, floatable=False)


def foo():
    uprint("current profile:")
    uprint(student_profile)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo, window_toolbar=toolbar)
    adapter.run()
