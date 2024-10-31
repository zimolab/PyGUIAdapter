from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import font_t
from pyguiadapter.widgets import FontSelectConfig, FontSelect


def font_t_example(arg1: font_t, arg2: font_t, arg3: font_t):
    """
    This is an example for **font_t** type hint and **FontSelect** widget.

    Args:
        arg1: description of arg1.
        arg2: description of arg2.
        arg3: description of arg3.
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        font_t_example,
        widget_configs={
            "arg1": FontSelectConfig(
                default_value="Arial",
                font_filters=FontSelect.MonospacedFonts,
            ),
            "arg2": FontSelectConfig(
                font_filters=FontSelect.ProportionalFonts,
            ),
            "arg3": FontSelectConfig(
                font_filters=FontSelect.MonospacedFonts | FontSelect.ProportionalFonts,
            ),
        },
    )
    adapter.run()
