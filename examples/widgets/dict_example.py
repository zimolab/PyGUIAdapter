from typing import Dict, Mapping, MutableMapping, TypedDict

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import DictEditConfig


class User(TypedDict):
    name: str
    age: int
    address: str
    email: str


def dict_example(
    arg1: dict, arg2: Dict, arg3: MutableMapping, arg4: Mapping, arg5: User
):
    """
    example for **DictEdit** for **dict-like** types

    @params

    [arg1]
    default_value = {a=1,b=2,c="3"}

    [arg2]
    default_value = {"key1"="value1", "key2"="value2"}

    @end
    """
    uprint(id(arg1))
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)
    uprint("arg4: ", arg4)
    uprint("arg5: ", arg5)


if __name__ == "__main__":
    arg1_conf = DictEditConfig(
        default_value={"a": 1, "b": 2, "c": "3", "d": [1, 2, 3]},
    )
    arg3_conf = DictEditConfig(
        default_value={"a": "A", "b": "B"},
    )

    arg4_conf = DictEditConfig(
        default_value={"c": "C", "d": "D", "e": [1, 2, 3, 4]},
    )

    arg5_conf = DictEditConfig(
        default_value=User(
            name="John", age=30, address="123 Main St", email="john@example.com"
        ),
    )

    adapter = GUIAdapter()
    adapter.add(
        dict_example,
        widget_configs={
            "arg1": arg1_conf,
            "arg3": arg3_conf,
            "arg4": arg4_conf,
            "arg5": arg5_conf,
        },
    )
    adapter.run()
