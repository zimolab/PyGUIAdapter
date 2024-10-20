from pyguiadapter.adapter import GUIAdapter


def show_select_win_anyway():
    """
    This example shows how to show function select window(FnSelectWindow) even if only one function was added.
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(show_select_win_anyway)
    adapter.run(show_select_window=True)
