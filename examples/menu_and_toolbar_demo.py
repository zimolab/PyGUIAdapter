import json
import threading

from pyguiadapter import GUIAdapter
from pyguiadapter.ui import ActionItem
from pyguiadapter.ui import ExecutionContext


def on_load_file(ctx: ExecutionContext):
    if not ctx.show_question_dialog("load parameter values from a file?"):
        return
    filepath = ctx.get_open_file_path()
    # we assume the file is a valid json file and is not very large
    # so that we can load it in the main thread
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            param_values = json.load(f)
        # set_param_values() may raise an exception
        # we need to handle it by ourself.
        ctx.set_param_values(param_values, ignore_exceptions=False)
    except BaseException as e:
        print(e)
        ctx.logging_fatal(f"{e}")
        return


def on_save_file(ctx: ExecutionContext):
    def _after_save(p: str, e: Exception):
        if e is not None:
            ctx.show_critical_dialog(f"failed to save file: {e}", title="Error")
            ctx.logging_fatal(f"failed to save file: {e}")
            return
        ctx.show_info_dialog(f"saved: {p}", title="Info")
        ctx.logging_info(f"file saved: {p}")

    def _save_file_in_background(path_: str, param_values_):
        # Note:
        # remember we are not in the main thread now, so if we need to do the ui operation,
        # we need to use ctx.run_on_ui_thread() to submit the ui operation to the main thread,
        # if we call the ui operation directly, it may cause error
        e = None
        try:
            with open(path_, "w", encoding="utf-8") as f:
                json.dump(param_values_, f, indent=4)
        except BaseException as err:
            e = err
        # process the result in main thread
        ctx.run_on_ui_thread(_after_save, path_, e)
        # better not do this
        # _after_save(p, e)

    path = ctx.get_save_file_path()
    if not path:
        dialog = None
        return
    param_values = ctx.get_param_values()
    # Do heavy work in background, here we use threading.Thread to do this.
    # But any other non-blocking tricks will work too, for example, the thread pool,
    # it all depends on your needs.
    threading.Thread(target=_save_file_in_background, args=(path, param_values)).start()


def core_logic(a: int, b: float, w: dict, c: str):
    """
    This demo shows how to add menus and toolbar actions to the execution window.

    Attention:
        the callback function of a menu or toolbar action will be invoked in main thread!
        so do not do any long-running or block operations in the callback function, such operations may cause window lag
        or crash the program!
    """
    pass


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.always_show_selection_window = True
    gui_adapter.execution_window_config.enable_menubar_actions = True
    gui_adapter.execution_window_config.enable_toolbar_actions = True
    gui_adapter.execution_window_config.title = "Menu Demo"

    action_load = ActionItem(text="Load", callback=on_load_file, shortcut="Ctrl+O")
    action_save = ActionItem(text="Save", callback=on_save_file, shortcut="Ctrl+S")

    menus = {
        "File": {
            "Load": action_load,
            "Save": action_save,
        },
    }

    toolbar_actions = [action_load, action_save]

    gui_adapter.add(core_logic, menus=menus, toolbar_actions=toolbar_actions)
    gui_adapter.run()
