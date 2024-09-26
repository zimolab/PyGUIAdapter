from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows.fnselect import FnSelectWindowConfig


def fn1():
    """
    This example shows how config the **function select window**
    """
    pass


def fn2():
    """
    This example shows how config the **function select window**
    """
    pass


if __name__ == "__main__":

    select_window_config = FnSelectWindowConfig(title="My Tool Kit")

    adapter = GUIAdapter()
    adapter.add(fn1)
    adapter.add(fn2)
    adapter.run(select_window_config=select_window_config)
