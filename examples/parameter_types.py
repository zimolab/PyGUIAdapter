"""
PyGUIAdapter supports the following types as function parameter types:
1.int
2.float
3.bool
4.str
5.list
6.tuple
7.dict
8.typing.Literal
8.any(in PyGUIAdapter any types means json type)

Each type has a corresponding input widget:

int -> IntLineEdit
float -> FloatLineEdit
bool -> CheckBox
str -> LineEdit
list -> ListEditor
tuple -> TupleEditor
dict -> DictEditor
typing.Literal -> ComboBox
any -> JsonEditor

The default value of a function parameter is displayed as a checkbox in the interface, where checking it
means use the default value as argument. If a default value for a parameter is not specified in the function signature,
then None is used as its default value.
"""

from datetime import datetime, date, time
from typing import Literal

from pyguiadapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


# noinspection PyDefaultArgument
def parameter_types_demo(
    int_param: int,
    float_param: float,
    bool_param: bool,
    str_param: str = "this is a string",
    datetime_param: datetime = datetime.now(),
    date_param: date = datetime.now().date(),
    time_param: time = datetime.now().time(),
    list_param: list = None,
    tuple_param: tuple = (1, 2, "3"),
    dict_param: dict = {"a": 1, "b": 2, "c": "3"},
    literal_param: Literal["foo", "bar", "张三", "李四"] = "李四",
    any_param: any = None,
):
    """This function shows default widget for supported parameter types

    :param time_param:
    :param date_param:
    :param datetime_param:
    :param int_param:
    :param float_param:
    :param bool_param:
    :param str_param:
    :param list_param:
    :param tuple_param:
    :param dict_param:
    :param literal_param:
    :param any_param:
    :return:
    """
    uprint("int_param: ", int_param)
    uprint("float_param: ", float_param)
    uprint("bool_param: ", bool_param)
    uprint("str_param: ", str_param)
    uprint("datetime_param: ", datetime_param)
    uprint("date_param: ", date_param)
    uprint("time_param: ", time_param)
    uprint("list_param: ", list_param)
    uprint("tuple_param: ", tuple_param)
    uprint("dict_param: ", dict_param)
    uprint("literal_param: ", literal_param)
    uprint("any_param: ", any_param)
    return "Hello world!"


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(parameter_types_demo)
    gui_adapter.run()
