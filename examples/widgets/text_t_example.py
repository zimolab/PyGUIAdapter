from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.types import text_t
from pyguiadapter.widgets import TextEditConfig


def text_t_example(arg1: text_t, arg2: text_t, arg3: text_t = "foo") -> str:
    """
    example for **text_t** and **TextEdit**

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3
    @return:

    @params
    [arg1]
    default_value = "Hello World"


    [arg2]
    default_value = "你好，世界！"


    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return "{};{};{}".format(arg1, arg2, arg3)


if __name__ == "__main__":

    arg3_conf = TextEditConfig(
        # this will override the default_value defined in the function signature
        default_value="bar",
        placeholder="Please input some text here!",
    )

    adapter = GUIAdapter()
    adapter.add(
        text_t_example,
        widget_configs={"arg3": arg3_conf},
    )
    adapter.run()
