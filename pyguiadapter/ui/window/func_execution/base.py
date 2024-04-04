import abc
from typing import Dict, Any, List

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QMenu, QToolBar, QMenuBar

from pyguiadapter.adapter.bundle import Callable
from pyguiadapter.ui.menus import create_menu_items, ActionItem, Separator
from pyguiadapter.ui.utils import (
    show_info_dialog,
    show_warning_dialog,
    show_critical_dialog,
    show_question_dialog,
)


class BaseExecutionWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._actions: Dict[int, QAction] = {}

    @abc.abstractmethod
    def get_func(self) -> Callable:
        pass

    @abc.abstractmethod
    def is_func_cancelable(self) -> bool:
        pass

    @abc.abstractmethod
    def is_func_executing(self) -> bool:
        pass

    @abc.abstractmethod
    def cancel_executing(self):
        pass

    @abc.abstractmethod
    def clear_output(self) -> None:
        pass

    @abc.abstractmethod
    def append_output(self, text: str, html: bool = False):
        pass

    @abc.abstractmethod
    def get_param_value(self, param_name: str) -> Any:
        pass

    @abc.abstractmethod
    def get_param_values(self) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def set_param_value(self, name: str, value: Any) -> None:
        pass

    @abc.abstractmethod
    def set_param_values(
        self, param_values: Dict[str, Any], ignore_exceptions: bool = False
    ) -> None:
        pass

    @abc.abstractmethod
    def get_params_info(self) -> Dict[str, Any]:
        pass

    @property
    @abc.abstractmethod
    def execution_context(self) -> Any:
        pass

    def show_info_dialog(self, message: str, *, title: str = None):
        show_info_dialog(self, message, title=title)

    def show_warning_dialog(self, message: str, *, title: str = None):
        show_warning_dialog(self, message, title=title)

    def show_critical_dialog(self, message: str, *, title: str = None):
        show_critical_dialog(self, message, title=title)

    def show_question_dialog(self, message: str, *, title: str = None) -> bool:
        return show_question_dialog(self, message, title=title)

    def _create_menus(self, menubar: QMenuBar, menu_configs: Dict[str, Dict]):
        for menu_name, items in menu_configs.items():
            if not isinstance(items, dict):
                raise ValueError("invalid menu items type")
            menu = QMenu(menu_name, parent=menubar)
            create_menu_items(
                items=items,
                parent_menu=menu,
                action_creator=self._create_action,
            )
            menubar.addMenu(menu)

    def _create_toolbar_actions(
        self, toolbar: QToolBar, toolbar_actions: List[ActionItem]
    ):
        for action_item in toolbar_actions:
            if isinstance(action_item, ActionItem):
                action = self._create_action(action_item)
                toolbar.addAction(action)
            elif action_item is Separator:
                toolbar.addSeparator()
            else:
                raise ValueError("invalid toolbar action item")

    def _create_action(self, action_item: ActionItem) -> QAction:
        key = id(action_item)
        if key in self._actions:
            return self._actions[key]
        action = QAction()
        action.setText(action_item.text)
        action.setData(action_item.callback)
        # noinspection PyUnresolvedReferences
        action.triggered.connect(self._on_action_triggered)
        if action_item.shortcut:
            action.setShortcut(action_item.shortcut)
        if action_item.icon:
            action.setIcon(QIcon(action_item.icon))
        self._actions[key] = action
        return action

    def _on_action_triggered(self, _):
        action = self.sender()
        if not isinstance(action, QAction):
            return
        action_callback = action.data()
        assert action_callback is not None and callable(action_callback)
        action_callback(self.execution_context)
