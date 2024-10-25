from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import JsonEditConfig
from pyguiadapter.extend_types import json_obj_t


def json_obj_t_example(arg1: json_obj_t, arg2: json_obj_t, arg3: json_obj_t):
    """
    This is an example for type **json_obj_t** type hint and **JsonEdit** widget.

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg3]
    default_value = true

    @end

    """
    uprint("arg1:", arg1, "type: ", type(arg1))
    uprint("arg2:", arg2, "type: ", type(arg2))
    uprint("arg3:", arg3, "type: ", type(arg3))


if __name__ == "__main__":
    arg1_conf = JsonEditConfig(default_value=[1, 2, 3, "a", "b", {"a": 1, "b": 2}])
    arg2_conf = JsonEditConfig(
        default_value={"a": 1, "b": 2},
        # height=0 or width=0 will make the inplace editor hidden.
        height=0,
        width=0,
    )
    adapter = GUIAdapter()
    adapter.add(
        json_obj_t_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf}
    )
    adapter.run()
