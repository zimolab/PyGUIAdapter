from __future__ import annotations

import dataclasses
from typing import List, Tuple

from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtCore import QSize, Qt

from .action import ActionConfig, Separator


@dataclasses.dataclass
class MenuConfig(object):
    title: str
    actions: List[ActionConfig | Separator | MenuConfig]
    icon: str | QIcon | QPixmap | None = None
    separators_collapsible: bool = True
    tear_off_enabled: bool = True


@dataclasses.dataclass
class ToolbarConfig(object):
    actions: List[ActionConfig | Separator]
    moveable: bool = True
    floatable: bool = True
    horizontal: bool = True
    icon_size: Tuple[int, int] | QSize | None = None
    initial_area: Qt.ToolBarArea | None = None
    allowed_areas: Qt.ToolBarAreas | None = None
    button_style: Qt.ToolButtonStyle | None = None
