"""
Another way to customize the widget of a parameter:

Using @begin...@end tag to wrap the widgets config in the function's docstring

Note: the widgets config between @begin and @end  should be in TOML format

e.g.

@begin

[param_a]
type="Slider"
label="Amount"

[param_b]
type="Dial"
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

    @begin
    [param_a]
      type="Slider"
      label="Amount"

    [param_b]
      type="Dial"
      label="Angel"
      min_value=0
      max_value=180
      show_value_label=true
      value_prefix="angle="
      value_suffix="°"

    @end
    """
    uprint("param_a:", param_a)
    uprint("param_b:", param_b)


gui_adapter = GUIAdapter()
gui_adapter.add(customize_widget_2)
gui_adapter.run()