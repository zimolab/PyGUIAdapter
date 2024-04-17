"""
Change the position of the description label:
  it can be above the center_widget with args.description_position=0
  it can be below the center_widget with args.description_position=1
"""

from pyguiadapter import GUIAdapter


def user_function(a: int, b: int) -> int:
    """

    :param a: this is the description of parameter a
    :param b: this is the description of parameter b
    :return:

    @widgets
    [a]
    description_position=0

    [b]
    description_position=1

    @end
    """

    return a + b


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(user_function)
    gui_adapter.run()
