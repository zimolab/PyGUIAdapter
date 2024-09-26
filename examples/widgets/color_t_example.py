from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import color_t
from pyguiadapter.widgets import ColorPickerConfig


def color_t_example(arg1: color_t, arg2: color_t, arg3: color_t = "red"):
    """
    example for type **color_t** and **ColorPicker** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = [25, 100, 100]
    alpha_channel = false
    return_type = "tuple"
    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = ColorPickerConfig(default_value="#effeef", return_type="str")
    arg3_conf = ColorPickerConfig(
        default_value="#feeffe", display_color_name=False, return_type="tuple"
    )
    adapter = GUIAdapter()
    adapter.add(
        color_t_example,
        widget_configs={
            "arg2": arg2_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
