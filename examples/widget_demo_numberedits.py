"""
This demo shows widgets for inputting numbers, see: function2widgets.widgets.numberedit
"""

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def numberedits_demo(
    int_spin: int,
    float_spin: float,
    dail: int,
    slider: int,
):
    """
    This demo shows widgets for inputting numbers

    :param int_spin:
    :param float_spin:
    :param dail:
    :param slider:
    :return:

    @begin
    [int_spin]
    type="IntSpinBox"
    min_value=0
    max_value=100
    step=1
    prefix="height = "
    suffix=" meter(s)"
    default=10

    [float_spin]
    type="FloatSpinBox"
    min_value=0.0
    max_value=1.0
    step=0.00000001
    decimals=8
    prefix="rate="
    suffix=""
    accelerated=true


    [dail]
    type="Dial"
    min_value=0
    max_value=180
    step=1
    #page_step=1
    tracking=true
    wrapping=true
    notches_visible=true
    notches_target=4.0
    inverted_appearance=false
    inverted_control=false
    show_value_label=true
    value_prefix="angel= "
    value_suffix="°"

    [slider]
    type="Slider"
    min_value=0
    max_value=100
    step=1
    #page_step=1
    tracking=true
    # tick_position: "Above", "Below", "Both", "Left", "Right", "None"
    tick_position="Above"
    tick_interval=2
    inverted_appearance=false
    inverted_control=false
    show_value_label=true
    value_prefix="value:"
    value_suffix=""

    @end
    """
    uprint("int_spin:", int_spin)
    uprint("float_spin:", float_spin)
    uprint("dail:", dail)
    uprint("slider:", slider)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(numberedits_demo)
    gui_adapter.run()
