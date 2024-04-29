from pyguiadapter import GUIAdapter


def foo(msg: str):
    pass


def bar(param1: int):
    pass


if __name__ == "__main__":

    gui_adapter = GUIAdapter()
    gui_adapter.add(foo, window_title="Foo")
    gui_adapter.add(bar, window_title="Bar")
    gui_adapter.run()
