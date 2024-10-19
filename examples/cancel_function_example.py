import time

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint, is_function_cancelled
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def cancel_function_example(target: int = 10, delay_per_iter: float = 0.5):
    """
    @params
    [target]
    min_value = 1

    [delay_per_iter]
    min_value = 0.001
    step = 0.5
    decimals = 3

    @end
    """
    for i in range(target):
        if is_function_cancelled():
            break
        uprint("process: ", i)
        time.sleep(delay_per_iter)
    uprint("done!")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        cancel_function_example,
        cancelable=True,
        window_config=FnExecuteWindowConfig(disable_widgets_on_execute=True),
    )
    adapter.run()
