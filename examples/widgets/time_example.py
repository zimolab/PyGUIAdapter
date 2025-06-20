from datetime import time

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import TimeEditConfig, TimeEdit
from pyguiadapter.widgets.basic.datetimeedit import TimeSpec


def time_example(arg1: time, arg2: time, arg3: time):
    """
    This is an example for **TimeEdit** and **datetime.time** type.

    Args:
        arg1: description of arg1
        arg2: description of arg2
        arg3: description of arg3

    Returns:
        None

    @params
    [arg3]
    label = "Argument 3"
    display_format = "HH小时mm分ss秒"

    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg1_conf = TimeEditConfig(
        default_value=time(hour=12, minute=30),
        max_time=time(hour=23, minute=59),
        min_time=time(hour=0, minute=0),
        time_spec=TimeSpec.UTC,
    )
    arg2_conf = TimeEditConfig(
        default_value=time(hour=20, minute=30),
        max_time=time(hour=23, minute=59),
        min_time=time(hour=12, minute=0),
        alignment=TimeEdit.AlignCenter,
    )
    adapter = GUIAdapter()
    adapter.add(time_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf})
    adapter.run()
