import time
from typing import Any

from pyguiadapter.adapter import ulogging
from pyguiadapter.adapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint, is_function_cancelled
from pyguiadapter.adapter.uinput import *
from pyguiadapter.types import text_t, int_t, float_t, directory_t, file_t, file_list_t
from pyguiadapter.windows import FnSelectWindowConfig, FnExecuteWindowConfig


def f1(
    arg1: str,
    arg2: text_t,
    arg3: int,
    arg4: int_t,
    arg5: float,
    arg6: float_t,
    arg7: directory_t,
    arg8: file_t,
    arg9: file_list_t,
    arg10: Any,
):
    """

    :param arg1:
    :return:

    @params
    [arg1]


    @end
    """
    uprint("hello world!")
    ulogging.info("hello world!\nhaha")
    ulogging.debug("hello world!")
    ulogging.warning("hello world!")
    ulogging.critical("hello world!")
    ulogging.fatal("hello world!")
    # show_text_file("./License", title="View License")
    # return f"{arg1} + {arg2}"
    # c = utils.read_text_file("./License")
    # uprint(c)
    uprint(arg9)


def f2():
    """
    Function 2
    :return:
    """
    i = 0
    while True:
        uprint("No: ", i)
        i += 1
        time.sleep(1)
        if is_function_cancelled():
            break
    uprint("f2 finished: ", i)


def f3(a: str, b: str):
    """
    # Function 3
    :return:

    @params
    [b]
    group="Misc"
    @end

    """
    # text = get_text(label="Input some text")
    # uprint(text)
    # i = get_int(label="Input some int", min_value=0, max_value=100)
    # uprint(i)
    # f = get_float(label="Input some float", min_value=0, max_value=100)
    # uprint(f)
    # it = get_selected_item(["a", "b", "c"], current=1, editable=True)
    # uprint(it)
    # color = get_color()
    # uprint(color)
    # color = get_color(show_alpha_channel=False)
    # uprint(color)
    # color = get_color_name()
    # uprint(color)
    # color = get_color_rgb()
    # uprint(color)
    # color = get_color_rgba()
    # uprint(color)

    # if a == "e":
    #     raise ParameterValidationError(
    #         parameter_name="b", message=f"invalid argument: {a}"
    #     )
    # return f"{a}"
    dir_ = get_existing_directory()
    uprint(dir_)
    url = get_existing_directory_url()
    uprint(url)
    filename = get_open_file()
    uprint(filename)
    files = get_open_files()
    uprint(files)
    save_file = get_save_file()
    uprint(save_file)


select_window_config = FnSelectWindowConfig(
    title="My ToolBox",
    default_fn_group_name="Main Functions",
    default_fn_group_icon="mdi6.cog-box",
    always_show_select_window=False,
)


def on_win_close(win: FnExecuteWindow) -> bool:
    return True


exec_win_config = FnExecuteWindowConfig(
    on_close=on_win_close,
)

adapter = GUIAdapter(select_window_config=select_window_config)
adapter.add(f1, window_config=exec_win_config)
adapter.add(f2, cancelable=True)
adapter.add(f3, group="Other Functions")
adapter.run()
