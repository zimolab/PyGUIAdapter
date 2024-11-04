from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import file_list_t
from pyguiadapter.widgets import FileListEditConfig, FileListEdit


def file_list_t_example(arg1: file_list_t, arg2: file_list_t, arg3: file_list_t):
    """
    This is an example for **file_list_t** type hint and **FileListEdit** widget.

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
        file_list_t_example,
        widget_configs={
            "arg1": FileListEditConfig(
                file_filters="Python Files (*.py);;Json Files (*.json)",
                text_elide_mode=FileListEdit.ElideNone,
                drag_n_drop=True,
                normalize_path=False,
                absolutize_path=False,
            ),
            "arg2": FileListEditConfig(
                file_filters="Python Files (*.py);;Json Files (*.json)",
                text_elide_mode=FileListEdit.ElideRight,
                drag_n_drop=True,
                normalize_path=True,
                absolutize_path=True,
            ),
            "arg3": FileListEditConfig(
                text_elide_mode=FileListEdit.ElideLeft,
                drag_n_drop=True,
            ),
        },
    )
    adapter.run()
