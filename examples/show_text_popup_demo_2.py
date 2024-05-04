from PyQt6.QtWidgets import QDialogButtonBox

from pyguiadapter import GUIAdapter
from pyguiadapter.interact.popup_info import TextPopupInfo
from pyguiadapter.interact.upopup import show_license_popup, show_text_popup
from pyguiadapter.ui import ExecutionContext, ActionItem

info = """
<strong>PyGUIAdapter</strong>
<p>
PyGUIAdapter is a library that makes it easy to convert (almost) any Python functions into a GUI application.
</p>

<p>Scan the qrcode below to visit the github repo of this lib.</p>

<p style="text-align:center">
<img src="./demo_img.png" />
</p>
<p style="text-align:center">
or click this link: <a href="https://github.com/zimolab/PyGUIAdapter">PyGUIAdapter</a>
</p>

"""


def show_text_popup_demo2():
    pass


def _action_show_about(ctx: ExecutionContext):
    show_text_popup(
        TextPopupInfo(text=info, window_title="About", open_external_link=True)
    )


if __name__ == "__main__":
    menus = {
        "About": {
            "Show About": ActionItem("Show About", _action_show_about),
        },
    }
    gui_adapter = GUIAdapter()
    gui_adapter.execution_window_config.enable_menubar_actions = True
    gui_adapter.add(show_text_popup_demo2, menus=menus)
    gui_adapter.run()
