from enum import Enum
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ulogging import uprint


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
    uprint(day_enums)
    uprint(color_enums)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(enums_example)
    adapter.run()
