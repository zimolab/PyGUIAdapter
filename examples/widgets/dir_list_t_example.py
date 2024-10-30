from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import dir_list_t
from pyguiadapter.widgets import DirectoryListEditConfig, DirectoryListEdit


def dir_list_t_example(arg1: dir_list_t, arg2: dir_list_t, arg3: dir_list_t):
    """
    This is an example for **dir_list_t** type hint and **DirectoryListEdit** widget.

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
    adapter.add(
        dir_list_t_example,
        widget_configs={
            "arg1": DirectoryListEditConfig(
                text_elide_mode=DirectoryListEdit.ElideNone,
                drag_n_drop=True,
            ),
            "arg2": DirectoryListEditConfig(
                text_elide_mode=DirectoryListEdit.ElideRight,
                drag_n_drop=True,
            ),
            "arg3": DirectoryListEditConfig(
                text_elide_mode=DirectoryListEdit.ElideLeft,
                drag_n_drop=True,
            ),
        },
    )
    adapter.run()
