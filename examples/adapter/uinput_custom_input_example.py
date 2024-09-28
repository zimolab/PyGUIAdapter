from typing import Any

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import uinput
from pyguiadapter.adapter.ucontext import uprint


def input_json_example(title: str) -> Any:
    ret = uinput.get_json_object(title)
    uprint(ret)


def input_py_literal_example(title: str) -> Any:
    ret = uinput.get_py_literal(title)
    uprint(ret)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(input_json_example)
    adapter.add(input_py_literal_example)
    adapter.run()
