from typing import Set, MutableSet

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import SetEditConfig


def set_example(arg1: set, arg2: Set, arg3: MutableSet):
    """
    This is an example for **SetEdit** for **set** types.

    Args:
        arg1: description of arg1.
        arg2: description of arg2.
        arg3: description of arg3.

    Returns:
        None.
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    arg1_conf = SetEditConfig(
        default_value={1, 2, 3},
    )
    arg2_conf = SetEditConfig(
        default_value={"a", "b", 1, 2},
    )
    arg3_conf = {
        "default_value": {1, 2, 3, (1, 2, 3, 4)},
    }
    adapter = GUIAdapter()
    adapter.add(
        set_example,
        widget_configs={
            "arg1": arg1_conf,
            "arg2": arg2_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
