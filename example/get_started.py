"""
Turn your function into gui is easy:

1. Import GUIAdapter from  pyguiadapter.adapter package
2. Write your functions
3. Create an instance of GUIAdapter
4. Add your function(s) to the instance
5. Invoke run() method of the instance

"""

from pyguiadapter.adapter import GUIAdapter


def user_function(a: int, b: int) -> int:
    """This is a user function."""
    return a + b


gui_adapter = GUIAdapter()
gui_adapter.always_show_selection_window = True
gui_adapter.add(user_function)
gui_adapter.run()
