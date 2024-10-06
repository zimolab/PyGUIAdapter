import enum
import json

from qtpy.QtWidgets import QAction
from typing import Any, Dict

from pyguiadapter.action import ActionConfig
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.extend_types import color_t, json_obj_t
from pyguiadapter.menu import MenuConfig
from pyguiadapter.utils import PyLiteralType, messagebox, filedialog, io
from pyguiadapter.windows.fnexec import FnExecuteWindow


def on_action_save_params(window: FnExecuteWindow, action: QAction):
    # check if the function is executing
    if window.is_function_executing():
        messagebox.show_warning_message(window, "Function is executing")
        return
    # get current parameter values from widgets
    # some values may be invalid so do not forget to catch errors
    try:
        params: Dict[str, Any] = window.get_parameter_values()
    except ParameterError as e:
        # if the error is a ParameterError, we can let the window handle it
        window.process_parameter_error(e)
        return
    except Exception as e:
        # if the error is not a ParameterError, we need handle it by ourselves properly
        # here we just show the exception message with a message box
        messagebox.show_exception_messagebox(
            window, e, message="Unable to get the parameters: {}"
        )
        return
    # now we get current parameter values, we can save them to a location like a file in disk.
    # So the next topic is how to serialize them properly? It is not a simple problem especially considering that we
    # need to load them back later.
    # If the all the parameters are basic or simple types, json is a good choice. However, considering the current case
    # we are working on, we have to deal with some complex types, like:
    #   arg5: list
    #   arg6: dict
    #   arg7: tuple
    #   arg8: set
    #   arg10: json_obj_t
    #   arg11: WeekDay
    #   arg12: PyLiteralType
    # In order to save them in json files and read them back accurately, a lot of efforts need to be made in
    # serialization and deserialization logic.
    # As a demo, we decide not to do this job so precisely here. In a real life project, please be careful.

    # let user select a file to save the parameters
    save_path = filedialog.get_save_file(
        window, title="Save Parameters", start_dir="./", filters="JSON files(*.json)"
    )
    if not save_path:
        return

    # process arg8 which is a set
    if "arg8" in params:
        arg8 = params["arg8"]
        params["arg8"] = set(arg8)

    # process arg11 which is an enum of type WeekDay
    if "arg11" in params:
        arg11 = params["arg11"]
        params["arg11"] = arg11.value

    try:
        # process arg12 which is a PyLiteralType
        if "arg12" in params:
            arg12 = params["arg12"]
            params["arg12"] = json.dumps(arg12, ensure_ascii=False)
        serialized_params = json.dumps(params, ensure_ascii=False)
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to serialize the parameters: "
        )
        return

    try:
        io.write_text_file(save_path, serialized_params)
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to save the parameters: "
        )
        return
    messagebox.show_info_message(window, "Parameters saved to {}".format(save_path))


def on_action_load_params(window: FnExecuteWindow, action: QAction):
    # check if the function is executing
    if window.is_function_executing():
        messagebox.show_warning_message(window, "Function is executing")
        return
    load_path = filedialog.get_open_file(
        window, title="Load Parameters", start_dir="./", filters="JSON files(*.json)"
    )
    if not load_path:
        return
    try:
        content = io.read_text_file(load_path)
        params = json.loads(content)
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to load the parameters: "
        )
        return
    if not isinstance(params, dict):
        messagebox.show_critical_message(window, message="Invalid parameters format!")
        return

    # process some special parameters with complex types
    try:
        # arg7: tuple
        if "arg7" in params:
            arg5 = params["arg7"]
            params["arg7"] = tuple(arg5)
        # arg8: set
        if "arg8" in params:
            arg8 = params["arg8"]
            params["arg8"] = set(arg8)
        # arg9: color_t (which is actually a tuple of 4 elements in our case)
        if "arg9" in params:
            arg9 = params["arg9"]
            params["arg9"] = tuple(arg9)
        # arg11: WeekDay
        if "arg11" in params:
            arg11 = params["arg11"]
            params["arg11"] = WeekDay(arg11)
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Invalid parameters format: "
        )
        return

    try:
        window.set_parameter_values(params)
    except ParameterError as e:
        window.process_parameter_error(e)
        return
    except Exception as e:
        messagebox.show_exception_messagebox(
            window, e, message="Unable to set the parameters: "
        )
        return


action_save_params = ActionConfig(
    text="Save Parameters",
    icon="fa.save",
    shortcut="Ctrl+S",
    on_triggered=on_action_save_params,
)

action_load_params = ActionConfig(
    text="Load Parameters",
    icon="fa.folder-open",
    shortcut="Ctrl+L",
    on_triggered=on_action_load_params,
)


class WeekDay(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


def load_save_example(
    arg1: int,
    arg2: str,
    arg3: bool,
    arg4: float,
    arg5: list,
    arg6: dict,
    arg7: tuple,
    arg8: set,
    arg9: color_t,
    arg10: json_obj_t,
    arg11: WeekDay,
    ar12: PyLiteralType,
):
    pass


if __name__ == "__main__":
    file_menu = MenuConfig(
        title="File",
        actions=[action_save_params, action_load_params],
    )
    adapter = GUIAdapter()
    adapter.add(load_save_example, window_menus=[file_menu])
    adapter.run()
