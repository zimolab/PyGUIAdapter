from datetime import datetime

from qtpy.QtWidgets import QApplication

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.extend_types import text_t


def app_style_example(
    arg1: str, arg2: int, arg3: float, arg4: bool, arg5: text_t, arg6: datetime
):
    """
    This example requires [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet).
    Please install it before you run the example.

    <br />

    e.g. using `pip`:

    > `pip install qdarkstyle`

    @param arg1: arg1 description
    @param arg2: arg2 description
    @param arg3: arg3 description
    @param arg4: arg4 description
    @param arg5: arg5 description
    @param arg6: arg6 description
    @return:

    @params
    [arg6]
    calendar_popup = true

    @end

    """
    pass


if __name__ == "__main__":
    import qdarkstyle

    def on_app_start(app: QApplication):
        # this will be called after the instantiation of QApplication.
        print("app started")
        app.setStyleSheet(qdarkstyle.load_stylesheet())

    adapter = GUIAdapter(on_app_start=on_app_start)
    adapter.add(app_style_example)
    adapter.run()
