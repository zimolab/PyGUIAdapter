from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import file_list_t


def file_list_edit_example(arg1: file_list_t, arg2: file_list_t):
    """
    This is an example for **file_list_t** type hint and **FileListEdit** widget.

    Args:
        arg1: description of arg1
        arg2: description of arg2

    Returns:
    """
    uprint(arg1)
    uprint(arg2)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(file_list_edit_example)
    adapter.run()
