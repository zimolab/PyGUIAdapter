from typing import Any

from pyguiadapter.adapter import GUIAdapter


def json_example(arg1: object, arg2: Any):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(json_example)
    adapter.run()
