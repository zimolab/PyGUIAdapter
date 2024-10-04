import dataclasses
from typing import Optional, List, Union

from pyqcodeeditor.QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from qtpy.QtWidgets import QWidget

from .actions import DEFAULT_MENUS, DEFAULT_TOOLBAR
from .base import BaseCodeEditorWindow, CodeEditorConfig
from .. import utils
from ..action import Separator
from ..toolbar import ToolBarConfig
from ..window import BaseWindowStateListener


class CodeEditorWindow(BaseCodeEditorWindow):
    def __init__(
        self,
        parent: Optional[QWidget],
        config: Optional[CodeEditorConfig] = None,
        listener: Optional[BaseWindowStateListener] = None,
        toolbar: Optional[ToolBarConfig] = None,
        menus: Optional[List[Union[ToolBarConfig, Separator]]] = None,
    ):
        config = config or CodeEditorConfig()

        if config.use_default_menus and not menus:
            exclude_menus = config.exclude_default_menus
            _menus = {
                menu.title: dataclasses.replace(menu)
                for menu in DEFAULT_MENUS
                if menu.title not in exclude_menus
            }
            exclude_menu_actions = config.exclude_default_menu_actions

            for menu_title, exclude_action in exclude_menu_actions:
                menu = _menus.get(menu_title, None)
                if not menu:
                    continue
                menu.remove_action(exclude_action)
            menus = list(_menus.values())

        if config.use_default_toolbar and not toolbar:
            toolbar = DEFAULT_TOOLBAR
            exclude_toolbar_actions = config.exclude_default_toolbar_actions
            for exclude_action in exclude_toolbar_actions:
                toolbar.remove_action(exclude_action)

        self.__current_file: Optional[str] = None
        self.__fingerprint: Optional[str] = utils.fingerprint(config.initial_text)
        self.__highlighter: Optional[QStyleSyntaxHighlighter] = None

        super().__init__(parent, config, listener, toolbar, menus)

    def _current_highlighter(self) -> Optional[QStyleSyntaxHighlighter]:
        return self.__highlighter

    def _update_current_highlighter(
        self, highlighter: Optional[QStyleSyntaxHighlighter]
    ):
        self.__highlighter = highlighter

    def _current_fingerprint(self) -> Optional[str]:
        return self.__fingerprint

    def _update_fingerprint(self):
        self.__fingerprint = utils.fingerprint(self.get_text())

    def _current_file(self) -> Optional[str]:
        self._config: CodeEditorConfig
        if self._config.no_file_mode:
            return None
        return self.__current_file

    def _update_current_file(self, file: str):
        self._config: CodeEditorConfig
        if self._config.no_file_mode:
            return
        self.__current_file = file
