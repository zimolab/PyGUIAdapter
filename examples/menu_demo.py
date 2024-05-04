from pyguiadapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint
from pyguiadapter.ui import ExecutionContext, ActionItem


def _action_show_document_dock(ctx: ExecutionContext):
    ctx.invoke("show_document_dock")


def _action_hide_document_dock(ctx: ExecutionContext):
    ctx.invoke("hide_document_dock")


def _action_show_output_dock(ctx: ExecutionContext):
    ctx.invoke("show_output_dock")


def _action_hide_output_dock(ctx: ExecutionContext):
    ctx.invoke("hide_output_dock")


def _action_hide_all_docks(ctx: ExecutionContext):
    ctx.invoke("hide_document_dock")
    ctx.invoke("hide_output_dock")


def menu_demo(foo: str):
    uprint(f"foo: {foo}")


if __name__ == "__main__":
    menus = {
        "View": {
            "Show Document": ActionItem("Show Document", _action_show_document_dock),
            "Show Output": ActionItem("Show Output", _action_show_output_dock),
            "Hide All": ActionItem("Hide All", _action_hide_all_docks),
        },
    }

    gui_adapter = GUIAdapter()
    gui_adapter.execution_window_config.enable_menubar_actions = True
    gui_adapter.add(menu_demo, menus=menus)
    gui_adapter.run()
