from typing import Dict, Any

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.itemseditor.valuetypes import (
    StringValue,
    IntValue,
    ChoiceValue,
    DateTimeValue,
    FileValue,
    ColorValue,
    PasswordEchoOnEditMode,
)
from pyguiadapter.widgets import SchemaObjectEditorConfig


def schema_object_example(arg1: Dict[str, Any]):
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
        schema_object_example,
        widget_configs={
            "arg1": SchemaObjectEditorConfig(
                default_value={
                    "name": "Alice",
                    "age": 25,
                    "gender": "female",
                    "birthday": "2022-01-01T12:00:00Z",
                    "photo": "",
                    "favorite_color": "#FFFFFF",
                    "address": "123 Main St",  # unknown key will be ignored, if ignore_unknown_keys is False
                },
                schema=schema,
                fill_missing_keys=True,
                ignore_unknown_keys=True,
            )
        },
    )
    adapter.run()
