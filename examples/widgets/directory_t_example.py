import os.path

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import directory_t, dir_t
from pyguiadapter.widgets import DirSelectConfig


def directory_t_example(arg1: directory_t, arg2: directory_t, arg3: dir_t):
    """
    example for type **directory_t** and **DirSelect** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg3]
    placeholder = "select path"
    dialog_title = "Select Dir"
    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg1_conf = DirSelectConfig(
        placeholder="select save path",
        dialog_title="Select Save Path",
    )
    arg2_conf = DirSelectConfig(
        default_value=os.path.dirname(os.path.abspath(__file__)),
        start_dir=os.path.expanduser("~"),
        clear_button=True,
    )
    adapter = GUIAdapter()
    adapter.add(
        directory_t_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf}
    )
    adapter.run()
