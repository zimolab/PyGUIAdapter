from datetime import date

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import DateEditConfig


def date_example(arg1: date, arg2: date, arg3: date):
    """
    example for type **date** and DateEdit widget
    """
    uprint("arg1", arg1)
    uprint("arg2", arg2)
    uprint("arg3", arg3)


if __name__ == "__main__":
    arg1_conf = DateEditConfig(
        min_date=date(2023, 1, 1),
        max_date=date(2023, 12, 31),
    )
    arg3_conf = DateEditConfig(
        default_value=date(2023, 6, 1),
        min_date=date(2023, 1, 1),
        max_date=date(2023, 12, 31),
        calendar_popup=True,
    )
    adapter = GUIAdapter()
    adapter.add(
        date_example,
        widget_configs={
            "arg1": arg1_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
