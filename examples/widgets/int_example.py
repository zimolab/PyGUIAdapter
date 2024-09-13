from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ulogging import uprint


def int_example(int_arg1: int, int_arg2: int, int_arg3: int = 100) -> int:
    """
    example for **int** and **IntSpinBox**
    @param int_arg1: min_value=-100, max_value=100, step=2
    @param int_arg2: max_value = 999, prefix="$"
    @param int_arg3: suffix = "(hex)", display_integer_base=16
    @return:

    @params
    [int_arg1]
    default_value = -100
    min_value = -100
    max_value = 100

    [int_arg2]
    max_value = 999
    prefix = "$"

    @end

    """
    uprint("int_arg1:", int_arg1)
    uprint("int_arg2:", int_arg2)
    uprint("int_arg3:", int_arg3)
    return int_arg1 + int_arg2 + int_arg3


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        int_example,
        widget_configs={
            "int_arg3": {
                "suffix": "(hex)",
                "display_integer_base": 16,
            }
        },
    )
    adapter.run()
