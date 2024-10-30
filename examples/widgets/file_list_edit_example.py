from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import path_list_t, file_list_t, dir_list_t


def file_list_edit_example(arg1: path_list_t, arg2: file_list_t, arg3: dir_list_t):
    """
    This is an example for **path_list_t** type hint and **PathListEdit** widget.

    Args:
        arg1: description of arg1
        arg2: description of arg2
        arg3: description of arg3

    Returns:
    """
    uprint(arg1)
    uprint(arg2)
    uprint(arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(file_list_edit_example)
    adapter.run()
