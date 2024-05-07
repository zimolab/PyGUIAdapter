from pyguiadapter import GUIAdapter
from pyguiadapter.interact.upopup import show_about_popup
from pyguiadapter.ui import ExecutionContext, ActionItem


def show_text_popup_demo2():
    pass


def _action_show_about(ctx: ExecutionContext):
    show_about_popup(
        app_name="PyGUIAdapter",
        app_logo="./demo_logo_1.png",
        app_copyright="copyright © zimolab. All right reserved",
        app_fields={
            "License": "GPL",
            "Version": "0.0.1",
            "Author": "zimolab",
            "GitHub": "<a href='https://github.com/zimolab/PyGUIAdapter'>PyGUIAdapter</a>",
        },
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
