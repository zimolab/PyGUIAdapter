from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows import FnExecuteWindowConfig


def resize_window_demo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        resize_window_demo,
        window_config=FnExecuteWindowConfig(
            size=(300, 400),
        ),
    )
    adapter.run()
