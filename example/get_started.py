"""
Turn your function into gui in just a few lines:

1.Import GUIAdapter from  pyguiadapter.adapter package
2.Write your function.
3.Create an instance of GUIAdapter
4.Add your function to the instance
5.Invoke run() method of the instance

"""

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.commons import DocumentFormat


def user_function(a: int, b: int) -> int:
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat…"""
    return a + b


gui_adapter = GUIAdapter()
gui_adapter.always_show_selection_window = True
gui_adapter.add(user_function)
gui_adapter.run()
