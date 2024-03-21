from examples.parameter_types import supported_types
from examples.print_and_logging import print_logging_demo
from examples.interact_by_popups import interact_with_popups
from examples.get_started import user_function
from examples.widget_demo_lineedits import lineedits_demo
from examples.widget_demo_numberedits import numberedits_demo
from examples.widget_demo_textedits import textedits_demo
from examples.widget_demo_selectwidgets import selectwidgets_demo
from examples.widget_demo_pathedits import pathedits_demo

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.commons import DocumentFormat

if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.selection_window_config.icon_mode = False
    gui_adapter.add(supported_types)
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
    gui_adapter.run()
