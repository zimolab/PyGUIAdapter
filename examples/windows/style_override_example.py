"""
This example requires PyQtDarkTheme. Please install it before you run this example.
"""

from datetime import datetime

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.extend_types import text_t
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig, OutputBrowserConfig


def app_style_example(
    arg1: str, arg2: int, arg3: float, arg4: bool, arg5: text_t, arg6: datetime
):
    """
    This example requires [PyQtDarkTheme](https://github.com/5yutan5/PyQtDarkTheme).
    Please install it before you run the example.
    <br />

    e.g. using `pip`:

    > `pip install pyqtdarktheme`

    <br />

    The style of output browser will be overridden with **OutputBrowserConfig.stylesheet**

    @param arg1: arg1 description
    @param arg2: arg2 description
    @param arg3: arg3 description
    @param arg4: arg4 description
    @param arg5: arg5 description
    @param arg6: arg6 description
    @return:
    """
    pass


if __name__ == "__main__":
    import qdarktheme

    def on_app_start(app):
        # this will be called after the instantiation of QApplication.
        print("app started")
        qdarktheme.setup_theme("dark")

    adapter = GUIAdapter(on_app_start=on_app_start)
    adapter.add(
        app_style_example,
        window_config=FnExecuteWindowConfig(
            output_browser_config=OutputBrowserConfig(
                stylesheet="""
                background-color: "#380C2A";
                color: "#FFFFFF";
                font-family: "Consolas";
                font-size: 12pt;
                """
            )
        ),
    )
    adapter.run()
