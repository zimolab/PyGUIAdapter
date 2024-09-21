from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.types import choice_t, choices_t
from pyguiadapter.widgets import ChoiceBoxConfig


class MyObject(object):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, MyObject):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        # this method is very important
        # the return value will be displayed as the ChoiceBox's item
        return self.name


def choice_t_example(arg1: choice_t, arg2: choice_t, arg3: choices_t):
    """
    example for type **choice_t** and **ChoiceBox** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3
    @return:

    @params
    [arg1]
    choices = [1,2,3,4]

    @end
    """
    uprint("arg1:", arg1, f", type: {type(arg1)}")
    uprint("arg2:", arg2, f", type: {type(arg2)}")
    uprint("arg3:", arg3, f", type: {type(arg3)}")


if __name__ == "__main__":
    arg2_conf = ChoiceBoxConfig(
        default_value="opt2", choices=["opt1", "opt2", "opt3", "opt4"], editable=True
    )
    arg3_conf = ChoiceBoxConfig(
        choices=[MyObject("apple"), MyObject("banana"), MyObject("orange")]
    )

    adapter = GUIAdapter()
    adapter.add(
        choice_t_example,
        widget_configs={
            "arg2": arg2_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
