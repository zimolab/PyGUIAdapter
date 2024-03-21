from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact import upopup


def interact_with_popups(popup_type: str = "get_int"):
    """
    This demo shows how interact with user by using popups

    :param popup_type: <b>Select the popup type to see what it looks like!</b>
    :return:
    """
    match popup_type:
        case "get_int":
            result = upopup.get_int("Enter an integer:", "Input", 100)
            upopup.information(f"You entered: {result}")
        case "get_float":
            result = upopup.get_float("Enter a float:", "Input", 100.0)
            upopup.information(f"You entered: {result}")
        case "get_text":
            result = upopup.get_text("Enter a string:", "Input")
            upopup.information(f"You entered: {result}")
        case "get_multiline_text":
            result = upopup.get_multiline_text("Enter text:", "Input")
            upopup.information(f"You entered: {result}")
        case "get_item":
            result = upopup.get_item(
                ["Item 1", "Item 2", "Item 3"], "Select an item:", "Select"
            )
            upopup.information(f"You selected: {result}")
        case "get_open_file_path":
            result = upopup.get_open_file_path("Select a file:", "./")
            upopup.information(f"You selected: {result}")
        case "get_open_file_paths":
            result = upopup.get_open_file_paths("Select files:", "./")
            upopup.information(f"You selected: {result}")
        case "get_save_file_path":
            result = upopup.get_save_file_path("Save to:", "./")
            upopup.information(f"You selected: {result}")
        case "get_directory_path":
            result = upopup.get_directory_path("Select a directory:", "./")
            upopup.information(f"You selected: {result}")
        case "information":
            upopup.information("this is information popup")
        case "warning":
            upopup.warning("this is warning popup")
        case "critical":
            upopup.critical("this is critical popup")
        case "question":
            result = upopup.question("this is question popup")
            upopup.information(f"You selected: {result}")
        case _:
            upopup.critical("Unknown popup type!")


gui_adapter = GUIAdapter()
gui_adapter.execution_window_config.show_function_result_dialog = False
gui_adapter.add(
    interact_with_popups,
    widgets_config={
        "popup_type": {
            "type": "ComboBox",
            "items": [
                "get_int",
                "get_float",
                "get_text",
                "get_multiline_text",
                "get_item",
                "get_open_file_path",
                "get_open_file_paths",
                "get_save_file_path",
                "get_directory_path",
                "information",
                "warning",
                "critical",
                "question",
            ],
        }
    },
)
gui_adapter.run()
