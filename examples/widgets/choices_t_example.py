from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import choices_t
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
    This is an example for type **choices_t** type hint and **MultiChoiceBox** widget.

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg1]
    default_value = ["opt1", "opt2"]
    choices = ["opt1", "opt2", "opt3", "opt4", "opt5"]
    @end
    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg2_conf = MultiChoiceBoxConfig(
        choices=[MyObject("foo"), MyObject("bar"), MyObject("baz")]
    )
    arg3_conf = MultiChoiceBoxConfig(
        default_value=(1, 2, 3),
        choices={
            "Option 1": 1,
            "Option 2": 2,
            "Option 3": 3,
            "Option 4": 4,
            "Option 5": 5,
        },
        columns=2,
    )
    adapter = GUIAdapter()
    adapter.add(
        choices_t_example, widget_configs={"arg2": arg2_conf, "arg3": arg3_conf}
    )
    adapter.run()
