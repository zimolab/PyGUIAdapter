from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def function_1(arg1: int, arg2: str, arg3: bool) -> None:
    pass


def function_2(arg1: int, arg2: str, arg3: bool) -> None:
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        function_1,
        # set window config for function_1
        window_config=FnExecuteWindowConfig(
            title="Function 1", clear_checkbox_visible=True
        ),
    )
    adapter.add(
        function_2,
        # set window config for function_2
        window_config=FnExecuteWindowConfig(
            title="Function 2",
            size=(400, 600),
            clear_checkbox_visible=False,
            clear_checkbox_checked=False,
            document_dock_visible=False,
        ),
    )
    adapter.run()
