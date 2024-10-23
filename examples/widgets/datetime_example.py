from datetime import datetime

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import DateTimeEditConfig, DateTimeEdit


def datetime_example(arg1: datetime, arg2: datetime, arg3: datetime):
    """
    This an example for **DateTimeEdit** widget and **datetime** type.

    Args:
        arg1: description of arg1.
        arg2: description of arg2.
        arg3: description of arg3.

    Returns:
        None.

    @params
    [arg2]
    label = "Argument 2"
    display_format = "dd.MM.yyyy HH:mm:ss"
    @end

    """
    uprint("arg1", arg1)
    uprint("arg2", arg2)
    uprint("arg3", arg3)


if __name__ == "__main__":
    arg1_conf = DateTimeEditConfig(
        min_datetime=datetime(2023, 1, 1),
        max_datetime=datetime(2023, 12, 31),
        time_spec=DateTimeEdit.UTC,
    )
    arg3_conf = DateTimeEditConfig(
        default_value=datetime(2023, 6, 1, 12, 59, 59),
        min_datetime=datetime(2023, 1, 1),
        max_datetime=datetime(2023, 12, 31),
        alignment=DateTimeEdit.AlignCenter,
        calendar_popup=False,
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
