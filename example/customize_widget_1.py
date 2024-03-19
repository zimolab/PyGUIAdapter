"""
Usually, the widget for a parameter depends on its type, but there are ways to customize the widget.

To do this, we can use the widgets_config parameter of the PyGUIAdapter.run() function.

widgets_config should be a mapping(dict) whose key is the parameter names you want to customize
and the value is the widget configs which is also a dict.

e.g.
...
widgets_config = {
    "param_1": {
        type: "IntSpinBox",
        label: "age",
        docstring: "this parameter means age",
        show_label: True,
        show_docstring: True,
        min_value: 0
        max_value: 200
    }
}
gui_adapter.run(some_func, widgets_config = widgets_config)
...

Every widget has the following configs:
 - type: the name of widget types, str.
    PyGUIAdapter provides a rich set of built-in widget types.
    see the function2widgets.widgets.allwidgets.BASIC_PARAMETER_WIDGETS.
    You can also create your own widget type which should be very easy to do.

 - label: the display name of a parameter, str.
    If not provided, it uses the parameter name as defined in the function signature.
    In above example, parameter 'param_1' will be displayed as 'age'

 - docstring:  the document string of a parameter, str.
    If not provided, the parameter's docstring text will be extracted from the function's docstring.

 - show_label: whether to show the label of a parameter, bool.

 - show_docstring: whether to shoe the docstring of parameter, bool.

 - stylesheet: qss string or file

And each type of widget has its own set of parameters.
For instance:
  IntSpinxBox
    -
  LineEdit

Refer to each widget type's __init__() to know all the parameters.


"""

from pyguiadapter.adapter import GUIAdapter


def customize_widget_1(name: str, password: str, age: int, intro: str):
    pass


gui_adapter = GUIAdapter()
widgets_config = {
    "name": {
        "type": "LineEdit",
        "label": "Account",
        "docstring": "input your name here",
        "show_label": True,
        "show_docstring": True,
        "placeholder": "input account here",
    },
    "password": {
        "type": "LineEdit",
        "label": "Password",
        "show_label": True,
        "show_docstring": True,
        "docstring": "input your password",
    },
    "age": {
        "type": "IntSpinBox",
        "label": "Your age",
        "docstring": "input your age here",
        "show_label": True,
        "show_docstring": True,
        "min_value": 0,
        "max_value": 100,
    },
    "intro": {
        "type": "PlainTextEdit",
        "docstring": "this text will not be seen, cause show_docstring is set to False",
        "show_docstring": False,
    },
}
gui_adapter.add(customize_widget_1, widgets_config=widgets_config)
gui_adapter.run()
