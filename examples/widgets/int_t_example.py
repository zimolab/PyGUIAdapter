from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import int_t
from pyguiadapter.widgets import IntLineEditConfig


def int_t_example(arg1: int_t, arg2: int_t, arg3: int_t = 100) -> int:
    """
    This is an example for **int_t** type hint and **IntLineEdit** widget.

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3
    @return:

    @params
    [arg1]
    default_value = -100
    min_value = -100
    max_value = 100

    [arg2]
    max_value = 999
    empty_value = -1

    @end
    """
    assert isinstance(arg1, int)
    assert isinstance(arg2, int)
    assert isinstance(arg3, int)
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return arg1 + arg2 + arg3


if __name__ == "__main__":

    arg3_conf = IntLineEditConfig(
        default_value=-99,
        min_value=-100,
        max_value=100,
        empty_value=None,
        placeholder="Enter a number",
        clear_button=True,
    )

    adapter = GUIAdapter()
    adapter.add(
        int_t_example,
        widget_configs={"arg3": arg3_conf},
    )
    adapter.run()
