from datetime import datetime

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import DateTimeEditConfig


def datetime_example(arg1: datetime, arg2: datetime, arg3: datetime):
    """
    example for type **datetime** and DateTimeEdit widget
    """
    uprint("arg1", arg1)
    uprint("arg2", arg2)
    uprint("arg3", arg3)


if __name__ == "__main__":
    arg1_conf = DateTimeEditConfig(
        min_datetime=datetime(2023, 1, 1),
        max_datetime=datetime(2023, 12, 31),
    )
    arg3_conf = DateTimeEditConfig(
        default_value=datetime(2023, 6, 1, 12, 59, 59),
        min_datetime=datetime(2023, 1, 1),
        max_datetime=datetime(2023, 12, 31),
        calendar_popup=True,
    )
    adapter = GUIAdapter()
    adapter.add(
        datetime_example,
        widget_configs={
            "arg1": arg1_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
