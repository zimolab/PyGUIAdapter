from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint


def greeting(name: str):
    """
    This is a simple *hello world* demo of [`PyGUIAdapter`](https://github.com/zimolab/PyGUIAdapter).

    :param name:  Hi, please tell me what your name
    """
    uprint(f"Hello {name}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(greeting)
    adapter.run()
