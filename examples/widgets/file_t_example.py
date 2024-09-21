import os.path

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import FileSelectConfig
from pyguiadapter.types import file_t


def file_t_example(arg1: file_t, arg2: file_t, arg3: file_t):
    """
    example for type **file_t** and **FileSelect** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg3]
    placeholder = "input save path here"
    save_file = true
    dialog_title = "Save File"
    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg1_conf = FileSelectConfig(
        placeholder="input file path here",
        filters="Text files(*.txt);;All files(*.*)",
        dialog_title="Open File",
    )
    arg2_conf = FileSelectConfig(
        default_value=os.path.abspath(__file__),
        start_dir=os.path.expanduser("~"),
        clear_button=True,
    )
    adapter = GUIAdapter()
    adapter.add(file_t_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf})
    adapter.run()
