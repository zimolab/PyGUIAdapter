from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.widgets import IntSpinBoxConfig, FloatSpinBoxConfig, BoolBoxConfig


def foo(a, b, c):
    pass


def bar(a, b, c):
    """
    bar
    @param a:
    @param b:
    @param c:
    @return:

    @params
    [a]
    widget_class = "IntSpinBox"

    [b]
    widget_class = "FloatSpinBox"

    [c]
    widget_class = "BoolBox"

    @end
    """
    pass


configs = {
    "a": IntSpinBoxConfig(),
    "b": FloatSpinBoxConfig(),
    "c": BoolBoxConfig(),
}

adapter = GUIAdapter()
adapter.add(foo, widget_configs=configs)
adapter.add(bar)
adapter.run()
