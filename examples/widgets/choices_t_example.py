from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.types import choices_t
from pyguiadapter.widgets import MultiChoiceBoxConfig


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


def choices_t_example(arg1: choices_t, arg2: choices_t, arg3: choices_t):
    """
    example for type **choices_t** and **MultiChoiceBox** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = [2,3]
    choices = [1,2,3,4]
    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = MultiChoiceBoxConfig(
        choices=[MyObject("foo"), MyObject("bar"), MyObject("baz")],
    )
    arg3_conf = MultiChoiceBoxConfig(
        default_value=["opt3"],
        choices=[
            "opt1",
            "opt2",
            "opt3",
            "opt4",
            "opt5",
            "opt6",
            "opt7",
            "opt8",
            "opt9",
            "opt10",
        ],
        columns=3,
    )
    adapter = GUIAdapter()
    adapter.add(
        choices_t_example, widget_configs={"arg2": arg2_conf, "arg3": arg3_conf}
    )
    adapter.run()
