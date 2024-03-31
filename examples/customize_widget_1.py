"""
Usually, the widget for a parameter depends on its type, but there are ways to customize the widget.

To do this, we can use the widget_configs parameter of PyGUIAdapter.run() function.

e.g.
```python
...
widget_configs = {
    "param_1": {
        "widget_class": "IntSpinBox",
        "label": "age",
        "description": "this parameter means age",
        "min_value": 0,
        "max_value": 200
        # more args of this parameter widget
    }

    "param_2": {
        ...
    },
    ...
}

gui_adapter.run(some_func, widget_configs = widget_configs)
```
...

Every widget shares the following args:
- default: the default value of this parameter
- label: the label of the parameter, if not specified, will be the parameter name
- description: the description of the parameter, if not specified, will look into docstring to see if there is description
               of the parameter
- stylesheet: the stylesheet string of the parameter widget
- set_default_on_init: whether to set the default value to the parameter widget when the widget is created
- hide_default_widget: whether to hide the default widget(usually a checkbox)
                        if the default value if None, this will be ignored
- default_widget_text: text template for the default widget
- separate_line: whether to add a horizontal line in the bottom of the parameter widget

Every widget also has it own args, which can be found in the source code of the widget class.

You can refer to function2widgets.widgets.* for all available widgets classes, like LineEdit IntSpinBox ComboBox etc.

For each widget class arguments, check the <WIDGET_CLASSNAME>Args class, such as LineEditArgs IntSpinBoxArgs ComboBoxArgs etc.

"""

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def customize_widget_1(name: str, password: str, age: int, intro: str):
    uprint("name:", name)
    uprint("password:", password)
    uprint("age:", age)
    uprint("intro:", intro)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    widgets_config = {
        "name": {
            "widget_class": "LineEdit",
            "label": "Account",
            "description": "input your name here",
            "placeholder": "input account here",
        },
        "password": {
            "widget_class": "LineEdit",
            "label": "Password",
            "echo_mode": "Password",
            "description": "input your password",
        },
        "age": {
            "widget_class": "IntSpinBox",
            "label": "Your age",
            "description": "input your age here",
            "min_value": 0,
            "max_value": 100,
        },
        "intro": {
            "widget_class": "PlainTextEdit",
            # "description": "this text will not be seen, cause show_docstring is set to False",
        },
    }
    gui_adapter.add(customize_widget_1, widget_configs=widgets_config)
    gui_adapter.run()
