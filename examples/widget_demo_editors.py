from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def editors_demo(
    universal_code: str,
    json_obj: any = 10,
    list_obj: list = [],
    tuple_obj: tuple = (),
    dict_obj: dict = {},
):
    """This demo show widgets for complex data types

    @widgets
    [universal_code]
    widget_class="CodeEditor"
    configs.Lexer="Python"
    @end
    """
    uprint("universal_code: ", universal_code)
    uprint("json_obj: ", json_obj)
    uprint("list_obj: ", list_obj)
    uprint("tuple_obj: ", tuple_obj)
    uprint("dict_obj: ", dict_obj)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.execution_window_config.show_function_result_dialog = False
    gui_adapter.add(editors_demo)
    gui_adapter.run()
