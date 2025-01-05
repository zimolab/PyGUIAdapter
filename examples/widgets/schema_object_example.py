from typing import Dict, Any

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import (
    StringValue,
    IntValue,
    ChoiceValue,
    DateTimeValue,
    FileValue,
    SchemaObjectEditorConfig,
    ColorValue,
)
from pyguiadapter.widgets.itemseditor.valuetypes import PasswordEchoOnEditMode


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
                    # "name": "Alice",
                    # "age": 25,
                    # "gender": "female",
                    # "birthday": "2022-01-01T12:00:00Z",
                    # "photo": "",
                    # "favorite_color": "#FFFFFF",
                },
                schema=schema,
                fill_missing_keys=True,
                ignore_unknown_keys=True,
            )
        },
    )
    adapter.run()
