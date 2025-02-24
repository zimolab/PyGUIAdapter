import dataclasses
from typing import Tuple, Optional, Union

from qtpy.QtCore import Qt

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
    item_editor_key_column_alignment: Union[Qt.AlignmentFlag, int, None] = None
    item_editor_value_column_alignment: Union[Qt.AlignmentFlag, int, None] = None
    double_click_to_edit: bool = True
    wrap_movement: bool = False
    duplicate_items_warning_message: Optional[str] = None
    no_selection_warning_message: Optional[str] = None
    multiple_selection_warning_message: Optional[str] = None
    no_items_warning_message: Optional[str] = None
    remove_confirm_message: Optional[str] = None
    clear_confirm_message: Optional[str] = None
    add_button_text: str = "Add"
    edit_button_text: str = "Edit"
    remove_button_text: str = "Remove"
    clear_button_text: str = "Clear"
    move_up_button_text: str = "Move Up"
    move_down_button_text: str = "Move Down"
