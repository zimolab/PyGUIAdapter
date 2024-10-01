import dataclasses
from typing import cast, Optional, List, Union

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from qtpy.QtWidgets import QWidget

from .. import utils
from .base import BaseCodeEditorWindow, CodeEditorConfig
from .actions import DEFAULT_MENUS, DEFAULT_TOOLBAR
from ..action import Separator
from ..toolbar import ToolBarConfig
from ..window import WindowStateListener


class CodeEditorWindow(BaseCodeEditorWindow):
    def __init__(
        self,
        parent: Optional[QWidget],
        config: Optional[CodeEditorConfig] = None,
        listener: Optional[WindowStateListener] = None,
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

        self.__editor: Optional[QCodeEditor] = None
        self.__current_file: Optional[str] = None
        self.__fingerprint: Optional[str] = utils.fingerprint(config.initial_text)
        self.__highlighter: Optional[QStyleSyntaxHighlighter] = None

        super().__init__(parent, config, listener, toolbar, menus)

    def _set_editor_instance(self, editor: QCodeEditor):
        assert self.__editor is None
        self.__editor = editor

    def _editor_instance(self) -> QCodeEditor:
        return self.__editor

    def _config_instance(self) -> CodeEditorConfig:
        return cast(CodeEditorConfig, self._config)

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
