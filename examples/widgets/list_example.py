from typing import List

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint


def list_example(arg1: list, arg2: List, arg3: list):
    """
    example for **ListEdit** for **list-like** types

    @params

    [arg1]
    default_value = [1,2,3,4]

    [arg2]
    default_value = ["a", "b", 3, "d"]

    @end
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    arg3_conf = {
        "default_value": [1, 2, 3, [1, 2, 3, 4]],
    }
    adapter = GUIAdapter()
    adapter.add(
        list_example,
        widget_configs={
            "arg3": arg3_conf,
        },
    )
    adapter.run()
