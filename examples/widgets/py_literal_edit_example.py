from typing import Any, Union

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import PyLiteralEditConfig


def py_literal_example(arg1: Any, arg2: object, arg3: Union[int, str]):
    """
    This is an example of **PyLiteralEdit** widget and **Any**, **object**, **Union** types

    Args:
        arg1: description of arg1
        arg2: description of arg2
        arg3: description of arg3

    Returns:
        None
    """
    uprint("arg1: ", arg1, f", type={type(arg1)}")
    uprint("arg2: ", arg2, f", type={type(arg2)}")
    uprint("arg3: ", arg3, f", type={type(arg3)}")


if __name__ == "__main__":
    # PyLiteralEdit support the PyLiteralType, which is a Union of:
    # bool, int, float, bytes, str, list, tuple, dict, set and NoneType.

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
        py_literal_example,
        widget_configs={
            "arg1": arg1_config,
            "arg2": arg2_config,
            "arg3": arg3_config,
        },
    )
    adapter.run()
