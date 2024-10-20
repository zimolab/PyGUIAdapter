import os.path

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import MultiFileSelectConfig
from pyguiadapter.extend_types import files_t


def files_t_example(arg1: files_t, arg2: files_t, arg3: files_t):
    """
    example for type **files_t** and **MultiFileSelect** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg3]
    placeholder = "select files"
    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg1_conf = MultiFileSelectConfig(
        default_value=("a", "b"),
        placeholder="input files here",
        filters="Text files(*.txt);;All files(*.*)",
        dialog_title="Open Files",
    )
    arg2_conf = MultiFileSelectConfig(
        default_value=[os.path.abspath(__file__)],
        start_dir=os.path.expanduser("~"),
        clear_button=True,
    )
    adapter = GUIAdapter()
    adapter.add(files_t_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf})
    adapter.run()
