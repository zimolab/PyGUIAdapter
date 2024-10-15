import json

from typing import Dict, Any

from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.extend_types import color_t
from pyguiadapter.menu import Menu
from pyguiadapter.utils import messagebox, filedialog
from pyguiadapter.windows.fnexec import FnExecuteWindow


def simple_load_save_example(
    arg1: int,
    arg2: float,
    arg3: bool,
    arg4: str,
    arg5: color_t,
):
    """
    This example shows how to save current parameter values to a json file and load a parameter values from a json file.
    @param arg1:
    @param arg2:
    @param arg3:
    @param arg4:
    @param arg5:
    @return:
    """
    uprint("arg1=", arg1)
    uprint("arg2=", arg2)
    uprint("arg3=", arg3)
    uprint("arg4=", arg4)
    uprint("arg5=", arg5)


def on_save_params(window: FnExecuteWindow, _: Action):
    # Step 1: obtain current parameter values from widgets
    #
    # if the current input in the widgets of some parameter is invalid, the get_parameter_values() method may raise a
    # exception. A good practice is to catch the exception and handle it properly:
    #  - for ParameterError, the FnExecuteWindow has a builtin logic to deal with it, so just call the
    #  process_parameter_error() method and let the window do the job.
    #
    #  - for other exceptions, we need handle it by ourselves. Here we choose to show the exception message with a
    #  message box to the user.

    try:
        params: Dict[str, Any] = window.get_parameter_values()
    except ParameterError as e:
        window.process_parameter_error(e)
        return
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to get the parameters: "
        )
        return

    # Step2: serialize the parameter values and save them to a json file
    #
    # In this example, because we don't use any complex types, we can use simply json.dump() to do the serialization.
    # However, If your function contains parameters of complex types, such as list, tuple, set, dict, enum, then
    # serialization and deserialization must be considered very carefully.
    #
    save_file = filedialog.get_save_file(
        window, "Save Parameters", filters="JSON files(*.json)"
    )
    if not save_file:
        return
    try:
        with open(save_file, "w") as f:
            json.dump(params, f)
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to save the parameters: "
        )
    else:
        messagebox.show_info_message(window, "Parameters have been saved!")


def on_load_params(window: FnExecuteWindow, _: Action):
    # Step 1: load the parameter values from a json file
    file = filedialog.get_open_file(
        window, "Load Parameters", filters="JSON files(*.json)"
    )
    if not file:
        return
    try:
        with open(file, "r") as f:
            params: Dict[str, Any] = json.load(f)
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to load the parameters: "
        )
        return
    if not isinstance(params, dict):
        messagebox.show_critical_message(window, message="Invalid parameters format!")
        return

    # Step2: set the parameter values to the widgets
    try:
        window.set_parameter_values(params)
    except ParameterError as e:
        window.process_parameter_error(e)
        return
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to set the parameters: "
        )
    else:
        messagebox.show_info_message(window, "Parameters have been loaded!")


if __name__ == "__main__":
    action_save_params = Action(
        text="Save Parameters",
        icon="fa.save",
        shortcut="Ctrl+S",
        on_triggered=on_save_params,
    )

    action_load_params = Action(
        text="Load Parameters",
        icon="fa.folder-open",
        shortcut="Ctrl+L",
        on_triggered=on_load_params,
    )

    menu = Menu(
        title="File",
        actions=[action_save_params, action_load_params],
    )

    adapter = GUIAdapter()
    adapter.add(simple_load_save_example, window_menus=[menu])
    adapter.run()
