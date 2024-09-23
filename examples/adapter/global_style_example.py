import os.path
from datetime import datetime

from pyguiadapter import utils
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import text_t


def app_style_example(
    arg1: str, arg2: int, arg3: float, arg4: bool, arg5: text_t, arg6: datetime
):
    """
    This example shows how to apply a global stylesheet to the application.

    First, read the stylesheet from a qss file. In this example, [Ubuntu.qss](https://github.com/GTRONICK/QSS/blob/master/Ubuntu.qss)
    will be used. This qss file is from GTRONICK's [QSS](https://github.com/GTRONICK/QSS) repo.

    Then, pass the qss content to the GUIAdapter constructor's **global_style** argument.

    """
    pass


if __name__ == "__main__":

    QSS_FILE = os.path.join(os.path.dirname(__file__), "Ubuntu.qss")
    global_stylesheet = utils.read_text_file(QSS_FILE)

    adapter = GUIAdapter(global_style=global_stylesheet)
    adapter.add(app_style_example)
    adapter.run()
