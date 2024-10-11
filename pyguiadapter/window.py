import dataclasses
import warnings
from abc import abstractmethod
from concurrent.futures import Future
from typing import Tuple, Dict, List, Optional, Union, Sequence, Callable

from qtpy.QtCore import QSize, Qt, Signal
from qtpy.QtGui import QAction, QIcon, QActionGroup, QClipboard
from qtpy.QtWidgets import QMainWindow, QWidget, QToolBar, QMenu, QApplication

from .action import ActionConfig, Separator
from .constants.clipboard import (
    CLIPBOARD_OWNS_CLIPBOARD,
    CLIPBOARD_SET_TEXT,
    CLIPBOARD_GET_TEXT,
    CLIPBOARD_OWNS_SELECTION,
    CLIPBOARD_SUPPORTS_SELECTION,
    CLIPBOARD_GET_SELECTION_TEXT,
    CLIPBOARD_SET_SELECTION_TEXT,
)
from .constants.font import FONT_FAMILY, FONT_MEDIUM
from .exceptions import ClipboardOperationError
from .menu import MenuConfig
from .toast import ToastWidget, ToastConfig
from .toolbar import ToolBarConfig
from .utils import IconType, get_icon, get_size


@dataclasses.dataclass(frozen=True)
class BaseWindowConfig(object):
    title: str = ""
    icon: IconType = None
    size: Union[Tuple[int, int], QSize] = (800, 600)
    position: Optional[Tuple[int, int]] = None
    always_on_top: bool = False
    font_family: Union[str, Sequence[str], None] = FONT_FAMILY
    font_size: Optional[int] = FONT_MEDIUM
    stylesheet: Optional[str] = None


# noinspection PyMethodMayBeStatic
class BaseWindowStateListener(object):
    def on_create(self, window: "BaseWindow"):
        pass

    # noinspection PyUnusedLocal
    def on_close(self, window: "BaseWindow") -> bool:
        return True

    def on_destroy(self, window: "BaseWindow"):
        pass

    def on_hide(self, window: "BaseWindow"):
        pass

    def on_show(self, window: "BaseWindow"):
        pass


class SimpleWindowStateListener(BaseWindowStateListener):
    def __init__(
        self,
        on_create: Callable[["BaseWindow"], None] = None,
        on_show: Callable[["BaseWindow"], None] = None,
        on_hide: Callable[["BaseWindow"], None] = None,
        on_close: Callable[["BaseWindow"], bool] = None,
        on_destroy: Callable[["BaseWindow"], None] = None,
    ):
        self._on_create_callback = on_create
        self._on_show_callback = on_show
        self._on_hide_callback = on_hide
        self._on_close_callback = on_close
        self._on_destroy_callback = on_destroy

    def on_create(self, window: "BaseWindow"):
        if self._on_create_callback:
            return self._on_create_callback(window)
        super().on_create(window)

    def on_close(self, window: "BaseWindow") -> bool:
        if self._on_close_callback:
            return self._on_close_callback(window)
        return super().on_close(window)

    def on_destroy(self, window: "BaseWindow"):
        if self._on_destroy_callback:
            return self._on_destroy_callback(window)
        super().on_destroy(window)

    def on_hide(self, window: "BaseWindow"):
        if self._on_hide_callback:
            return self._on_hide_callback(window)
        super().on_hide(window)

    def on_show(self, window: "BaseWindow"):
        if self._on_show_callback:
            return self._on_show_callback(window)
        super().on_show(window)


class BaseWindow(QMainWindow):
    sig_clear_toasts = Signal()

    def __init__(
        self,
        parent: Optional[QWidget],
        config: BaseWindowConfig,
        listener: Optional[BaseWindowStateListener] = None,
        toolbar: Optional[ToolBarConfig] = None,
        menus: Optional[List[Union[MenuConfig, Separator]]] = None,
    ):
        super().__init__(parent)

        self._config: BaseWindowConfig = config
        self._toolbar: Optional[ToolBarConfig] = toolbar
        if menus:
            menus = [*menus]
        self._menus: Optional[List[Union[MenuConfig, Separator]]] = menus
        self._listener: BaseWindowStateListener = listener
        self._actions: Dict[int, QAction] = {}

        self._create_ui()
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

        self.set_title(self._config.title)
        self.set_icon(self._config.icon)
        self.set_size(self._config.size)
        self.set_position(self._config.position)
        self.set_always_on_top(self._config.always_on_top)
        self.set_font(self._config.font_family, self._config.font_size)
        self.set_stylesheet(self._config.stylesheet)

    def set_title(self, title: str):
        title = title or ""
        self.setWindowTitle(title)

    def get_title(self) -> str:
        return self.windowTitle()

    def set_icon(self, icon: IconType):
        icon = get_icon(icon) or QIcon()
        self.setWindowIcon(icon)

    def set_always_on_top(self, enabled: bool):
        if enabled:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

    def is_always_on_top(self) -> bool:
        return bool(self.windowFlags() & Qt.WindowStaysOnTopHint)

    def set_size(self, size: Union[Tuple[int, int], QSize]):
        size = get_size(size)
        if not size:
            raise ValueError(f"invalid size: {size}")
        self.resize(size)

    def get_size(self) -> Tuple[int, int]:
        size = self.size()
        return size.width(), size.height()

    def set_position(self, position: Optional[Tuple[int, int]]):
        if not position:
            return
        if len(position) != 2:
            raise ValueError(f"invalid position: {position}")
        self.move(*position)

    def get_position(self) -> Tuple[int, int]:
        pos = self.pos()
        return pos.x(), pos.y()

    def set_font(self, font_family: Union[str, Sequence[str]], font_size: int):
        font = self.font()
        if not font_family:
            pass
        elif isinstance(font_family, str):
            font.setFamily(font_family)
        elif isinstance(font_family, Sequence):
            font = self.font()
            font.setFamilies(font_family)
        else:
            raise TypeError(f"invalid font_family type: {type(font_family)}")
        if font_size and font_size > 0:
            font.setPixelSize(font_size)
            # font.setPointSize(font_size)
        self.setFont(font)

    def get_font_size(self) -> int:
        return self.font().pointSize()

    def get_font_family(self) -> str:
        return self.font().family()

    def get_font_families(self) -> Sequence[str]:
        return self.font().families()

    def set_stylesheet(self, stylesheet: Optional[str]):
        if not stylesheet:
            return
        self.setStyleSheet(stylesheet)

    def get_stylesheet(self) -> str:
        return self.styleSheet()

    def find_action(self, action_config: ActionConfig) -> Optional[QAction]:
        c_id = id(action_config)
        return self._actions.get(c_id, None)

    def set_action_state(self, action_config: ActionConfig, checked: bool) -> bool:
        action = self.find_action(action_config)
        if action is None:
            warnings.warn(f"action not found: {action_config}")
            return False
        if not action.isCheckable():
            warnings.warn(f"action is not checkable: {action_config}")
            return False
        action.setChecked(checked)
        return True

    def toggle_action_state(self, action_config: ActionConfig) -> bool:
        action = self.find_action(action_config)
        if action is None:
            warnings.warn(f"action not found: {action_config}")
            return False
        if not action.isCheckable():
            warnings.warn(f"action is not checkable: {action_config}")
            return False
        action.toggle()

    def query_action_state(self, action_config: ActionConfig) -> Optional[bool]:
        action = self.find_action(action_config)
        if action is None:
            return None
        return action.isChecked()

    @staticmethod
    def get_clipboard_text() -> str:
        clipboard = QApplication.clipboard()
        return clipboard.text()

    @staticmethod
    def set_clipboard_text(text: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    @staticmethod
    def get_selection_text() -> Optional[str]:
        clipboard = QApplication.clipboard()
        return clipboard.text(mode=QClipboard.Selection)

    @staticmethod
    def set_selection_text(text: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(text, mode=QClipboard.Selection)

    @staticmethod
    def supports_selection() -> bool:
        return QApplication.clipboard().supportsSelection()

    @staticmethod
    def owns_clipboard() -> bool:
        return QApplication.clipboard().ownsClipboard()

    @staticmethod
    def owns_selection() -> bool:
        return QApplication.clipboard().ownsSelection()

    def on_clipboard_operation(self, future: Future, operation: int, data: object):
        if operation == CLIPBOARD_GET_TEXT:
            text = self.get_clipboard_text()
            future.set_result(text)
            return

        if operation == CLIPBOARD_SET_TEXT:
            if not isinstance(data, str):
                raise ClipboardOperationError(
                    operation, f"data must be a str, got {data}"
                )
            self.set_clipboard_text(data)
            future.set_result(None)
            return

        if operation == CLIPBOARD_GET_SELECTION_TEXT:
            text = self.get_selection_text()
            future.set_result(text)
            return

        if operation == CLIPBOARD_SET_SELECTION_TEXT:
            if not isinstance(data, str):
                raise ClipboardOperationError(
                    operation, f"data must be a str, got {data}"
                )
            self.set_selection_text(data)
            future.set_result(None)
            return

        if operation == CLIPBOARD_SUPPORTS_SELECTION:
            future.set_result(self.supports_selection())
            return

        if operation == CLIPBOARD_OWNS_CLIPBOARD:
            future.set_result(self.owns_clipboard())
            return

        if operation == CLIPBOARD_OWNS_SELECTION:
            future.set_result(self.owns_selection())
            return

        raise ClipboardOperationError(
            operation, f"invalid clipboard operation: {operation}"
        )

    def show_toast(
        self,
        message: str,
        duration: int = 2000,
        config: Optional[ToastConfig] = None,
        clear: bool = False,
    ):
        if clear:
            self.clear_toasts()
        toast = ToastWidget(self, message, duration, config=config)
        toast.sig_toast_finished.connect(self._on_toast_finished)
        # noinspection PyUnresolvedReferences
        self.sig_clear_toasts.connect(toast.finish)
        toast.start()

    def clear_toasts(self):
        # noinspection PyUnresolvedReferences
        self.sig_clear_toasts.emit()

    def _on_toast_finished(self):
        w = self.sender()
        if not isinstance(w, ToastWidget):
            return
        # noinspection PyUnresolvedReferences
        self.sig_clear_toasts.disconnect(w.finish)
        w.sig_toast_finished.disconnect(self._on_toast_finished)
        w.deleteLater()
        del w

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

        size = get_size(toolbar_config.icon_size)
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
        exclusive_group = None
        if menu_config.exclusive:
            exclusive_group = QActionGroup(self)
            exclusive_group.setExclusive(True)

        for action_config in menu_config.actions:
            if isinstance(action_config, Separator):
                menu.addSeparator()
                continue
            if isinstance(action_config, ActionConfig):
                action = self._create_action(action_config)
                if action.isCheckable() and exclusive_group:
                    exclusive_group.addAction(action)
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
            action.setIcon(get_icon(action_config.icon))
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
        self.clear_toasts()
        self._clear_actions()

    def _clear_actions(self):
        for action in self._actions.values():
            self.removeAction(action)
            action.deleteLater()
        self._actions.clear()
        del self._actions

    @abstractmethod
    def _create_ui(self):
        pass
