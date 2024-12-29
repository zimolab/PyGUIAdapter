import dataclasses
from typing import Tuple, Optional

WARNING_DIALOG_TITLE = "Warning"
CONFIRM_DIALOG_TITLE = "Confirm"


@dataclasses.dataclass
class CommonEditorConfig(object):
    window_title: str = "Object Editor"
    window_size: tuple = (800, 600)
    standard_buttons: bool = True
    warning_dialog_title: str = WARNING_DIALOG_TITLE
    confirm_dialog_title: str = CONFIRM_DIALOG_TITLE
    center_container_title: str = ""
    item_editor_title: str = ""
    item_editor_size: Tuple[int, int] = (500, 600)
    item_editor_center_container_title: str = ""
    double_click_to_edit: bool = True
    wrap_movement: bool = False
    duplicate_items_warning_message: Optional[str] = None
    no_selection_warning_message: Optional[str] = None
    multiple_selection_warning_message: Optional[str] = None
    no_items_warning_message: Optional[str] = None
    remove_confirm_message: Optional[str] = None
    clear_confirm_message: Optional[str] = None
