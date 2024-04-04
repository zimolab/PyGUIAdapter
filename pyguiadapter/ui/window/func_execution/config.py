import dataclasses
import enum
from typing import Optional, Tuple

from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.styles import (
    DEFAULT_OUTPUT_FONT_FAMILY,
    DEFAULT_OUTPUT_FONT_SIZE,
    DEFAULT_OUTPUT_BG_COLOR,
    DEFAULT_OUTPUT_TEXT_COLOR,
    DEFAULT_DOCUMENT_FONT_FAMILY,
    DEFAULT_DOCUMENT_FONT_SIZE,
    DEFAULT_DOCUMENT_BG_COLOR,
    DEFAULT_DOCUMENT_TEXT_COLOR,
)
from .constants import (
    FUNC_RESULT_MSG,
    FUNC_RESULT_DIALOG_TITLE,
    FUNC_START_MSG,
    FUNC_FINISH_MSG,
    FUNC_ERROR_DIALOG_TITLE,
    FUNC_ERROR_MSG,
)


class DockWidgetState(enum.Enum):
    Shown = 0
    Hidden = 1
    Floating = 3


@dataclasses.dataclass
class DockConfig(object):
    title: Optional[str] = None
    state: DockWidgetState = DockWidgetState.Shown
    floating_size: Tuple[int, int] = dataclasses.field(default=(400, 600))


@dataclasses.dataclass
class ExecutionWindowConfig(WindowConfig):

    tabify_docks: bool = True
    output_dock_config: DockConfig = DockConfig()
    document_dock_config: DockConfig = DockConfig()

    autoclear_output: bool = True

    param_groupbox_title: Optional[str] = None
    autoclear_checkbox_text: Optional[str] = None
    execute_button_text: Optional[str] = None
    clear_button_text: Optional[str] = None
    cancel_button_text: Optional[str] = None

    output_font_family: str = DEFAULT_OUTPUT_FONT_FAMILY
    output_font_size: int = DEFAULT_OUTPUT_FONT_SIZE
    output_bg_color: str = DEFAULT_OUTPUT_BG_COLOR
    output_text_color: str = DEFAULT_OUTPUT_TEXT_COLOR

    document_font_family: str = DEFAULT_DOCUMENT_FONT_FAMILY
    document_font_size: int = DEFAULT_DOCUMENT_FONT_SIZE
    document_bg_color: str = DEFAULT_DOCUMENT_BG_COLOR
    document_text_color: str = DEFAULT_DOCUMENT_TEXT_COLOR

    print_func_result: bool = True
    func_result_msg: str = FUNC_RESULT_MSG
    show_func_result_dialog: bool = True
    func_result_dialog_title: str = FUNC_RESULT_DIALOG_TITLE
    func_result_dialog_msg: str = FUNC_RESULT_MSG

    print_func_start_msg: bool = True
    func_start_msg: str = FUNC_START_MSG

    print_func_finish_msg: bool = True
    func_finish_msg: str = FUNC_FINISH_MSG

    show_func_error_dialog: bool = True
    func_error_dialog_title: str = FUNC_ERROR_DIALOG_TITLE
    func_error_dialog_msg: str = FUNC_ERROR_MSG
    print_func_error: bool = True
    func_error_msg: str = FUNC_ERROR_MSG

    timestamp: bool = True
    timestamp_pattern: str = "%Y-%m-%d %H:%M:%S"

    enable_menubar_actions: bool = False
    enable_toolbar_actions: bool = False
