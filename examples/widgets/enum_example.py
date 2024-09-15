from enum import Enum
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ulogging import uprint
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
    example for type **enum** and **EnumSelect**
    @param day_enums: Enums for week days
    @param color_enums:  Enums for RGB colors
    @return:

    @params
    [day_enums]
    # this will override the default value defined in the function signature
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
            "RED": ("mdi.invert-colors", {"color": "red"}),
            "GREEN": ("mdi.invert-colors", {"color": "green"}),
            "BLUE": ("mdi.invert-colors", {"color": "blue"}),
        },
        icon_size=(24, 24),
    )
    adapter = GUIAdapter()
    adapter.add(enums_example, widget_configs={"color_enums": color_enums_conf})
    adapter.run()
