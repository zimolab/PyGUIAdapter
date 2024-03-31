from examples.parameter_types import parameter_types_demo
from examples.customize_widget_1 import customize_widget_1
from examples.customize_widget_2 import customize_widget_2
from examples.print_and_logging import print_logging_demo
from examples.interact_by_popups import interact_with_popups
from examples.get_started import user_function
from examples.widget_demo_lineedits import lineedits_demo
from examples.widget_demo_numberinputs import number_input_demo
from examples.widget_demo_textedits import text_edits_demo
from examples.widget_demo_selectwidgets import select_widgets_demo
from examples.widget_demo_pathedits import path_edits_demo
from examples.widget_demo_editors import editors_demo

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.commons import DocumentFormat

if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.selection_window_config.icon_mode = False
    gui_adapter.add(parameter_types_demo)

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
        },
    }

    gui_adapter.add(
        customize_widget_1,
        display_document="customize parameter widgets by widget_configs",
        widgets_config=widgets_config,
    )
    gui_adapter.add(customize_widget_2)
    gui_adapter.add(
        print_logging_demo,
        display_name="Print and Logging Demo",
        display_icon="platte",
        display_document="### Show how to print messages",
        document_format=DocumentFormat.MARKDOWN,
    )
    gui_adapter.add(interact_with_popups)
    gui_adapter.add(user_function)
    gui_adapter.add(lineedits_demo)
    gui_adapter.add(number_input_demo)
    gui_adapter.add(text_edits_demo)
    gui_adapter.add(select_widgets_demo)
    gui_adapter.add(path_edits_demo)
    gui_adapter.add(editors_demo)
    gui_adapter.run()
