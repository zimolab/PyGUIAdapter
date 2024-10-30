from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import color_tuple_t
from pyguiadapter.widgets import ColorTuplePickerConfig


def color_tuple_t_example(
    arg1: color_tuple_t,
    arg2: color_tuple_t,
    arg3: color_tuple_t = (125, 230, 156),
):
    """
    This is an example for type **color_tuple_t** type hint and **ColorPicker** widget.

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = [255,0, 126]
    alpha_channel = false
    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = ColorTuplePickerConfig(
        default_value=(25, 25, 25, 255), alpha_channel=True
    )
    arg3_conf = ColorTuplePickerConfig(display_color_name=False)
    adapter = GUIAdapter()
    adapter.add(
        color_tuple_t_example, widget_configs={"arg2": arg2_conf, "arg3": arg3_conf}
    )
    adapter.run()
