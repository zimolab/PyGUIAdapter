from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import paths_t


def paths_t_example(arg1: paths_t, arg2: paths_t, arg3: paths_t):
    """
    This is an example for **PathsEdit** for **paths_t** types.

    Args:
        arg1: description of arg1.
        arg2: description of arg2.
        arg3: description of arg3.

    Returns:
        None.

    @params
    [arg1]
    default_value = ["/path/to/file1.txt", "/path/to/file2.txt"]


    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(paths_t_example)
    adapter.run()
