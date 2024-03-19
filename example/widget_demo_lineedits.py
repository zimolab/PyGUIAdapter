"""
This demo shows different types of line edit.
"""

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def lineedits_demo(str_lineedit: str, int_lineedit: int, float_lineedit: float):
    """
    Demonstrating different types of lineedit.

    :param str_lineedit: used for input single line text
    :param int_lineedit: used for input integer number
    :param float_lineedit: used for input float number
    :return:

    @begin
    [str_lineedit]
    type="LineEdit"
    #below are parameters of LineEdit widget
    #placeholder = ""
    #clear_button = false
    #echo_mode = "Normal"
    #regex =  ".*"
    #input_mask = "00.0000.000"

    [int_lineedit]
    type="IntLineEdit"


    [float_lineedit]
    type="FloatLineEdit"

    @end
    """
    uprint("int_lineedit:", int_lineedit)
    uprint("str_lineedit:", str_lineedit)
    uprint("float_lineedit:", float_lineedit)


gui_adapter = GUIAdapter()
gui_adapter.add(lineedits_demo)
gui_adapter.run()
