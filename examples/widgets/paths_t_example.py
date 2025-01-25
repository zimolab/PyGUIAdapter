from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import paths_t
from pyguiadapter.widgets import PathsEditorConfig


def paths_t_example(arg1: paths_t, arg2: paths_t, arg3: paths_t):
    """
    This is an example for **PathsEditor** for **paths_t** types.

    Args:
        arg1: description of arg1.
        arg2: description of arg2.
        arg3: description of arg3.

    Returns:
        None.

    @params
    [arg1]
    default_value = ["/path/to/file1.txt", "/path/to/file2.txt"]

    [arg2]
    add_dir = false

    [arg3]
    add_file = false

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    widget_configs = {"arg1": PathsEditorConfig()}
    adapter = GUIAdapter()
    adapter.add(paths_t_example, widget_configs=widget_configs)
    adapter.run()
