from enum import Enum
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.utils import qta_icon
from pyguiadapter.widgets import EnumSelectConfig


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def enums_example(day_enums: Weekday, color_enums: Color = Color.GREEN):
    """
    This is an example for type **enum** and **EnumSelect** widget.

    @param day_enums: Enums for week days
    @param color_enums:  Enums for RGB colors
    @return:

    @params
    [day_enums]
    default_value = "MONDAY"
    icons = {"MONDAY"="mdi6.numeric-1-circle", "TUESDAY"="mdi6.numeric-2-circle"}

    @end

    """
    uprint(day_enums)
    uprint(color_enums)


if __name__ == "__main__":
    color_enums_conf = EnumSelectConfig(
        # this will override the default value defined in the function signature
        default_value=Color.BLUE,
        icons={
            # you can use the Enum value as the key to its icon
            "RED": qta_icon("mdi.invert-colors", color="red"),
            "GREEN": qta_icon("mdi.invert-colors", color="green"),
            "BLUE": qta_icon("mdi.invert-colors", color="blue"),
            # or you can use the Enum value itself as the key to its icon
            # Color.RED: qta_icon("mdi.invert-colors", color="red"),
            # Color.GREEN: qta_icon("mdi.invert-colors", color="green"),
            # Color.BLUE: qta_icon("mdi.invert-colors", color="blue"),
        },
        icon_size=(24, 24),
    )
    adapter = GUIAdapter()
    adapter.add(enums_example, widget_configs={"color_enums": color_enums_conf})
    adapter.run()
