from typing import Tuple

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import TupleEditConfig


def tuple_example(arg1: tuple, arg2: Tuple, arg3: tuple):
    """
    This is an example for **TupleEdit** and **tuple** types

    Args:
        arg1: describes of arg1
        arg2: describes of arg2
        arg3: describes of arg3

    Returns:
        None
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    arg1_conf = TupleEditConfig(
        default_value=(1, 2, 3),
    )
    arg2_conf = {
        "default_value": (1, 2, 3, [1, 2, 3, 4]),
    }
    arg3_conf = TupleEditConfig(
        default_value=(1, 2, 3),
        label="Arg3",
        # set editor_height or editor_width to 0 will hide the inplace editor
        editor_height=0,
        editor_width=0,
    )
    adapter = GUIAdapter()
    adapter.add(
        tuple_example,
        widget_configs={
            "arg1": arg1_conf,
            "arg2": arg2_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
