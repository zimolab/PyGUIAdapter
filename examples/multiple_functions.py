from examples.parameter_types import supported_types
from examples.customize_widget_1 import customize_widget_1
from examples.customize_widget_2 import customize_widget_2
from examples.print_and_logging import print_logging_demo
from examples.interact_by_popups import interact_with_popups
from examples.get_started import user_function
from examples.widget_demo_lineedits import lineedits_demo
from examples.widget_demo_numberedits import numberedits_demo
from examples.widget_demo_textedits import textedits_demo
from examples.widget_demo_selectwidgets import selectwidgets_demo
from examples.widget_demo_pathedits import pathedits_demo
from examples.widget_demo_codeeditors import codeeditors_demo

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.commons import DocumentFormat

if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.selection_window_config.icon_mode = False
    gui_adapter.add(supported_types)

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
            "echo_mode": "Password",
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
    gui_adapter.add(numberedits_demo)
    gui_adapter.add(textedits_demo)
    gui_adapter.add(selectwidgets_demo)
    gui_adapter.add(pathedits_demo)
    gui_adapter.add(codeeditors_demo)
    gui_adapter.run()
