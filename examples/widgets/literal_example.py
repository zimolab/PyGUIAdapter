from typing import Literal

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import ExclusiveChoiceBoxConfig


class MyObj(object):
    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, MyObj):
            return other._name == self._name
        return False

    def __hash__(self):
        return hash(self._name)


my_objects = [MyObj("obj1"), MyObj("obj2"), MyObj("obj3")]


def literal_example(
    arg1: Literal["option1", "option2", "option3"] = "option2",
    arg2: Literal[1, 2, 3, 4, 5] = 3,
    arg3: Literal["option1", "option2", 1, 2, True, False] = 1,
    arg4: MyObj = my_objects[0],
):
    """
    example for type **typing.Literal**
    @params
    [arg3]
    columns = 2
    show_type_icon = false
    @end
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)
    uprint(f"arg4: {arg4}({type(arg4)})")


if __name__ == "__main__":
    arg4_conf = ExclusiveChoiceBoxConfig(
        # this will override the default value defined in the function signature
        default_value=my_objects[1],
        show_type_icon=True,
        choices=my_objects,
        object_icon="ei.asl",
    )
    adapter = GUIAdapter()
    adapter.add(literal_example, widget_configs={"arg4": arg4_conf})
    adapter.run()
