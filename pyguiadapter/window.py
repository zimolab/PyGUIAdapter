import dataclasses
from typing import Tuple, Dict, List, Optional, Union, Sequence

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QAction
from qtpy.QtWidgets import QMainWindow, QWidget, QToolBar, QMenu

from . import utils
from .action import ActionConfig, Separator, MenuConfig
from .toolbar import ToolBarConfig


@dataclasses.dataclass
class BaseWindowConfig(object):
    title: str = ""
    icon: utils.IconType = None
    size: Union[Tuple[int, int], QSize] = (800, 600)
    position: Optional[Tuple[int, int]] = None
    always_on_top: bool = False
    font_family: Union[str, Sequence[str], None] = None
    font_size: Optional[int] = None
    stylesheet: Optional[str] = None


# noinspection PyMethodMayBeStatic
class WindowStateListener(object):
    def on_create(self, window: "BaseWindow"):
        pass

    def on_close(self, window: "BaseWindow") -> bool:
        return True

    def on_destroy(self, window: "BaseWindow"):
        pass

    def on_hide(self, window: "BaseWindow"):
        pass

    def on_show(self, window: "BaseWindow"):
        pass


class BaseWindow(QMainWindow):
    def __init__(
        self,
        parent: Optional[QWidget],
        config: BaseWindowConfig,
        listener: Optional[WindowStateListener] = None,
        toolbar: Optional[ToolBarConfig] = None,
        menus: Optional[List[Union[MenuConfig, Separator]]] = None,
    ):
        super().__init__(parent)

        self._config: BaseWindowConfig = config
        self._toolbar: Optional[ToolBarConfig] = toolbar
        if menus:
            menus = menus.copy()
        self._menus: Optional[List[Union[MenuConfig, Separator]]] = menus
        self._listener: WindowStateListener = listener

        self._actions: Dict[int, QAction] = {}

        self.apply_configs()
        self._setup_toolbar()
        self._setup_menus()
        self._on_create()

    # noinspection PyMethodOverriding
    def closeEvent(self, event):
        if not self._on_close():
            event.ignore()
            return
        self._on_cleanup()
        event.accept()
        self._on_destroy()

    # noinspection PyPep8Naming
    def showEvent(self, event):
        self._on_show()
        super().showEvent(event)

    # noinspection PyMethodOverriding
    def hideEvent(self, event):
        self._on_hide()
        super().hideEvent(event)

    def apply_configs(self):
        if self._config is None:
            return

        # set window title
        title = self._config.title or ""
        self.setWindowTitle(title)

        # set window icon
        if self._config.icon:
            self.setWindowIcon(utils.get_icon(self._config.icon))

        # set window size
        size = utils.get_size(self._config.size)
        if size:
            self.resize(size)

        # set window position
        if self._config.position:
            assert len(self._config.position) == 2
            self.move(*self._config.position)

        font = self.font()
        font_size = self._config.font_size
        if font_size and font_size > 0:
            font.setPointSize(font_size)
        font_family = self._config.font_family
        if not font_family:
            pass
        elif isinstance(font_family, str):
            font.setFamily(font_family)
        elif isinstance(font_family, Sequence):
            font = self.font()
            font.setFamilies(font_family)
        else:
            raise TypeError(f"invalid font_family type: {type(font_family)}")
        self.setFont(font)

        if self._config.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # apply stylesheet
        if self._config.stylesheet:
            self.setStyleSheet(self._config.stylesheet)

    def _setup_toolbar(self):
        # create toolbar (if toolbar config provided)
        if self._toolbar:
            self._create_toolbar(toolbar_config=self._toolbar)

    def _setup_menus(self):
        # create menu (if menu config provided)
        if self._menus:
            self._create_menus(menus=self._menus)

    def _create_toolbar(self, toolbar_config: ToolBarConfig):
        toolbar = QToolBar(self)
        toolbar.setMovable(toolbar_config.moveable)
        toolbar.setFloatable(toolbar_config.floatable)

        size = utils.get_size(toolbar_config.icon_size)
        if size:
            toolbar.setIconSize(size)

        if toolbar_config.allowed_areas:
            toolbar.setAllowedAreas(toolbar_config.allowed_areas)

        if toolbar_config.button_style is not None:
            toolbar.setToolButtonStyle(toolbar_config.button_style)

        if toolbar_config.actions:
            self._add_toolbar_actions(toolbar=toolbar, actions=toolbar_config.actions)

        toolbar_area = toolbar_config.initial_area
        if toolbar_area is None:
            # noinspection PyUnresolvedReferences
            toolbar_area = Qt.TopToolBarArea
        self.addToolBar(toolbar_area, toolbar)
        self._toolbar = toolbar

    def _add_toolbar_actions(
        self, toolbar: QToolBar, actions: List[Union[ActionConfig, Separator]]
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

    # noinspection PyArgumentList
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

        def _on_triggered():
            if action_config.on_triggered is not None:
                action_config.on_triggered(self, action)

        def _toggled():
            if action_config.on_toggled is not None:
                action_config.on_toggled(self, action)

        # noinspection PyUnresolvedReferences
        action.triggered.connect(_on_triggered)
        # noinspection PyUnresolvedReferences
        action.toggled.connect(_toggled)

        self._actions[action_config_id] = action
        return action

    def _on_create(self):
        if not self._listener:
            return
        self._listener.on_create(self)

    def _on_close(self) -> bool:
        if not self._listener:
            should_close = True
        else:
            should_close = self._listener.on_close(self)
        return should_close

    def _on_destroy(self):
        if not self._listener:
            return
        self._listener.on_destroy(self)

    def _on_hide(self):
        if not self._listener:
            return
        self._listener.on_hide(self)

    def _on_show(self):
        if not self._listener:
            return
        self._listener.on_show(self)

    def _on_cleanup(self):
        self._clear_actions()

    def _clear_actions(self):
        for action in self._actions.values():
            self.removeAction(action)
            action.deleteLater()
        self._actions.clear()
