import os.path
from datetime import datetime

from qtpy.QtWidgets import QApplication
from pyguiadapter import utils
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import text_t


def app_style_example(
    arg1: str, arg2: int, arg3: float, arg4: bool, arg5: text_t, arg6: datetime
):
    """
    This example shows how to apply a global stylesheet to the application.

    In this example, [Ubuntu.qss](https://github.com/GTRONICK/QSS/blob/master/Ubuntu.qss)
    will be used. This qss file is from GTRONICK's [QSS](https://github.com/GTRONICK/QSS) repo.

    The QSS will be set in **on_app_start()** callback.
    """
    pass


if __name__ == "__main__":

    QSS_FILE = os.path.join(os.path.dirname(__file__), "Ubuntu.qss")

    def on_app_start(app: QApplication):
        assert isinstance(app, QApplication)
        print("on_app_start")
        qss = utils.read_text_file(QSS_FILE)
        app.setStyleSheet(qss)
        print("app style applied")

    adapter = GUIAdapter(on_app_start=on_app_start)
    adapter.add(app_style_example)
    adapter.run()
