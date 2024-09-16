from datetime import time

from pyguiadapter.adapter import GUIAdapter


def time_example(arg1: time, arg2: time, arg3: time):
    """
    example for type **time** and **TimeEdit** widget
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(time_example)
    adapter.run()
