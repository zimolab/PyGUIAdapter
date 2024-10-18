from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.utils import messagebox
from pyguiadapter.window import SimpleWindowEventListener
from pyguiadapter.windows.fnselect import FnSelectWindow


def on_window_create(window: FnSelectWindow):
    print("on_create")


def on_window_show(window: FnSelectWindow):
    print("on_show")


def on_window_hide(window: FnSelectWindow):
    print("on_hide")


def on_window_close(window: FnSelectWindow) -> bool:
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


def on_window_destroy(window: FnSelectWindow):
    print("on_destroy")


def event_example_3():
    pass


if __name__ == "__main__":
    event_listener = SimpleWindowEventListener(
        on_create=on_window_create,
        on_show=on_window_show,
        on_hide=on_window_hide,
        on_close=on_window_close,
        on_destroy=on_window_destroy,
    )
    adapter = GUIAdapter()
    adapter.add(event_example_3)
    adapter.run(show_select_window=True, select_window_listener=event_listener)
