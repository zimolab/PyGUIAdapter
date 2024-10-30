from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import path_list_t
from pyguiadapter.widgets import PathListEdit, PathListEditConfig


def path_list_t_example(arg1: path_list_t, arg2: path_list_t, arg3: path_list_t):
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
    adapter.add(
        path_list_t_example,
        widget_configs={
            "arg1": PathListEditConfig(
                add_files=True,
                add_dirs=True,
                file_filters="Python Files (*.py);;Json Files (*.json)",
                text_elide_mode=PathListEdit.ElideNone,
                drag_n_drop=True,
            ),
            "arg2": PathListEditConfig(
                add_files=True,
                add_dirs=False,
                file_filters="Python Files (*.py);;Json Files (*.json)",
                text_elide_mode=PathListEdit.ElideRight,
                drag_n_drop=True,
            ),
            "arg3": PathListEditConfig(
                add_files=False,
                add_dirs=True,
                text_elide_mode=PathListEdit.ElideLeft,
                drag_n_drop=True,
            ),
        },
    )
    adapter.run()
