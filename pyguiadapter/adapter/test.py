import threading
from datetime import datetime

import time

from pyguiadapter.adapter.adapter import GUIAdapter
from pyguiadapter.windows import (
    FnSelectWindowConfig,
    FnExecuteWindowConfig,
    FnExecuteWindow,
)


def f1(arg1: str, arg2: str):
    """

    :param arg1:
    :return:

    @params
    [arg1]
    default_value="1234"

    @end
    """
    return f"{arg1} + {arg2}"


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
    print("thread", threading.current_thread())
    time.sleep(10)
    return datetime.now()


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
)
adapter.add(f2)
adapter.add(f3, group="Other Functions")
adapter.run()
