from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.types import int_slider_t
from pyguiadapter.widgets import SliderConfig
from pyguiadapter.widgets.extend.slider import TickPosition


def int_slider_t_example(
    arg1: int_slider_t, arg2: int_slider_t, arg3: int_slider_t = 100
) -> int:
    """
    example for **int_slider_t** and **Slider** widget

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
    tick_interval = 10
    inverted_controls = true
    inverted_appearance = true

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return arg1 + arg2 + arg3


if __name__ == "__main__":

    arg3_conf = SliderConfig(
        # this will override the default_value defined in the function signature
        default_value=-99,
        min_value=-100,
        max_value=100,
        tick_position=TickPosition.TicksAbove,
        tick_interval=2,
        suffix=" mv",
    )

    adapter = GUIAdapter()
    adapter.add(
        int_slider_t_example,
        widget_configs={"arg3": arg3_conf},
    )
    adapter.run()
