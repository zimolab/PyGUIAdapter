from __future__ import annotations

import dataclasses
from typing import Callable, Tuple, Dict, List

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QAction
from qtpy.QtWidgets import QMainWindow, QWidget, QToolBar, QMenu

from . import utils
from .action import ActionConfig, Separator
from .menu import MenuConfig, ToolbarConfig

DEFAULT_WINDOW_SIZE = (800, 600)


GLOBAL_STYLESHEET = "*{font-size: 10pt}"


@dataclasses.dataclass
class BaseWindowConfig(object):
    title: str = ""
    icon: utils.IconType = None
    size: Tuple[int, int] | QSize = DEFAULT_WINDOW_SIZE
    toolbar: ToolbarConfig | None = None
    menus: List[MenuConfig | Separator] | None = None
    on_create: Callable[["BaseWindow"], None] | None = None
    on_close: Callable[["BaseWindow"], bool] | None = None
    on_destroy: Callable[["BaseWindow"], None] | None = None
    on_hide: Callable[["BaseWindow"], None] | None = None
    on_show: Callable[["BaseWindow"], None] | None = None
    stylesheet: str | None = GLOBAL_STYLESHEET


class BaseWindow(QMainWindow):
    def __init__(self, parent: QWidget | None, config: BaseWindowConfig):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self._config: BaseWindowConfig = config
        self._actions: Dict[int, QAction] = {}
        self._update_ui()

        self._on_create()

    def closeEvent(self, event):
        if not self._on_close():
            event.ignore()
            return
        self._on_cleanup()
        event.accept()
        self._on_destroy()

    def showEvent(self, event):
        self._on_show()
        super().showEvent(event)

    def hideEvent(self, event):
        self._on_hide()
        super().hideEvent(event)

    def _update_ui(self):
        if self._config is None:
            return

        # set window title
        title = self._config.title or ""
        self.setWindowTitle(title)

        # set window icon
        if self._config.icon:
            self.setWindowIcon(utils.get_icon(self._config.icon))

        # set window size
        if self._config.size:
            if isinstance(self._config.size, tuple):
                size = QSize(self._config.size[0], self._config.size[1])
                self.resize(size)
            elif isinstance(self._config.size, QSize):
                self.resize(self._config.size)
            else:
                raise ValueError(f"invalid size type: {type(self._config.size)}")

        # create toolbar (if toolbar config provided)
        if self._config.toolbar:
            self._create_toolbar(toolbar_config=self._config.toolbar)

        # create menu (if menu config provided)
        if self._config.menus:
            self._create_menus(menus=self._config.menus)

        # apply stylesheet
        if self._config.stylesheet:
            self.setStyleSheet(self._config.stylesheet)

    def _create_toolbar(self, toolbar_config: ToolbarConfig):
        toolbar = QToolBar(self)
        toolbar.setMovable(toolbar_config.moveable)
        toolbar.setFloatable(toolbar_config.floatable)
        toolbar.setOrientation(
            Qt.Horizontal if toolbar_config.horizontal else Qt.Vertical
        )

        if toolbar_config.icon_size:
            size = toolbar_config.icon_size
            if isinstance(size, tuple):
                size = QSize(size[0], size[1])
            toolbar.setIconSize(size)

        if toolbar_config.allowed_areas:
            toolbar.setAllowedAreas(toolbar_config.allowed_areas)

        if toolbar_config.button_style is not None:
            toolbar.setToolButtonStyle(toolbar_config.button_style)

        if toolbar_config.actions:
            self._add_toolbar_actions(toolbar=toolbar, actions=toolbar_config.actions)

        toolbar_area = toolbar_config.initial_area
        if toolbar_area is None:
            toolbar_area = Qt.TopToolBarArea
        self.addToolBar(toolbar_area, toolbar)

    def _add_toolbar_actions(
        self, toolbar: QToolBar, actions: List[ActionConfig | Separator]
    ):
        for action_config in actions:
            if isinstance(action_config, Separator):
                toolbar.addSeparator()
                continue

            action = self._create_action(action_config)
            toolbar.addAction(action)

    def _create_menus(self, menus: List[MenuConfig]):
        menubar = self.menuBar()
        for menu_config in menus:
            if isinstance(menu_config, Separator):
                menubar.addSeparator()
                continue
            menu = self._create_menu(menu_config)
            menubar.addMenu(menu)

    def _create_menu(self, menu_config: MenuConfig) -> QMenu:
        menu = QMenu(self)
        menu.setTitle(menu_config.title)
        for action_config in menu_config.actions:
            if isinstance(action_config, Separator):
                menu.addSeparator()
                continue
            if isinstance(action_config, ActionConfig):
                action = self._create_action(action_config)
                menu.addAction(action)
            elif isinstance(action_config, MenuConfig):
                submenu = self._create_menu(action_config)
                menu.addMenu(submenu)
            else:
                raise ValueError(f"invalid action_config type: {type(action_config)}")
        return menu

    def _create_action(self, action_config: ActionConfig) -> QAction:

        action_config_id = id(action_config)
        # reuse action if already created
        if action_config_id in self._actions:
            return self._actions[action_config_id]

        action = QAction(self)
        action.setText(action_config.text)
        if action_config.icon:
            action.setIcon(utils.get_icon(action_config.icon))
        if action_config.icon_text:
            action.setIconText(action_config.icon_text)
        action.setAutoRepeat(action_config.auto_repeat)
        action.setEnabled(action_config.enabled)
        action.setCheckable(action_config.checkable)
        action.setChecked(action_config.checked)
        if action_config.shortcut:
            action.setShortcut(action_config.shortcut)
        if action_config.shortcut_context is not None:
            action.setShortcutContext(action_config.shortcut_context)
        if action_config.tooltip:
            action.setToolTip(action_config.tooltip)
        if action_config.status_tip:
            action.setStatusTip(action_config.status_tip)
        if action_config.whats_this:
            action.setWhatsThis(action_config.whats_this)
        if action_config.priority is not None:
            action.setPriority(action_config.priority)
        if action_config.menu_role is not None:
            action.setMenuRole(action_config.menu_role)

        def _on_action_trigger():
            if action_config.on_trigger is not None:
                action_config.on_trigger(self, action)

        def _on_action_toggle():
            if action_config.on_toggle is not None:
                action_config.on_toggle(self, action)

        # noinspection PyUnresolvedReferences
        action.triggered.connect(_on_action_trigger)
        # noinspection PyUnresolvedReferences
        action.toggled.connect(_on_action_toggle)

        self._actions[action_config_id] = action
        return action

    def _on_create(self):
        if self._config is None or not callable(self._config.on_create):
            return
        if self._config.on_create:
            self._config.on_create(self)

    def _on_close(self) -> bool:
        if self._config is None or not callable(self._config.on_close):
            should_close = True
        else:
            should_close = self._config.on_close(self)
        return should_close

    def _on_destroy(self):
        if self._config is None or not callable(self._config.on_destroy):
            return
        self._config.on_destroy(self)

    def _on_hide(self):
        if self._config is None or not callable(self._config.on_hide):
            return
        self._config.on_hide(self)

    def _on_show(self):
        if self._config is None or not callable(self._config.on_show):
            return
        self._config.on_show(self)

    def _on_cleanup(self):
        for action in self._actions.values():
            action.deleteLater()
        self._actions.clear()
