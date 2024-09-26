from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import StringListEditConfig
from pyguiadapter.extend_types import string_list_t


def string_list_t_example(
    arg1: string_list_t,
    arg2: string_list_t,
    arg3: string_list_t,
):
    """
    example for type **string_list_t** and **StringListEdit** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = ["a", "b", "c", "d"]
    add_file = true
    add_dir = false
    file_filters = "Python files(*.py);;Text files(*.txt)"

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = StringListEditConfig(add_file=False, add_dir=True)
    arg3_conf = StringListEditConfig(add_file=False, add_dir=False)
    adapter = GUIAdapter()
    adapter.add(
        string_list_t_example, widget_configs={"arg2": arg2_conf, "arg3": arg3_conf}
    )
    adapter.run()
