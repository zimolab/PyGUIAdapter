from typing import Dict, Any, List

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import SchemaObjectsEditorConfig
from pyguiadapter.itemseditor.valuetypes import (
    StringValue,
    IntValue,
    ChoiceValue,
    DateTimeValue,
    FileValue,
    ColorValue,
    PasswordEchoOnEditMode,
)


def schema_objects_example(arg1: List[Dict[str, Any]]):
    uprint("schema_object_example")
    uprint("arg1:", arg1)


if __name__ == "__main__":

    schema = {
        "name": StringValue(),
        "age": IntValue(default_value=1, max_value=120, min_value=1),
        "gender": ChoiceValue("male", choices=["male", "female", "other"]),
        "birthday": DateTimeValue(),
        "photo": FileValue(
            file_filters="JPG Files (*.jpg);;PNG Files (*.png);;All Files (*)"
        ),
        "favorite_color": ColorValue(),
        "password": StringValue(password_symbol="*", echo_mode=PasswordEchoOnEditMode),
    }

    adapter = GUIAdapter()
    adapter.add(
        schema_objects_example,
        widget_configs={
            "arg1": SchemaObjectsEditorConfig(
                default_value=[{"name": "Alice", "age": 25, "gender": "female"}],
                schema=schema,
                fill_missing_keys=True,
                ignore_unknown_keys=True,
            )
        },
    )
    adapter.run()
