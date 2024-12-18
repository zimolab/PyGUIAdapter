from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import int_dial_t
from pyguiadapter.widgets import DialConfig


def int_dial_t_example(
    arg1: int_dial_t, arg2: int_dial_t, arg3: int_dial_t = 100
) -> int:
    """
    This is an example for **int_dial_t** type hint and **Dial** widget.

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
    single_step = 2
    tracking = false
    prefix = "count: "
    inverted_controls = true
    inverted_appearance = true

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return arg1 + arg2 + arg3


if __name__ == "__main__":

    arg3_conf = DialConfig(
        default_value=-99,
        min_value=-100,
        max_value=100,
        suffix=" mv",
    )

    adapter = GUIAdapter()
    adapter.add(int_dial_t_example, widget_configs={"arg3": arg3_conf})
    adapter.run()
