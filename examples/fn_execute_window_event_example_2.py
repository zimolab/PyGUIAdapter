from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.utils import messagebox
from pyguiadapter.windows.fnexec import (
    FnExecuteWindow,
    SimpleFnExecuteWindowEventListener,
)


def on_execute_start(window: FnExecuteWindow):
    print("on_execute_start()")


def on_execute_result(window: FnExecuteWindow, result) -> bool:
    print(f"on_execute_result(): {result}")
    messagebox.show_info_message(window, message=f"Result: {result}", title="Result")
    return False


def on_execute_error(window: FnExecuteWindow, error) -> bool:
    print(f"on_execute_error(): {error}")
    messagebox.show_exception_messagebox(window, error)
    return False


def on_execute_finish(window: FnExecuteWindow):
    print("on_execute_finish()")


def event_example_3(a: int = 1, b: int = 1):
    return a / b


if __name__ == "__main__":
    event_listener = SimpleFnExecuteWindowEventListener(
        on_execute_start=on_execute_start,
        on_execute_result=on_execute_result,
        on_execute_error=on_execute_error,
        on_execute_finish=on_execute_finish,
    )
    adapter = GUIAdapter()
    adapter.add(event_example_3, window_listener=event_listener)
    adapter.run()
