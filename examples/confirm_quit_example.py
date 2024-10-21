from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.utils import messagebox
from pyguiadapter.window import SimpleWindowEventListener
from pyguiadapter.windows.fnexec import FnExecuteWindow


def foo(arg1: int, arg2: str, arg3: bool):
    pass


def on_close(window: FnExecuteWindow) -> bool:
    ret = messagebox.show_question_message(
        window, message="Are you sure you want to quit?"
    )
    if ret == messagebox.Yes:
        # when `on_close()` returns True, the window will be closed
        return True
    else:
        messagebox.show_info_message(window, message="Quit cancelled by user!")
        # when `on_close()` returns False, the window will not be closed
        # in other words, the close event will be ignored
        return False


if __name__ == "__main__":
    # create a window listener that listens for the `on_close` event
    event_listener = SimpleWindowEventListener(on_close=on_close)

    adapter = GUIAdapter()
    # add the `foo` function to the adapter with the `window_listener` argument set to the event_listener
    adapter.add(foo, window_listener=event_listener)
    adapter.run()
