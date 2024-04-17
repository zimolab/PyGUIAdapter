"""
This demo shows different types of line edit.
"""

from pyguiadapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def lineedits_demo(str_lineedit: str, int_lineedit: int, float_lineedit: float):
    """
    Demonstrating different types of lineedit.

    :param str_lineedit: used for input single line text
    :param int_lineedit: used for input integer number
    :param float_lineedit: used for input float number
    :return:

    @widgets
    [str_lineedit]
    widget_class="LineEdit"
    #below are some args for LineEdit widget
    placeholder = ""
    clear_button = false
    echo_mode = "Normal"
    regex =  ".*"
    input_mask = "00.0000.000"

    [int_lineedit]
    widget_class="IntLineEdit"


    [float_lineedit]
    widget_class="FloatLineEdit"

    @end
    """
    uprint("int_lineedit:", int_lineedit)
    uprint("str_lineedit:", str_lineedit)
    uprint("float_lineedit:", float_lineedit)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(lineedits_demo)
    gui_adapter.run()
