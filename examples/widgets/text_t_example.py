from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import text_t
from pyguiadapter.widgets import TextEditConfig


def text_t_example(arg1: text_t, arg2: text_t, arg3: text_t = "foo") -> str:
    """
    This is an example for **text_t** type hint and **TextEdit** widget.

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
    assert isinstance(arg1, str)
    assert isinstance(arg2, str)
    assert isinstance(arg3, str)
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)
    return "{};{};{}".format(arg1, arg2, arg3)


if __name__ == "__main__":

    arg3_conf = TextEditConfig(
        default_value="bar",
        placeholder="Please input some text here!",
    )

    adapter = GUIAdapter()
    adapter.add(text_t_example, widget_configs={"arg3": arg3_conf})
    adapter.run()
