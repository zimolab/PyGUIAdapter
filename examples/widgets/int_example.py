from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import IntSpinBoxConfig


def int_example(arg1: int, arg2: int, arg3: int = 100) -> int:
    """
    A simple example for **int** and **IntSpinBox**

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @return:

    @params
    # parameter widget config for arg1
    [arg1]
    default_value = -100
    min_value = -100
    max_value = 100

    # parameter widget config for arg2
    [arg2]
    default_value = 1000
    max_value = 999
    prefix = "$"

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return arg1 + arg2 + arg3


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        int_example,
        widget_configs={
            # parameter config for arg3
            "arg3": IntSpinBoxConfig(
                default_value=100, min_value=0, max_value=1000, step=10, prefix="$"
            )
        },
    )
    adapter.run()
