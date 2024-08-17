from __future__ import annotations

import dataclasses
from typing import Callable

from qtpy.QtWidgets import QAction

from . import window, utils


@dataclasses.dataclass
class ActionConfig(object):
    text: str
    on_trigger: Callable[[window.BaseWindow, QAction], None] | None = None
    on_toggle: Callable[[window.BaseWindow, QAction], None] | None = None
    icon: utils.IconType = None
    icon_text: str | None = None
    auto_repeat: bool = False
    enabled: bool = True
    checkable: bool = False
    checked: bool = False
    shortcut: str | None = None
    shortcut_context: QAction.ShortcutContext | None = None
    tooltip: str | None = None
    whats_this: str | None = None
    status_tip: str | None = None
    priority: QAction.Priority | None = None
    menu_role: QAction.MenuRole | None = None


@dataclasses.dataclass
class Separator(object):
    pass
