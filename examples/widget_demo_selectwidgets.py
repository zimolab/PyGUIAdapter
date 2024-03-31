from typing import Literal

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def select_widgets_demo(
    combo_1: Literal["opt1", "opt2", "opt3"],
    combo_2: str,
    combo_3: str,
    checkbox: bool,
    checkbox_group: str,
    radio_button_group: str,
):
    """
    This demo shows how to use select widgets
    :param combo_1:  <b>combobox: items from typing.Literal</b>
    :param combo_2: <b>combobox: items from config</b>
    :param combo_3: <b>combobox: editable</b>
    :param checkbox: <b>checkbox: yes or no choice</b>
    :param checkbox_group:  <b>checkbox group: multiple options and choices</b>
    :param radio_button_group: <b>radio group: multiple options but only one choice</b>
    :return:

    @widgets
    [combo_2]
    widget_class="ComboBox"
    # when you use ComboBox, items must be provided, or an error will be raised
    items=["选项1", "选项2", "选项3"]

    [combo_3]
    widget_class="ComboBoxEdit"
    items=["选项1", "选项2", "选项3"]

    [checkbox]
    widget_class="CheckBox"
    text="Use this option"

    [checkbox_group]
    widget_class="CheckBoxGroup"
    # when you use CheckBoxGroup, items must be provided, or an error will be raised
    items=["A", "B", "C", "D", "E", "F" , "G", "H", "I", "J"]
    column_count=3

    [radio_button_group]
    widget_class="RadioButtonGroup"
    # when you use CheckBoxGroup, items must be provided, or an error will be raised
    items=["A", "B", "C", "D", "E", "F" , "G", "H", "I", "J"]
    column_count=3
    @end
    """
    uprint("combo_1:", combo_1)
    uprint("combo_2:", combo_2)
    uprint("combo_3:", combo_3)
    uprint("checkbox:", checkbox)
    uprint("checkbox_group:", checkbox_group)
    uprint("radio_button_group:", radio_button_group)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(select_widgets_demo)
    gui_adapter.run()
