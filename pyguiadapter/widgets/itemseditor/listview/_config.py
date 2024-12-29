import dataclasses
from typing import Union

from qtpy.QtCore import Qt


@dataclasses.dataclass
class ListViewConfig(object):
    item_text_alignment: Union[int, Qt.AlignmentFlag, None] = None
    alternating_row_colors: bool = False
    item_editable: bool = True
    item_data_as_tooltip: bool = False
    item_data_as_status_tip: bool = False
