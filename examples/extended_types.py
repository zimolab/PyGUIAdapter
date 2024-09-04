from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import *


def extended_types_showcase(
    text: text_t,
    int_spinbox: int,
    int_lineedit: int_t,
    float_spinbox: float,
    float_lineedit: float_t,
    file_list: file_list_t,
    choice: choice_t,
):
    """

    @params
    [choice]
    default_value = ""
    choices = ["Python", "C++", "C", "Java", "Rust", "Others"]

    @end

    """


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(extended_types_showcase)
    adapter.run()
