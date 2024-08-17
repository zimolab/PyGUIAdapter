from datetime import datetime, date, time

from pyguiadapter.adapter.adapter import GUIAdapter
from pyguiadapter.widgets import LineEdit, LineEditConfig
from pyguiadapter.windows import (
    FnSelectWindowConfig,
    FnExecuteWindowConfig,
    FnExecuteWindow,
)


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
    pass


def f1(arg1: str = "5678"):
    """

    :param arg1:
    :return:

    @params
    [arg1]
    default_value="1234"

    @end
    """
    pass


def f2():
    """
    Function 2
    :return:
    """
    pass


def f3():
    """
    # Function 3
    :return:
    """
    pass


select_window_config = FnSelectWindowConfig(
    title="My ToolBox",
    default_fn_group_name="Main Functions",
    default_fn_group_icon="mdi6.cog-box",
)


def on_win_close(win: FnExecuteWindow) -> bool:
    return True


exec_win_config = FnExecuteWindowConfig(
    on_close=on_win_close,
)

adapter = GUIAdapter(select_window_config=select_window_config)
adapter.add(
    f1,
    window_config=exec_win_config,
    widget_configs={"arg1": LineEditConfig(default_value="abcd")},
)
adapter.add(f2)
adapter.add(f3, group="Other Functions")
adapter.run(always_show_select_window=True)
