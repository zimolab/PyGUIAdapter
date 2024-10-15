import dataclasses
import warnings
from abc import abstractmethod
from concurrent.futures import Future
from typing import Tuple, Dict, List, Optional, Union, Sequence, Callable

from qtpy.QtCore import QSize, Qt, Signal
from qtpy.QtGui import QAction, QIcon, QActionGroup, QClipboard
from qtpy.QtWidgets import QMainWindow, QWidget, QToolBar, QMenu, QApplication

from .action import Action, Separator
from .constants.clipboard import (
    CLIPBOARD_OWNS_CLIPBOARD,
    CLIPBOARD_SET_TEXT,
    CLIPBOARD_GET_TEXT,
    CLIPBOARD_OWNS_SELECTION,
    CLIPBOARD_SUPPORTS_SELECTION,
    CLIPBOARD_GET_SELECTION_TEXT,
    CLIPBOARD_SET_SELECTION_TEXT,
)
from .exceptions import ClipboardOperationError
from .menu import MenuConfig
from .toast import ToastWidget, ToastConfig
from .toolbar import ToolBarConfig
from .utils import IconType, get_icon, get_size


@dataclasses.dataclass(frozen=True)
class BaseWindowConfig(object):
    title: str = ""
    """窗口标题"""

    icon: IconType = None
    """窗口图标"""

    size: Union[Tuple[int, int], QSize] = (800, 600)
    """窗口大小"""

    position: Optional[Tuple[int, int]] = None
    """窗口位置"""

    always_on_top: bool = False
    """窗口是否永远置顶"""

    font_family: Union[str, Sequence[str], None] = None
    """窗口使用的字体"""

    font_size: Optional[int] = None
    """窗口字体的大小（px）"""

    stylesheet: Optional[str] = None
    """窗口的样式表（QSS格式）"""


# noinspection PyMethodMayBeStatic
class BaseWindowEventListener(object):
    """该类为窗口事件监听器基类，用于监听`BaseWindow`类的窗口事件。开发者可以在子类中override特定的事件回调函数，以实现对特定事件的监听"""

    def on_create(self, window: "BaseWindow") -> None:
        """
        事件回调函数，在窗口创建后调用。

        Args:
            window: 发生事件的窗口

        Returns:
            无返回值
        """
        pass

    # noinspection PyUnusedLocal
    def on_close(self, window: "BaseWindow") -> bool:
        """
        事件回调函数，在窗口关闭时调用。

        Args:
            window: 发生事件的窗口

        Returns:
            返回一个`bool`值，用于指示是否要关闭窗口。返回`True`表示确实要关闭窗口，返回`False`将阻止窗口被关闭。默认返回`True`。
        """
        return True

    def on_destroy(self, window: "BaseWindow"):
        """
        事件回调函数，在窗口销毁后调用（注意：在该函数回调后，还将回调一次`on_hide()`）。

        Args:
            window: 发生事件的窗口

        Returns:
            无返回值
        """
        pass

    def on_hide(self, window: "BaseWindow"):
        """
        事件回调函数，在窗口被隐藏后调用（注意：在`on_destroy()`被回调后，此函数将被回调）。

        Args:
            window: 发生事件的窗口

        Returns:
            无返回值
        """
        pass

    def on_show(self, window: "BaseWindow"):
        """
        事件回调函数，在窗口显示后调用。

        Args:
            window: 发生事件的窗口

        Returns:
            无返回值
        """
        pass


class SimpleWindowEventListener(BaseWindowEventListener):
    """该类为`BaseWindowEventListener`子类，用于快速创建`BaseWindowEventListener`实例。开发者可以直接在构造函数中传入要监听的事件的回调函数，
    而不必手动创建`BaseWindowEventListener`的子类。
    """

    def __init__(
        self,
        on_create: Callable[["BaseWindow"], None] = None,
        on_show: Callable[["BaseWindow"], None] = None,
        on_hide: Callable[["BaseWindow"], None] = None,
        on_close: Callable[["BaseWindow"], bool] = None,
        on_destroy: Callable[["BaseWindow"], None] = None,
    ):
        """
        构造函数。用于创建`SimpleWindowEventListener`类实例。

        Args:
            on_create: 回调函数，该函数在窗口创建后调用。
            on_show: 回调函数，该函数在窗口显示后回调。
            on_hide: 回调函数，该函数在窗口被隐藏时回调。
            on_close: 回调函数，该函数在窗口被关闭时回调。
            on_destroy: 回调函数，该函数在窗口被销毁后回调。
        """
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
    """
    `PyGUIAdapter`中所有顶级窗口的基类，定义了窗口基本的外观和逻辑，并且实现了一些公共的方法。
    这些方法可以在窗口事件回调函数中或者`Action`的回调函数中调用。
    """

    sig_clear_toasts = Signal()

    def __init__(
        self,
        parent: Optional[QWidget],
        config: BaseWindowConfig,
        listener: Optional[BaseWindowEventListener] = None,
        toolbar: Optional[ToolBarConfig] = None,
        menus: Optional[List[Union[MenuConfig, Separator]]] = None,
    ):
        super().__init__(parent)

        self._config: BaseWindowConfig = config
        self._toolbar: Optional[ToolBarConfig] = toolbar
        if menus:
            menus = [*menus]
        self._menus: Optional[List[Union[MenuConfig, Separator]]] = menus
        self._listener: BaseWindowEventListener = listener
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
        """
        设置窗口标题。

        Args:
            title: 待设置的标题

        Returns:
            无返回值

        """
        title = title or ""
        self.setWindowTitle(title)

    def get_title(self) -> str:
        """
        获取窗口标题。

        Returns:
            返回当前窗口标题
        """
        return self.windowTitle()

    def set_icon(self, icon: IconType):
        """
        设置窗口图标。

        Args:
            icon: 待设置的图标

        Returns:
            无返回值

        """
        icon = get_icon(icon) or QIcon()
        self.setWindowIcon(icon)

    def set_always_on_top(self, enabled: bool):
        """
        设置窗口是否总是置顶。

        Args:
            enabled: 是否总是置顶

        Returns:
            无返回值
        """
        if enabled:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

    def is_always_on_top(self) -> bool:
        """
        判断窗口是否总是置顶。

        Returns:
            返回`True`代表窗口当前处于总是置顶状态。

        """
        return bool(self.windowFlags() & Qt.WindowStaysOnTopHint)

    def set_size(self, size: Union[Tuple[int, int], QSize]):
        """
        设置窗口尺寸。

        Args:
            size: 目标尺寸。

        Returns:
            无返回值

        """
        size = get_size(size)
        if not size:
            raise ValueError(f"invalid size: {size}")
        self.resize(size)

    def get_size(self) -> Tuple[int, int]:
        """
        获取窗口当前尺寸。

        Returns:
            返回窗口当前尺寸。

        """
        size = self.size()
        return size.width(), size.height()

    def set_position(self, position: Optional[Tuple[int, int]]):
        """
        设置窗口在屏幕上的位置。

        Args:
            position: 目标位置。

        Returns:
            无返回值

        """
        if not position:
            return
        if len(position) != 2:
            raise ValueError(f"invalid position: {position}")
        self.move(*position)

    def get_position(self) -> Tuple[int, int]:
        """
        获取窗口位置。

        Returns:
            返回窗口当前在屏幕上的位置。

        """
        pos = self.pos()
        return pos.x(), pos.y()

    def set_font(self, font_family: Union[str, Sequence[str]], font_size: int):
        """
        设置窗口字体。

        Args:
            font_family: 字体名称
            font_size: 字体大小（px）

        Returns:
            无返回值

        """
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
        """
        获取窗口字体大小（px）。

        Returns:
           返回当前窗口字体大小。
        """
        return self.font().pointSize()

    def get_font_family(self) -> str:
        """
        获取当前窗口字体系列名称。

        Returns:
            返回当前窗口字体系列名称（以字符串形式）。
        """
        return self.font().family()

    def get_font_families(self) -> Sequence[str]:
        """
        获取当前窗口字体系列名称。

        Returns:
            返回当前窗口字体系列名称（以列表形式）。
        """
        return self.font().families()

    def set_stylesheet(self, stylesheet: Optional[str]):
        """
        为窗口设置样式表（QSS）格式。

        Args:
            stylesheet: 样式表

        Returns:
            无返回值

        """
        if not stylesheet:
            return
        self.setStyleSheet(stylesheet)

    def get_stylesheet(self) -> str:
        """
        获取窗口当前样式表。

        Returns:
            返回窗口当前样式表。

        """
        return self.styleSheet()

    def find_action(self, action: Action) -> Optional[QAction]:
        """
        查找`action`对应的`QAction`实例。

        Args:
            action: 待查找的`Action`实例

        Returns:
            如果`action`被添加到当前窗口的菜单栏或工具栏中，则返回对应的`QAction`实例，否则，返回`None`。
        """
        return self._actions.get(id(action), None)

    def set_action_state(self, action: Action, checked: bool) -> bool:
        """
        设置`action`对应`QAction`对象的“选中”（`checked`)状态。

        Args:
            action: 待查找的`Action`实例
            checked: 目标状态

        Returns:
            若未找到`action`对应的`QAction`对象，或者对应的`QAction`对象的`checkable`属性为`False`（`isCheckable() == False`），
            则该函数返回`False`。否则返回`True`。


        """
        action = self.find_action(action)
        if action is None:
            warnings.warn(f"action not found: {action}")
            return False
        if not action.isCheckable():
            warnings.warn(f"action is not checkable: {action}")
            return False
        action.setChecked(checked)
        return True

    def toggle_action_state(self, action: Action) -> bool:
        """
        切换`action`对应`QAction`对象的“选中”（`checked`)状态。

        Args:
            action: 待查找的`Action`实例

        Returns:
            若未找到`action`对应的`QAction`对象，或者对应的`QAction`对象的`checkable`属性为`False`（`isCheckable() == False`），
            则该函数返回`False`。否则返回`True`。
        """
        action = self.find_action(action)
        if action is None:
            warnings.warn(f"action not found: {action}")
            return False
        if not action.isCheckable():
            warnings.warn(f"action is not checkable: {action}")
            return False
        action.toggle()

    def query_action_state(self, action: Action) -> Optional[bool]:
        """
        查询`action`对应`QAction`对象是否处于“选中”（`checked`)状态。

        Args:
            action: 待查找的`Action`实例

        Returns:
            若未找到`action`对应的`QAction`对象，函数将返回`None`。否则返回一个`bool`值，用以表示对应`QAction`是否处于“选中”（`checked`)状态。

        """
        action = self.find_action(action)
        if action is None:
            return None
        return action.isChecked()

    @staticmethod
    def get_clipboard_text() -> str:
        """
        获取剪贴板内容。

        Returns:
            返回当前剪贴板文本。
        """
        clipboard = QApplication.clipboard()
        return clipboard.text()

    @staticmethod
    def set_clipboard_text(text: str):
        """
        设置剪贴板内容。

        Args:
            text: 要设置到剪贴板中的文本

        Returns:
            无返回值

        """
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
        """
        显示一条toast消息。

        Args:
            message: 待显示的消息
            duration: 消息显示的时长，单位毫秒
            config: toast的配置
            clear: 在显示当前消息前，是否清除之前发出的消息

        Returns:
            无返回值
        """
        if clear:
            self.clear_toasts()
        toast = ToastWidget(self, message, duration, config=config)
        toast.sig_toast_finished.connect(self._on_toast_finished)
        # noinspection PyUnresolvedReferences
        self.sig_clear_toasts.connect(toast.finish)
        toast.start()

    def clear_toasts(self):
        """
        清除之前发出的toast消息。

        Returns:
            无返回值

        """
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
        self, toolbar: QToolBar, actions: List[Union[Action, Separator]]
    ):
        for action in actions:
            if isinstance(action, Separator):
                toolbar.addSeparator()
                continue

            action = self._create_action(action)
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

        for action in menu_config.actions:
            if isinstance(action, Separator):
                menu.addSeparator()
                continue
            if isinstance(action, Action):
                action = self._create_action(action)
                if action.isCheckable() and exclusive_group:
                    exclusive_group.addAction(action)
                menu.addAction(action)
            elif isinstance(action, MenuConfig):
                submenu = self._create_menu(action)
                menu.addMenu(submenu)
            else:
                raise ValueError(f"invalid action type: {type(action)}")
        return menu

    def _create_action(self, action: Action) -> QAction:
        action_id = id(action)
        # reuse action if already created
        if action_id in self._actions:
            return self._actions[action_id]

        action = QAction(self)
        action.setText(action.text)
        if action.icon:
            action.setIcon(get_icon(action.icon))
        if action.icon_text:
            action.setIconText(action.icon_text)
        action.setAutoRepeat(action.auto_repeat)
        action.setEnabled(action.enabled)
        action.setCheckable(action.checkable)
        action.setChecked(action.checked)
        if action.shortcut:
            action.setShortcut(action.shortcut)
        if action.shortcut_context is not None:
            action.setShortcutContext(action.shortcut_context)
        if action.tooltip:
            action.setToolTip(action.tooltip)
        if action.status_tip:
            action.setStatusTip(action.status_tip)
        if action.whats_this:
            action.setWhatsThis(action.whats_this)
        if action.priority is not None:
            action.setPriority(action.priority)
        if action.menu_role is not None:
            action.setMenuRole(action.menu_role)

        def _on_triggered():
            if action.on_triggered is not None:
                action.on_triggered(self, action)

        def _toggled():
            if action.on_toggled is not None:
                action.on_toggled(self, action)

        # noinspection PyUnresolvedReferences
        action.triggered.connect(_on_triggered)
        # noinspection PyUnresolvedReferences
        action.toggled.connect(_toggled)

        self._actions[action_id] = action
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
