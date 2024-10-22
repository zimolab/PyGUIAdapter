import dataclasses
import inspect
import os
from abc import abstractmethod
from typing import Type, Callable, Tuple, Optional, Union, List

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
from ..action import Separator
from ..toolbar import ToolBar
from ..window import BaseWindow, BaseWindowConfig, BaseWindowEventListener


class BaseCodeFormatter(object):
    @abstractmethod
    def format_code(self, text: str) -> Optional[str]:
        pass


LineWrapMode = QTextEdit.LineWrapMode
WordWrapMode = QTextOption.WrapMode


@dataclasses.dataclass(frozen=True)
class CodeEditorConfig(BaseWindowConfig):
    title: Optional[str] = None
    untitled_filename: Optional[str] = None
    highlighter: Optional[Type[QStyleSyntaxHighlighter]] = None
    highlighter_args: Union[dict, list, tuple, None] = None
    completer: Optional[QCompleter] = None
    auto_indent: bool = True
    auto_parentheses: bool = True
    text_font_size: Optional[int] = None
    text_font_family: Optional[str] = None
    tab_size: int = DEFAULT_TAB_SIZE
    tab_replace: bool = True
    initial_text: str = ""
    formatter: Union[BaseCodeFormatter, Callable[[str], str], None] = None
    file_filters: Optional[str] = None
    start_dir: Optional[str] = None
    check_unsaved_changes: bool = True
    show_filename_in_title: bool = True
    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    line_wrap_width: int = DEFAULT_LINE_WRAP_WIDTH
    word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap
    file_encoding: str = "utf-8"

    quit_dialog_title: Optional[str] = None
    confirm_dialog_title: Optional[str] = None
    error_dialog_title: Optional[str] = None
    open_file_dialog_title: Optional[str] = None
    save_file_dialog_title: Optional[str] = None
    save_as_dialog_title: Optional[str] = None
    unsaved_warning_message: Optional[str] = None
    open_failed_message: Optional[str] = None
    save_failed_message: Optional[str] = None
    format_failed_message: Optional[str] = None

    use_default_menus: bool = True
    excluded_menus: Tuple[str] = ()
    excluded_menu_actions: Tuple[Tuple[str, str], ...] = ()

    use_default_toolbar: bool = True
    excluded_toolbar_actions: Tuple[str, ...] = ()

    no_file_mode: bool = False


class BaseCodeEditorWindow(BaseWindow):

    def __init__(
        self,
        parent: Optional[QWidget],
        config: Optional[CodeEditorConfig] = None,
        listener: Optional[BaseWindowEventListener] = None,
        toolbar: Optional[ToolBar] = None,
        menus: Optional[List[Union[ToolBar, Separator]]] = None,
    ):
        config = config or CodeEditorConfig()
        self._editor: Optional[QCodeEditor] = None
        super().__init__(parent, config, listener, toolbar, menus)

    def apply_configs(self):
        super().apply_configs()
        self._config: CodeEditorConfig
        self.set_highlighter(self._config.highlighter)
        self.set_completer(self._config.completer)
        self.set_auto_indent_enabled(self._config.auto_indent)
        self.set_auto_parentheses_enabled(self._config.auto_parentheses)
        self.set_tab_replace(self._config.tab_size, self._config.tab_replace)
        self.set_text_font_size(self._config.text_font_size)
        self.set_text_font_family(self._config.text_font_family)
        self.set_line_wrap_mode(self._config.line_wrap_mode)
        self.set_line_wrap_width(self._config.line_wrap_width)
        self.set_word_wrap_mode(self._config.word_wrap_mode)

    def _create_ui(self):
        self._config: CodeEditorConfig

        center_widget = QWidget(self)
        self._editor = QCodeEditor(center_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._editor)
        self.setCentralWidget(center_widget)
        center_widget.setLayout(layout)

        self.set_text(self._config.initial_text)
        self._update_fingerprint()
        self._update_title()

    def _on_close(self) -> bool:
        self._config: CodeEditorConfig
        if not self.check_modification():
            return super()._on_close()
        # noinspection PyUnresolvedReferences
        msgbox = utils.MessageBoxConfig(
            title=self._config.quit_dialog_title or QUIT_DIALOG_TITLE,
            text=self._config.unsaved_warning_message or UNSAVED_WARNING_MSG,
            buttons=utils.StandardButton.Yes | utils.StandardButton.No,
        ).create_messagebox(self)
        if msgbox.exec_() == utils.StandardButton.Yes:
            return super()._on_close()
        else:
            return False

    @abstractmethod
    def _current_highlighter(self) -> Optional[QStyleSyntaxHighlighter]:
        pass

    @abstractmethod
    def _update_current_highlighter(
        self, highlighter: Optional[QStyleSyntaxHighlighter]
    ):
        pass

    @abstractmethod
    def _current_fingerprint(self) -> Optional[str]:
        pass

    @abstractmethod
    def _update_fingerprint(self):
        pass

    @abstractmethod
    def _current_file(self) -> Optional[str]:
        pass

    @abstractmethod
    def _update_current_file(self, file: str):
        pass

    def _update_title(self):
        self._config: CodeEditorConfig
        if self._config.title is None:
            win_title = DEFAULT_WINDOW_TITLE
        else:
            win_title = self._config.title.strip()

        if self._config.untitled_filename is None:
            untitled_filename = DEFAULT_UNTITLED_FILENAME
        else:
            untitled_filename = self._config.untitled_filename
        current_file = (self._current_file() or "").strip()
        if self._config.show_filename_in_title:
            if not current_file:
                filename = untitled_filename
            else:
                filename = os.path.basename(current_file)
            win_title = f"{win_title} - {filename}".strip()
        self.setWindowTitle(win_title)

    def get_text(self) -> str:
        return self._editor.toPlainText()

    def set_text(self, text: Optional[str]):
        self._editor.setPlainText(text or "")

    def set_highlighter(
        self,
        highlighter: Optional[Type[QStyleSyntaxHighlighter]],
        args: Union[list, tuple, dict, None] = None,
    ):
        current_highlighter = self._current_highlighter()
        if current_highlighter is not None:
            current_highlighter.setDocument(None)
            current_highlighter.deleteLater()
            self._update_current_highlighter(None)
        current_highlighter = create_highlighter(highlighter, args)
        if current_highlighter is not None:
            current_highlighter.setParent(self)
        self._editor.setHighlighter(current_highlighter)

    def set_completer(self, completer: Optional[QCompleter]):
        self._editor.setCompleter(completer)

    def set_tab_replace(self, size: int = DEFAULT_TAB_SIZE, tab_replace: bool = True):
        self._editor.setTabReplace(tab_replace)
        self._editor.setTabReplaceSize(size)

    def is_tab_replace_enabled(self) -> bool:
        return self._editor.tabReplace()

    def get_tab_replace_size(self) -> int:
        return self._editor.tabReplaceSize()

    def set_auto_indent_enabled(self, enable: bool = True):
        self._editor.setAutoIndentation(enable)

    def is_auto_indent_enabled(self) -> bool:
        return self._editor.autoIndentation()

    def set_auto_parentheses_enabled(self, enable: bool):
        self._editor.setAutoParentheses(enable)

    def is_auto_parentheses_enabled(self) -> bool:
        return self._editor.autoParentheses()

    def set_text_font_size(self, size: Optional[int]):
        if size is None:
            return
        if size <= 0:
            raise ValueError(f"invalid size: {size}")
        self._editor.setFontPointSize(size)

    def set_text_font_family(self, family: Optional[str]):
        if family is None or family.strip() == "":
            return
        self._editor.setFontFamily(family)

    def get_text_font_size(self) -> Optional[int]:
        return self._editor.fontSize()

    def set_word_wrap_mode(self, mode: WordWrapMode):
        if mode is not None:
            self._editor.setWordWrapMode(mode)

    def get_word_wrap_mode(self) -> WordWrapMode:
        return self._editor.wordWrapMode()

    def set_line_wrap_mode(self, mode: LineWrapMode):
        if mode is not None:
            self._editor.setLineWrapMode(mode)

    def get_line_wrap_mode(self) -> LineWrapMode:
        return self._editor.lineWrapMode()

    def set_line_wrap_width(self, width: Optional[int]):
        if width is None:
            return
        if width <= 0:
            raise ValueError(f"invalid width: {width}")
        self._editor.setLineWrapColumnOrWidth(width)

    def get_line_wrap_width(self) -> int:
        return self._editor.lineWrapColumnOrWidth()

    def is_modified(self) -> bool:
        text = self.get_text()
        current_fingerprint = utils.fingerprint(text)
        return current_fingerprint != self._current_fingerprint()

    def check_modification(self) -> bool:
        self._config: CodeEditorConfig
        if not self._config.check_unsaved_changes:
            return False
        return self.is_modified()

    def open_file(self):
        self._config: CodeEditorConfig
        if self.check_modification():
            # noinspection PyUnresolvedReferences
            ret = utils.show_question_message(
                self,
                message=self._config.unsaved_warning_message or UNSAVED_WARNING_MSG,
                title=self._config.confirm_dialog_title or CONFIRM_DIALOG_TITLE,
                buttons=utils.StandardButton.No | utils.StandardButton.Yes,
            )
            if ret != utils.StandardButton.Yes:
                return
        filepath = utils.get_open_file(
            self,
            title=self._config.open_file_dialog_title or OPEN_FILE_DIALOG_TITLE,
            start_dir=self._config.start_dir,
            filters=self._config.file_filters,
        )
        if not filepath:
            return

        try:
            new_text = utils.read_text_file(
                filepath, encoding=self._config.file_encoding
            )
        except Exception as e:
            msg = self._config.open_failed_message or OPEN_FAILED_MSG
            msg = msg.format(filepath)
            utils.show_exception_messagebox(
                self,
                exception=e,
                title=self._config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}:{e}",
                detail=True,
            )
            return
        self.set_text(new_text)
        if not self._config.no_file_mode:
            self._update_current_file(os.path.normpath(os.path.abspath(filepath)))
            self._update_fingerprint()
            self._update_title()

    def save_file(self):
        self._config: CodeEditorConfig
        if self._config.no_file_mode:
            return
        current_file = self._current_file()
        if not current_file:
            return self.save_as_file()

        if not self.check_modification():
            return
        try:
            utils.write_text_file(
                current_file, self.get_text(), encoding=self._config.file_encoding
            )
        except Exception as e:
            msg = self._config.save_failed_message or SAVE_FAILED_MSG
            msg = msg.format(current_file)
            utils.show_exception_messagebox(
                self,
                exception=e,
                title=self._config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}: {e}",
            )
        else:
            self._update_fingerprint()

    def save_as_file(self):
        self._config: CodeEditorConfig
        if self._config.no_file_mode:
            return
        filepath = utils.get_save_file(
            self,
            title=self._config.save_as_dialog_title or SAVE_AS_DIALOG_TITLE,
            start_dir=self._config.start_dir,
            filters=self._config.file_filters,
        )
        if not filepath:
            return
        try:
            utils.write_text_file(
                filepath, self.get_text(), encoding=self._config.file_encoding
            )
        except Exception as e:
            msg = self._config.save_failed_message or SAVE_FAILED_MSG
            msg = msg.format(filepath)
            utils.show_exception_messagebox(
                self,
                exception=e,
                title=self._config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}: {e}",
            )
        else:
            self._update_current_file(os.path.normpath(os.path.abspath(filepath)))
            self._update_fingerprint()
            self._update_title()

    def format_code(self):
        self._config: CodeEditorConfig
        if not self._config.formatter:
            return

        try:
            if isinstance(self._config.formatter, BaseCodeFormatter):
                formatted = self._config.formatter.format_code(self.get_text())
            else:
                formatted = self._config.formatter(self.get_text())
        except Exception as e:
            msg = self._config.format_failed_message or FORMAT_FAILED_MSG
            utils.show_exception_messagebox(
                self,
                exception=e,
                title=self._config.error_dialog_title or ERROR_DIALOG_TITLE,
                message=f"{msg}: {e}",
            )
            return
        if isinstance(formatted, str):
            self.set_text(formatted)

    def redo(self):
        self._editor.redo()

    def undo(self):
        self._editor.undo()

    def cut(self):
        self._editor.cut()

    def copy(self):
        self._editor.copy()

    def paste(self):
        self._editor.paste()

    def select_all(self):
        self._editor.selectAll()


def create_highlighter(
    highlighter_class: Optional[Type[QStyleSyntaxHighlighter]],
    args: Union[dict, list, tuple, None],
) -> Optional[QStyleSyntaxHighlighter]:
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
