from __future__ import annotations

import dataclasses
import inspect
import os
from abc import abstractmethod
from typing import Type, Callable, Tuple

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from qtpy.QtGui import QTextOption
from qtpy.QtWidgets import QWidget, QCompleter, QVBoxLayout, QTextEdit

from .constants import (
    DEFAULT_TAB_SIZE,
    DEFAULT_LINE_WRAP_WIDTH,
    UNSAVED_WARNING_MSG,
    CONFIRM_DIALOG_TITLE,
    DEFAULT_WINDOW_TITLE,
    DEFAULT_UNTITLED_FILENAME,
    OPEN_FILE_DIALOG_TITLE,
    ERROR_DIALOG_TITLE,
    OPEN_FAILED_MSG,
    SAVE_FAILED_MSG,
    SAVE_AS_DIALOG_TITLE,
    FORMAT_FAILED_MSG,
    QUIT_DIALOG_TITLE,
)
from .. import utils
from ..window import BaseWindow, BaseWindowConfig


class BaseCodeFormatter(object):
    @abstractmethod
    def format_code(self, text: str) -> str | None:
        pass


LineWrapMode = QTextEdit.LineWrapMode
WordWrapMode = QTextOption.WrapMode


@dataclasses.dataclass
class CodeEditorConfig(BaseWindowConfig):
    title: str | None = None
    untitled_filename: str | None = None
    use_default_menus: bool = True
    use_default_toolbar: bool = True
    highlighter: Type[QStyleSyntaxHighlighter] | None = None
    highlighter_args: dict | list | tuple | None = None
    completer: QCompleter | None = None
    auto_indent: bool = True
    auto_parentheses: bool = True
    text_font_size: int | None = None
    tab_size: int = DEFAULT_TAB_SIZE
    tab_replace: bool = True
    initial_text: str = ""
    formatter: BaseCodeFormatter | Callable[[str], str] | None = None
    file_filters: str | None = None
    start_dir: str | None = None
    check_unsaved_changes: bool = True
    show_filename_in_title: bool = True
    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    line_wrap_width: int = DEFAULT_LINE_WRAP_WIDTH
    word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap
    file_encoding: str = "utf-8"

    quit_dialog_title: str | None = None
    confirm_dialog_title: str | None = None
    error_dialog_title: str | None = None
    open_file_dialog_title: str | None = None
    save_file_dialog_title: str | None = None
    save_as_dialog_title: str | None = None
    unsaved_warning_message: str | None = None
    open_failed_message: str | None = None
    save_failed_message: str | None = None
    format_failed_message: str | None = None

    exclude_default_menus: Tuple[str] = ()
    exclude_default_menu_actions: Tuple[Tuple[str, str], ...] = ()
    exclude_default_toolbar_actions: Tuple[str, ...] = ()

    no_file_mode: bool = False


class BaseCodeEditorWindow(BaseWindow):

    def _setup_ui(self):
        super()._setup_ui()

        center_widget = QWidget(self)

        config = self._config_instance()
        editor = QCodeEditor(center_widget)
        self._set_editor_instance(editor)

        self.set_highlighter(config.highlighter)
        self.set_completer(config.completer)
        self.set_auto_indent_enabled(config.auto_indent)
        self.set_auto_parentheses_enabled(config.auto_parentheses)
        self.set_tab_replace(config.tab_size, config.tab_replace)
        self.set_text_font_size(config.text_font_size)
        self.set_line_wrap_mode(config.line_wrap_mode)
        self.set_line_wrap_width(config.line_wrap_width)
        self.set_word_wrap_mode(config.word_wrap_mode)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(editor)

        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)

        self.set_text(config.initial_text)
        self._update_fingerprint()
        self._update_title()

    def _on_close(self) -> bool:
        if not self.check_modification():
            return super()._on_close()

        config = self._config_instance()
        # noinspection PyUnresolvedReferences
        msgbox = utils.MessageBoxConfig(
            title=config.quit_dialog_title or QUIT_DIALOG_TITLE,
            text=config.unsaved_warning_message or UNSAVED_WARNING_MSG,
            buttons=utils.StandardButton.Yes | utils.StandardButton.No,
        ).create_messagebox(self)
        if msgbox.exec_() == utils.StandardButton.Yes:
            return super()._on_close()
        else:
            return False

    @abstractmethod
    def _set_editor_instance(self, editor: QCodeEditor):
        pass

    @abstractmethod
    def _editor_instance(self) -> QCodeEditor:
        pass

    @abstractmethod
    def _config_instance(self) -> CodeEditorConfig:
        pass

    @abstractmethod
    def _current_highlighter(self) -> QStyleSyntaxHighlighter | None:
        pass

    @abstractmethod
    def _update_current_highlighter(self, highlighter: QStyleSyntaxHighlighter | None):
        pass

    @abstractmethod
    def _current_fingerprint(self) -> str | None:
        pass

    @abstractmethod
    def _update_fingerprint(self):
        pass

    @abstractmethod
    def _current_file(self) -> str | None:
        pass

    @abstractmethod
    def _update_current_file(self, file: str):
        pass

    def _update_title(self):
        if self._config_instance().title is None:
            win_title = DEFAULT_WINDOW_TITLE
        else:
            win_title = self._config_instance().title.strip()

        if self._config_instance().untitled_filename is None:
            untitled_filename = DEFAULT_UNTITLED_FILENAME
        else:
            untitled_filename = self._config_instance().untitled_filename
        current_file = (self._current_file() or "").strip()
        if self._config_instance().show_filename_in_title:
            if not current_file:
                filename = untitled_filename
            else:
                filename = os.path.basename(current_file)
            win_title = f"{win_title} - {filename}".strip()
        self.setWindowTitle(win_title)

    def get_text(self) -> str:
        return self._editor_instance().toPlainText()

    def set_text(self, text: str | None):
        text = text or ""
        self._editor_instance().setPlainText(text)

    def set_highlighter(
        self,
        highlighter: Type[QStyleSyntaxHighlighter] | None,
        args: list | tuple | dict | None = None,
    ):
        config = self._config_instance()
        config.highlighter = highlighter
        config.highlighter_args = args
        current_highlighter = self._current_highlighter()
        if current_highlighter is not None:
            current_highlighter.setDocument(None)
            self._update_current_highlighter(None)
            current_highlighter.deleteLater()
        current_highlighter = create_highlighter(highlighter, args)
        if current_highlighter is not None:
            current_highlighter.setParent(self)
        self._editor_instance().setHighlighter(current_highlighter)

    def get_highlighter(self) -> Type[QStyleSyntaxHighlighter] | None:
        return self._config_instance().highlighter

    def set_completer(self, completer: QCompleter | None):
        self._editor_instance().setCompleter(completer)
        self._config_instance().completer = completer

    def get_completer(self) -> QCompleter | None:
        return self._config_instance().completer

    def set_formatter(self, formatter: BaseCodeFormatter | Callable[[str], str] | None):
        assert (
            formatter is None
            or callable(formatter)
            or isinstance(formatter, BaseCodeFormatter)
        )
        self._config_instance().formatter = formatter

    def get_formatter(self) -> BaseCodeFormatter | Callable[[str], str] | None:
        return self._config_instance().formatter

    def set_tab_replace(self, size: int = DEFAULT_TAB_SIZE, tab_replace: bool = True):
        config = self._config_instance()
        config.tab_size = size
        config.tab_replace = tab_replace
        self._editor_instance().setTabReplace(tab_replace)
        self._editor_instance().setTabReplaceSize(size)

    def get_tab_size(self) -> int:
        return self._config_instance().tab_size

    def is_tab_replace_enabled(self) -> bool:
        return self._config_instance().tab_replace

    def set_auto_indent_enabled(self, enable: bool = True):
        self._config_instance().auto_indent = enable
        self._editor_instance().setAutoIndentation(enable)

    def is_auto_indent_enabled(self) -> bool:
        return self._config_instance().auto_indent

    def set_auto_parentheses_enabled(self, enable: bool):
        self._config_instance().auto_parentheses = enable
        self._editor_instance().setAutoParentheses(enable)

    def is_auto_parentheses_enabled(self) -> bool:
        return self._config_instance().auto_parentheses

    def set_text_font_size(self, size: int | None):
        self._config_instance().text_font_size = size
        if size and size > 0:
            self._editor_instance().setFontSize(size)

    def get_text_font_size(self) -> int | None:
        return self._config_instance().text_font_size

    def set_word_wrap_mode(self, mode: WordWrapMode):
        if mode is not None:
            self._config_instance().word_wrap_mode = mode
            self._editor_instance().setWordWrapMode(mode)

    def get_word_wrap_mode(self) -> WordWrapMode:
        return self._config_instance().word_wrap_mode

    def set_line_wrap_mode(self, mode: LineWrapMode):
        if mode is not None:
            self._config_instance().line_wrap_mode = mode
            self._editor_instance().setLineWrapMode(mode)

    def get_line_wrap_mode(self) -> LineWrapMode:
        return self._config_instance().line_wrap_mode

    def set_line_wrap_width(self, width: int):
        assert width > 0
        self._config_instance().line_wrap_width = width
        self._editor_instance().setLineWrapColumnOrWidth(width)

    def get_line_wrap_width(self) -> int:
        return self._config_instance().line_wrap_width

    def set_file_filters(self, filters: str | None):
        self._config_instance().file_filters = filters

    def get_file_filters(self) -> str | None:
        return self._config_instance().file_filters

    def set_start_dir(self, directory: str | None):
        self._config_instance().start_dir = directory

    def get_start_dir(self) -> str | None:
        return self._config_instance().start_dir

    def set_show_filename_in_title(self, show: bool):
        self._config_instance().show_filename_in_title = show

    def is_show_filename_in_title(self) -> bool:
        return self._config_instance().show_filename_in_title

    def is_modified(self) -> bool:
        text = self.get_text()
        current_fingerprint = utils.fingerprint(text)
        return current_fingerprint != self._current_fingerprint()

    def check_modification(self) -> bool:
        if not self._config_instance().check_unsaved_changes:
            return False
        return self.is_modified()

    def open_file(self):
        config = self._config_instance()
        if self.check_modification():
            # noinspection PyUnresolvedReferences
            ret = utils.show_question_message(
                self,
                message=config.unsaved_warning_message or UNSAVED_WARNING_MSG,
                title=config.confirm_dialog_title or CONFIRM_DIALOG_TITLE,
                buttons=utils.StandardButton.No | utils.StandardButton.Yes,
            )
            if ret != utils.StandardButton.Yes:
                return
        filepath = utils.get_open_file(
            self,
            title=config.open_file_dialog_title or OPEN_FILE_DIALOG_TITLE,
            start_dir=config.start_dir,
            filters=config.file_filters,
        )
        if not filepath:
            return

        try:
            new_text = utils.read_text_file(filepath, encoding=config.file_encoding)
        except Exception as e:
            msg = config.open_failed_message or OPEN_FAILED_MSG
            msg = msg.format(filepath)
            utils.show_exception_message(
                self,
                exception=e,
                title=config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}:{e}",
                detail=True,
            )
            return
        self.set_text(new_text)
        if not config.no_file_mode:
            self._update_current_file(os.path.normpath(os.path.abspath(filepath)))
            self._update_fingerprint()
            self._update_title()

    def save_file(self):
        config = self._config_instance()
        if config.no_file_mode:
            return
        current_file = self._current_file()
        if not current_file:
            return self.save_as_file()

        if not self.check_modification():
            return
        try:
            utils.write_text_file(
                current_file, self.get_text(), encoding=config.file_encoding
            )
        except Exception as e:
            msg = config.save_failed_message or SAVE_FAILED_MSG
            msg = msg.format(current_file)
            utils.show_exception_message(
                self,
                exception=e,
                title=config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}: {e}",
            )
        else:
            self._update_fingerprint()

    def save_as_file(self):
        config = self._config_instance()
        if config.no_file_mode:
            return
        filepath = utils.get_save_file(
            self,
            title=config.save_as_dialog_title or SAVE_AS_DIALOG_TITLE,
            start_dir=config.start_dir,
            filters=config.file_filters,
        )
        if not filepath:
            return
        try:
            utils.write_text_file(
                filepath, self.get_text(), encoding=config.file_encoding
            )
        except Exception as e:
            msg = config.save_failed_message or SAVE_FAILED_MSG
            msg = msg.format(filepath)
            utils.show_exception_message(
                self,
                exception=e,
                title=config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}: {e}",
            )
        else:
            self._update_current_file(os.path.normpath(os.path.abspath(filepath)))
            self._update_fingerprint()
            self._update_title()

    def format_code(self):
        config = self._config_instance()
        if not config.formatter:
            return

        try:
            if isinstance(config.formatter, BaseCodeFormatter):
                formatted = config.formatter.format_code(self.get_text())
            else:
                formatted = config.formatter(self.get_text())
        except Exception as e:
            msg = config.format_failed_message or FORMAT_FAILED_MSG
            utils.show_exception_message(
                self,
                exception=e,
                title=config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}: {e}",
            )
            return
        if isinstance(formatted, str):
            self.set_text(formatted)

    def redo(self):
        self._editor_instance().redo()

    def undo(self):
        self._editor_instance().undo()

    def cut(self):
        self._editor_instance().cut()

    def copy(self):
        self._editor_instance().copy()

    def paste(self):
        self._editor_instance().paste()

    def select_all(self):
        self._editor_instance().selectAll()


def create_highlighter(
    highlighter_class: Type[QStyleSyntaxHighlighter] | None,
    args: dict | list | tuple | None,
) -> QStyleSyntaxHighlighter | None:
    assert highlighter_class is None or (
        inspect.isclass(highlighter_class)
        and issubclass(highlighter_class, QStyleSyntaxHighlighter)
    )
    assert args is None or isinstance(args, (dict, list, tuple))
    if highlighter_class is None:
        return None

    if not args:
        instance = highlighter_class(None)
    elif isinstance(args, dict):
        instance = highlighter_class(**args)
    elif isinstance(args, (list, tuple)):
        instance = highlighter_class(*args)
    else:
        raise TypeError(f"invalid type of args: {type(args)}")

    return instance
