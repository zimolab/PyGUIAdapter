from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import color_hex_t
from pyguiadapter.widgets import ColorHexPickerConfig


def color_hex_t_example(
    arg1: color_hex_t,
    arg2: color_hex_t,
    arg3: color_hex_t = "red",
):
    """
    This is an example for type **color_hex_t** type hint and **ColorPicker** widget.

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = "#aaffbb"
    alpha_channel = false
    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = ColorHexPickerConfig(default_value="#effeedff", alpha_channel=True)
    arg3_conf = ColorHexPickerConfig(display_color_name=False)
    adapter = GUIAdapter()
    adapter.add(
        color_hex_t_example, widget_configs={"arg2": arg2_conf, "arg3": arg3_conf}
    )
    adapter.run()
