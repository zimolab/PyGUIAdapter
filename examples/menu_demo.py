from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.ui.menus import ActionItem
from pyguiadapter.ui.window.func_execution.context import ExecutionContext


def on_load_file(ctx: ExecutionContext):
    ctx.show_info_dialog("Load file")


def on_save_file(ctx: ExecutionContext):
    print("save")


def core_logic(a: int, b: float, c: str):
    pass


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.execution_window_config.enable_menubar_actions = True
    gui_adapter.execution_window_config.enable_toolbar_actions = True
    gui_adapter.execution_window_config.title = "Menu Demo"
    action_load = ActionItem(text="Load", callback=on_load_file, shortcut="Ctrl+O")
    action_save = ActionItem(text="Save", callback=on_save_file, shortcut="Ctrl+S")
    func_menus = {
        "File": {
            "Load": action_load,
            "Save": action_save,
        },
    }
    func_toolbar_actions = [action_load, action_save]
    gui_adapter.add(core_logic, menus=func_menus, toolbar_actions=func_toolbar_actions)
    gui_adapter.run()
