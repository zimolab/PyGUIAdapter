from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.types import float_t
from pyguiadapter.widgets import FloatLineEditConfig


def float_t_example(arg1: float_t, arg2: float_t, arg3: float_t = 100) -> float:
    """
    example for **float_t** and **IntLineEdit**

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3
    @return:

    @params
    [arg1]
    default_value = -100.0
    min_value = -100.0
    max_value = 100.0

    [arg2]
    default_value = 99999999.0
    max_value = 99999999.0
    empty_value = -1.0
    decimals = 3
    scientific_notation = true

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return arg1 + arg2 + arg3


if __name__ == "__main__":

    arg3_conf = FloatLineEditConfig(
        # this will override the default_value defined in the function signature
        default_value=-0.00005,
        min_value=-100.0,
        max_value=100.0,
        empty_value=-1,
        decimals=5,
        scientific_notation=True,
    )

    adapter = GUIAdapter()
    adapter.add(
        float_t_example,
        widget_configs={"arg3": arg3_conf},
    )
    adapter.run()
