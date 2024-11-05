from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import int_quantity_t, float_quantity_t
from pyguiadapter.widgets import IntQuantityBoxConfig, FloatQuantityBoxConfig


def quantity_t_example(
    arg1: int_quantity_t, arg2: float_quantity_t, arg3: int_quantity_t = None
):
    """
    This is an example about **xxx_quantity_t** type hint and **XXXQuantityBox** widget.

    Args:
        arg1: description of arg1
        arg2: description of arg2
        arg3: description of arg3
    @params
    [arg3]
    units = ["kg", "g", "mg", "µg", "ng", "pg"]
    default_value_description = "use the default value"
    @end
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        quantity_t_example,
        widget_configs={
            "arg1": IntQuantityBoxConfig(
                default_value=(1, "kg"),
                units=["kg", "g", "mg", "µg", "ng", "pg"],
                min_value=0,
                step=1,
            ),
            "arg2": FloatQuantityBoxConfig(
                default_value=(1.0, "m"),
                units=["m", "cm", "mm", "µm", "nm", "pm"],
                min_value=0.0,
                max_value=1000.0,
                decimals=5,
                step=0.00001,
            ),
        },
    )
    adapter.run()
