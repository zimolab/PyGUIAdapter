from typing import Any, Union

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import PyLiteralEditConfig


def any_example(arg1: Any, arg2: object, arg3: Union[int, str]):
    """
    example of **PyLiteralEdit** for **Any**, **object**, **Union** types
    """
    uprint("arg1: ", arg1, f", type={type(arg1)}")
    uprint("arg2: ", arg2, f", type={type(arg2)}")
    uprint("arg3: ", arg3, f", type={type(arg3)}")


if __name__ == "__main__":
    # PyLiteralEdit support the PyLiteralType, which is a Union of:
    # bool, int, float, bytes, str, list, tuple, dict, set

    arg1_config = PyLiteralEditConfig(
        default_value=[1, 2, 3, 4],
    )
    arg2_config = PyLiteralEditConfig(
        default_value=("a", "b", "c", "d"),
    )
    arg3_config = PyLiteralEditConfig(
        default_value={1, 2, 3},
    )
    adapter = GUIAdapter()
    adapter.add(
        any_example,
        widget_configs={
            "arg1": arg1_config,
            "arg2": arg2_config,
            "arg3": arg3_config,
        },
    )
    adapter.run()
