from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.window import BaseWindowEventListener
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox


def event_example_1():
    pass


class ExampleEventListener(BaseWindowEventListener):

    def on_create(self, window: FnExecuteWindow):
        print("on_create")
        super().on_create(window)

    def on_close(self, window: FnExecuteWindow) -> bool:
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

    def on_destroy(self, window: FnExecuteWindow):
        print("on_destroy")
        super().on_destroy(window)

    def on_hide(self, window: FnExecuteWindow):
        print("on_hide")
        super().on_hide(window)

    def on_show(self, window: FnExecuteWindow):
        print("on_show")
        super().on_show(window)


if __name__ == "__main__":
    event_listener = ExampleEventListener()
    adapter = GUIAdapter()
    adapter.add(event_example_1, window_listener=event_listener)
    adapter.run()
