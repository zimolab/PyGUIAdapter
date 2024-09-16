from datetime import datetime

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint


def datetime_example(arg1: datetime, arg2: datetime, arg3: datetime):
    """
    example for type **datetime** and DateTimeEdit widget
    """
    uprint("arg1", arg1)
    uprint("arg2", arg2)
    uprint("arg3", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(datetime_example)
    adapter.run()
