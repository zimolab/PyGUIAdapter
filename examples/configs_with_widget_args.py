from function2widgets.widgets import LineEdit
from function2widgets.widgets.lineedit import LineEditArgs

from pyguiadapter.adapter import AS_IS, GUIAdapter


def foo(msg: str):
    pass


if __name__ == "__main__":
    configs = {
        "msg": {
            "widget_class": LineEdit.__name__,
            "widget_args": LineEditArgs(
                parameter_name=AS_IS,
                label="Param A",
                default=None,
                description="This is param A",
                placeholder="placeholder",
                default_value_description="use default value",
            ),
        }
    }

    gui_adapter = GUIAdapter()
    gui_adapter.add(foo, widget_configs=configs)
    gui_adapter.run()
