from typing import Tuple

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import TupleEditConfig


def tuple_example(arg1: tuple, arg2: Tuple, arg3: tuple):
    """
    example for **TupleEdit** for **tuple-like** types
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    arg1_conf = TupleEditConfig(
        default_value=(1, 2, 3),
    )
    arg2_conf = TupleEditConfig(
        default_value=("a", "b", 1, 2),
    )
    arg3_conf = {
        "default_value": (1, 2, 3, [1, 2, 3, 4]),
    }
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
