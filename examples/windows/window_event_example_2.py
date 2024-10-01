from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.window import SimpleWindowStateListener
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox


def on_window_create(window: FnExecuteWindow):
    print("on_create")


def on_window_show(window: FnExecuteWindow):
    print("on_show")


def on_window_hide(window: FnExecuteWindow):
    print("on_hide")


def on_window_close(window: FnExecuteWindow) -> bool:
    print("on_close")
    ret = messagebox.show_question_message(
        window,
        title="Confirm Quit",
        message="Are you sure to quit?",
        buttons=messagebox.Yes | messagebox.No,
    )
    if ret == messagebox.Yes:
        return True
    return False


def on_window_destroy(window: FnExecuteWindow):
    print("on_destroy")


def event_example_2():
    pass


if __name__ == "__main__":
    event_listener = SimpleWindowStateListener(
        on_create=on_window_create,
        on_show=on_window_show,
        on_hide=on_window_hide,
        on_close=on_window_close,
        on_destroy=on_window_destroy,
    )
    adapter = GUIAdapter()
    adapter.add(event_example_2, window_listener=event_listener)
    adapter.run()
