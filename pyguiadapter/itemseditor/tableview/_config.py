import dataclasses
from typing import Union, Literal, Optional, Dict

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHeaderView

ResizeMode = QHeaderView.ResizeMode


@dataclasses.dataclass
class TableViewConfig(object):
    alternating_row_colors: bool = True
    show_horizontal_header: bool = True
    show_vertical_header: bool = True
    show_grid: bool = True
    continuous_selection: bool = True
    item_text_alignment: Union[int, Qt.AlignmentFlag, None] = None
    item_data_as_tooltip: bool = False
    item_data_as_status_tip: bool = False
    row_data_type: Literal["tuple", "list", "dict"] = "tuple"
    ignore_unknown_columns: bool = False
    stretch_last_section: bool = True
    resize_rows_to_contents: bool = True
    column_widths: Optional[Dict[int, int]] = None
    horizontal_resize_modes: Union[Dict[int, ResizeMode], ResizeMode, None] = None
    vertical_resize_modes: Union[Dict[int, ResizeMode], ResizeMode, None] = None
