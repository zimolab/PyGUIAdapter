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

from typing import Literal

from pyguiadapter.adapter import GUIAdapter


def supported_types(
    int_param: int,
    float_param: float,
    bool_param: bool,
    str_param: str = "this is a string",
    list_param: list = None,
    tuple_param: tuple = (1, 2, "3"),
    dict_param: dict = {"a": 1, "b": 2, "c": "3"},
    literal_param: Literal["foo", "bar", "张三", "李四"] = "李四",
    any_param: any = None,
):
    """This function shows default widget for all supported parameter types

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
    pass


gui_adapter = GUIAdapter()
gui_adapter.add(supported_types)
gui_adapter.run()
