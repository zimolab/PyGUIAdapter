from typing import List

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import ListEditConfig


def list_example(arg1: list, arg2: List, arg3: list):
    """
    This is an example for **ListEdit** and list** types

    Args:
        arg1: description of arg1
        arg2: description of arg2
        arg3: description of arg3

    Returns:
        None

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
    arg3_conf = ListEditConfig(
        default_value=[1, 2, 3, 4, ["a", "b", 3, "d"]],
        # set editor_height or editor_width to 0 will hide the inplace editor
        editor_height=0,
        editor_width=0,
    )
    adapter = GUIAdapter()
    adapter.add(list_example, widget_configs={"arg3": arg3_conf})
    adapter.run()
