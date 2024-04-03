import threading

from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint
from pyguiadapter.ui.window.func_execution import ExecutionWindow
from pyguiadapter.ui.window.class_init import ClassInitWindow
from pyguiadapter.ui.window.func_selection import SelectionWindow


class Foo(object):
    def __init__(self, a: int, b: str, c: float):
        """This is Foo class"""
        self._a = a
        self._b = b
        self._c = c

    def foo(self, a: int, b: str, c: float):
        uprint("Foo.foo() called!")
        a = a or self._a
        b = b or self._b
        c = c or self._c
        uprint("a: {}, b: {}, c: {}".format(a, b, c))


def on_application_started(application: QApplication):
    print("Application started!", threading.current_thread())
    apply_stylesheet(application, theme="light_teal.xml")


def on_execution_window_created(execution_window: ExecutionWindow):
    print("Execution window created!", threading.current_thread())


def on_initialization_window_created(initialization_window: ClassInitWindow):
    print("Initialization window created!", threading.current_thread())


def on_selection_window_created(selection_window: SelectionWindow):
    print("Selection window created!", threading.current_thread())


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.always_show_selection_window = True
    gui_adapter.on_app_started(on_application_started)
    gui_adapter.on_class_init_window_created(on_initialization_window_created)
    gui_adapter.on_selection_window_created(on_selection_window_created)
    gui_adapter.on_execution_window_created(on_execution_window_created)

    with gui_adapter.instantiate_class(Foo) as foo_instance:
        gui_adapter.add(Foo.foo, bind=foo_instance)
        gui_adapter.run()
