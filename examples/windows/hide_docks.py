from pyguiadapter.adapter import GUIAdapter, udialog
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def hide_docks_example(a: int, b: str, c: bool):
    if a < 0:
        raise ParameterError("a", "a must >= 0")
    if b == "":
        raise ValueError("invalid value of b")
    udialog.show_info_messagebox(f"Receive: {a}, {b}, {c}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        hide_docks_example,
        window_config=FnExecuteWindowConfig(
            size=(300, 400),
            show_document_dock=False,
            show_output_dock=False,
        ),
    )
    adapter.run()
