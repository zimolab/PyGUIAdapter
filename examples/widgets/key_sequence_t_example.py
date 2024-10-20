from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import key_sequence_t
from pyguiadapter.widgets import KeySequenceEditConfig, KeySequenceFormat


def key_sequence_t_example(
    arg1: key_sequence_t, arg2: key_sequence_t, arg3: key_sequence_t = "Ctrl+Q"
):
    """
    example for type **key_sequence_t** and **KeySequenceEdit** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = "Ctrl+Shift+V"

    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = KeySequenceEditConfig(default_value="Ctrl+Alt+D")

    arg3_conf = KeySequenceEditConfig(
        default_value="Ctrl+Alt+D", key_sequence_format=KeySequenceFormat.NativeText
    )
    adapter = GUIAdapter()
    adapter.add(
        key_sequence_t_example,
        widget_configs={
            "arg2": arg2_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
