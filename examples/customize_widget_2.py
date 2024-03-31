"""
Another way to customize the widget of a parameter:

Using @widgets...@end tag to wrap the widget configs in the function's docstring

Note: the widget configs between @widget and @end  should be in TOML format

e.g.

@widgets

[param_a]
widget_class="Slider"
label="Amount"

[param_b]
widget_class="Dial"
label="Angel"
prefix="angel"
suffix="°"

@end

"""

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def customize_widget_2(param_a: int = 10, param_b: int = 180):
    """
    Customize widget in docstring

    :param param_a:
    :param param_b:
    :return:

    @widgets
    [param_a]
      widget_class="Slider"
      label="Amount"
      show_value_label=true
      tracking=false

    [param_b]
      widget_class="Dial"
      label="Angel"
      min_value=0
      max_value=180
      show_value_label=true
      value_prefix="angle="
      value_suffix="°"
      tracking=true

    @end
    """
    uprint("param_a:", param_a)
    uprint("param_b:", param_b)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(customize_widget_2)
    gui_adapter.run()
