from datetime import datetime, date, time

from pyguiadapter import GUIAdapter
from pyguiadapter.interact import ulogging


def datetime_edits_demo(dt: datetime, dt_str: str, d: date, t: time):
    """This function demonstrates how to use the date and time edits.

    @widgets
    [dt]
    label = "datetime"
    display_format = "yyyy-MM-dd HH:mm"
    calendar_popup = true
    min_datetime = "2021-11-22 10:10"
    max_datetime = "2024-12-21 10:10"

    [dt_str]
    label = "datetime by string"
    widget_class = "DateTimeEdit"

    [d]
    display_format = "yyyy年MM月dd日"
    calendar_popup = true
    min_date = "2021年11月22日"
    max_date = "2024年12月21日"

    [t]
    display_format = "HH:mm"
    min_time = "8:30"
    max_time = "17:30"


    @end

    """
    ulogging.debug(f"dt: {dt}, dt_str: {dt_str}, d: {d}, t: {t}")
    return dt, dt_str, d, t


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(datetime_edits_demo)
    gui_adapter.run()
