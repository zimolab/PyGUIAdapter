from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import PlainDictEditConfig
from pyguiadapter.extend_types import plain_dict_t


def plain_dict_t_example(arg1: plain_dict_t, arg2: plain_dict_t, arg3: plain_dict_t):
    """
    example for type **plain_dict_t** and **PlainDictEdit** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg3]
    default_value = {key1=1,key2="value",key3=true,key4=[1,2,3.0]}
    @end

    """
    uprint("arg1:", arg1, "type: ", type(arg1))
    uprint("arg2:", arg2, "type: ", type(arg2))
    uprint("arg3:", arg3, "type: ", type(arg3))


if __name__ == "__main__":
    arg1_conf = PlainDictEditConfig(
        default_value={
            "key1": 1,
            "key2": "value",
            "key3": True,
            "key4": [1, 2, 3.0],
            "key5": None,
            "key6": {"key7": 1},
        }
    )
    arg2_conf = PlainDictEditConfig(
        default_value={
            "Content-Type": "application/json",
            "Authorization": "Bearer token123",
        },
        key_header="Header",
        value_header="Value",
        vertical_header_visible=True,
    )
    adapter = GUIAdapter()
    adapter.add(
        plain_dict_t_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf}
    )
    adapter.run()
