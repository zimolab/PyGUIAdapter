from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import *


def extended_types_showcase(
    text: text_t,
    int_spinbox: int,
    int_lineedit: int_t,
    float_spinbox: float,
    float_lineedit: float_t,
    file_list: files_t,
    choice: choice_t,
    multi_choices: choices_t,
):
    """

    @params
    [choice]
    default_value = ""
    choices = ["Python", "C++", "C", "Java", "Rust", "Others"]

    [multi_choices]
    default_value = "Python"
    choices = ["Python", "C++", "C", "Java", "Rust", "Others"]

    @end

    """


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(extended_types_showcase)
    adapter.run()
