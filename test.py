import threading
import time
from datetime import datetime

from qtpy.QtWidgets import QMessageBox
from pyguiadapter.adapter import ulogging
from pyguiadapter.adapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.adapter.upopup import *
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
    uprint("hello world!")
    ulogging.info("hello world!\nhaha")
    ulogging.debug("hello world!")
    ulogging.warning("hello world!")
    ulogging.critical("hello world!")
    ulogging.fatal("hello world!")
    # show_info_dialog(
    #     "hello world!",
    #     "Hello",
    #     buttons=QMessageBox.Yes | QMessageBox.No,
    #     detailed_text="hello world!",
    #     informative_text="hello world!",
    #     escape_button=QMessageBox.Yes,
    # )
    # show_warning_dialog(
    #     "hello world!",
    #     "Hello",
    #     buttons=QMessageBox.Yes | QMessageBox.No,
    #     detailed_text="hello world!",
    #     informative_text="hello world!",
    #     escape_button=QMessageBox.Yes,
    # )
    # show_critical_dialog(
    #     "hello world!",
    #     "Hello",
    #     buttons=QMessageBox.Yes | QMessageBox.No,
    #     detailed_text="hello world!",
    #     informative_text="hello world!",
    #     escape_button=QMessageBox.Yes,
    # )
    # ret = show_question_dialog(
    #     "hello world!",
    #     "Hello",
    #     detailed_text="hello world!",
    # )
    # uprint(ret)
    with open("./License", "r") as f:
        c = f.read()
    ret = show_text_content(c)
    print(ret)
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
