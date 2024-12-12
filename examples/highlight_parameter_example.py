from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.udialog import show_warning_messagebox
from pyguiadapter.adapter.useful import highlight_parameter


def highlight_parameter_example(a: int = 0, b: int = 1, c: int = 2):
    """
    This is an example of `highlight_parameter()`.

    @params
    [b]
    group = "Group 2"

    [c]
    group = "Group 3"

    @end
    """
    if a <= 0:
        show_warning_messagebox("a should be > 0")
        highlight_parameter("a")
        return

    if b < 1:
        show_warning_messagebox("b should be >= 1")
        highlight_parameter("b")
        return

    if c > 2:
        show_warning_messagebox("c should be <= 2")
        highlight_parameter("c")
        return


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(highlight_parameter_example)
    adapter.run()
