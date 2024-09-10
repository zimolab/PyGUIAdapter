from __future__ import annotations

import dataclasses
import hashlib
import inspect
import json
import os.path
import warnings
from abc import abstractmethod
from typing import Callable, List, Type

from yapf.yapflib.yapf_api import FormatCode
from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from qtpy.QtGui import QAction, QTextOption
from qtpy.QtWidgets import QWidget, QCompleter, QVBoxLayout, QTextEdit

from .. import utils
from ..window import (
    BaseWindow,
    BaseWindowConfig,
    MenuConfig,
    Separator,
    ToolbarConfig,
    ActionConfig,
)


LineWrapMode = QTextEdit.LineWrapMode
WordWrapMode = QTextOption.WrapMode


class BaseCodeFormatter(object):

    @abstractmethod
    def format_code(self, text: str) -> str | None:
        pass


class JsonFormatter(BaseCodeFormatter):

    def __init__(self, indent: int = 4):
        self._indent = indent

    @property
    def indent(self) -> int:
        return self._indent

    @indent.setter
    def indent(self, value: int):
        if value < 0:
            warnings.warn(f"indent must be greater than or equals to 0, got: {value}")
            return
        self._indent = value

    def format_code(self, text: str) -> str | None:
        try:
            return json.dumps(json.loads(text), indent=self._indent, ensure_ascii=False)
        except Exception as e:
            warnings.warn(f"failed to format code: {e}")
            return None


class PythonCodeFormatter(BaseCodeFormatter):

    def __init__(self):
        pass

    def format_code(self, text: str) -> str | None:
        try:
            formatted, changed = FormatCode(text)
        except Exception as e:
            warnings.warn(f"failed to format code: {e}")
            return None
        else:
            if changed:
                return formatted
            return None


def _on_open_file(ctx: "CodeEditorWindow", _: QAction):
    ctx.open_file()


def _on_save_file(ctx: "CodeEditorWindow", _: QAction):
    ctx.save_file()


def _on_save_file_as(ctx: "CodeEditorWindow", _: QAction):
    ctx.save_as_file()


def _on_quit(ctx: "CodeEditorWindow", _: QAction):
    ctx.close()


def _on_undo(ctx: "CodeEditorWindow", _: QAction):
    ctx.undo()


def _on_redo(ctx: "CodeEditorWindow", _: QAction):
    ctx.redo()


def _on_cut(ctx: "CodeEditorWindow", _: QAction):
    ctx.cut()


def _on_copy(ctx: "CodeEditorWindow", _: QAction):
    ctx.copy()


def _on_paste(ctx: "CodeEditorWindow", _: QAction):
    ctx.paste()


def _on_format_code(ctx: "CodeEditorWindow", _: QAction):
    ctx.format_code()


def _on_select_all(ctx: "CodeEditorWindow", _: QAction):
    ctx.select_all()


DEFAULT_ACTION_OPEN = ActionConfig(
    text="Open",
    icon="fa.folder-open-o",
    shortcut="Ctrl+O",
    on_triggered=_on_open_file,
)

DEFAULT_ACTION_SAVE = ActionConfig(
    text="Save",
    icon="fa.save",
    shortcut="Ctrl+S",
    on_triggered=_on_save_file,
)

DEFAULT_ACTION_SAVE_AS = ActionConfig(
    text="Save as",
    icon="mdi.content-save-edit-outline",
    shortcut="Ctrl+Shift+S",
    on_triggered=_on_save_file_as,
)

DEFAULT_ACTION_QUIT = ActionConfig(
    text="Quit",
    icon="fa.window-close-o",
    shortcut="Ctrl+Q",
    on_triggered=_on_quit,
)

DEFAULT_ACTION_UNDO = ActionConfig(
    text="Undo",
    icon="fa.undo",
    shortcut="Ctrl+Z",
    on_triggered=_on_undo,
)

DEFAULT_ACTION_REDO = ActionConfig(
    text="Redo",
    icon="fa.repeat",
    shortcut="Ctrl+Y",
    on_triggered=_on_redo,
)

DEFAULT_ACTION_CUT = ActionConfig(
    text="Cut",
    icon="fa.cut",
    shortcut="Ctrl+X",
    on_triggered=_on_cut,
)

DEFAULT_ACTION_COPY = ActionConfig(
    text="Copy",
    icon="fa.copy",
    shortcut="Ctrl+C",
    on_triggered=_on_copy,
)

DEFAULT_ACTION_PASTE = ActionConfig(
    text="Paste",
    icon="fa.paste",
    shortcut="Ctrl+V",
    on_triggered=_on_paste,
)

DEFAULT_ACTION_FORMAT_CODE = ActionConfig(
    text="Format code",
    icon="fa.indent",
    shortcut="Ctrl+Alt+L",
    on_triggered=_on_format_code,
)


DEFAULT_ACTION_SELECT_ALL = ActionConfig(
    text="Select all",
    icon="fa.object-group",
    shortcut="Ctrl+A",
    on_triggered=_on_select_all,
)

DEFAULT_FILE_MENU = MenuConfig(
    title="File",
    actions=[
        DEFAULT_ACTION_OPEN,
        DEFAULT_ACTION_SAVE,
        DEFAULT_ACTION_SAVE_AS,
        Separator(),
        DEFAULT_ACTION_QUIT,
    ],
)

DEFAULT_EDIT_MENU = MenuConfig(
    title="Edit",
    actions=[
        DEFAULT_ACTION_UNDO,
        DEFAULT_ACTION_REDO,
        Separator(),
        DEFAULT_ACTION_CUT,
        DEFAULT_ACTION_COPY,
        DEFAULT_ACTION_PASTE,
        Separator(),
        DEFAULT_ACTION_FORMAT_CODE,
        Separator(),
        DEFAULT_ACTION_SELECT_ALL,
    ],
)


DEFAULT_MENUS: List[MenuConfig] = [DEFAULT_FILE_MENU, DEFAULT_EDIT_MENU]
DEFAULT_TOOLBARS = ToolbarConfig(
    actions=[
        DEFAULT_ACTION_OPEN,
        DEFAULT_ACTION_SAVE,
        Separator(),
        DEFAULT_ACTION_UNDO,
        DEFAULT_ACTION_REDO,
        Separator(),
        DEFAULT_ACTION_CUT,
        DEFAULT_ACTION_COPY,
        DEFAULT_ACTION_PASTE,
        Separator(),
        DEFAULT_ACTION_FORMAT_CODE,
        Separator(),
        DEFAULT_ACTION_SELECT_ALL,
    ],
    moveable=True,
    icon_size=(24, 24),
)

DEFAULT_TEXT_FONT_SIZE = 14
DEFAULT_TAB_SIZE = 4


@dataclasses.dataclass
class CodeEditorConfig(BaseWindowConfig):
    title: str = "Editor"
    enable_default_menus: bool = True
    enable_default_toolbar: bool = True
    highlighter: Type[QStyleSyntaxHighlighter] | None = None
    highlighter_args: dict | list | tuple | None = None
    completer: QCompleter | None = None
    auto_indent: bool = True
    auto_parentheses: bool = True
    text_font_size: int | None = None
    tab_size: int = DEFAULT_TAB_SIZE
    tab_replace: bool = True
    initial_text: str = ""
    code_formatter: BaseCodeFormatter | Callable[[str], str] | None = None
    file_filters: str | None = None
    start_dir: str | None = None
    check_unsaved_changes: bool = True
    show_filename_in_title: bool = True
    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    line_wrap_width: int = 88
    word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap


class CodeEditorWindow(BaseWindow):
    def __init__(self, parent: QWidget | None, config: CodeEditorConfig | None = None):
        config = config or CodeEditorConfig()

        if config.enable_default_menus and config.menus is None:
            config.menus = DEFAULT_MENUS

        if config.enable_default_toolbar and config.toolbar is None:
            config.toolbar = DEFAULT_TOOLBARS

        self._config: CodeEditorConfig = config
        self._editor: QCodeEditor | None = None
        self._current_file: str | None = None
        self._initial_fingerprint: str | None = self._fingerprint(config.initial_text)

        self._highlighter: QStyleSyntaxHighlighter | None = None

        super().__init__(parent, config=config)

    def _setup_ui(self):
        super()._setup_ui()

        center_widget = QWidget(self)

        self._editor = QCodeEditor(center_widget)

        self.set_highlighter(self._config.highlighter, self._config.highlighter_args)
        self._editor.setCompleter(self._config.completer)
        self._editor.setAutoIndentation(self._config.auto_indent)
        self._editor.setAutoParentheses(self._config.auto_parentheses)
        self._editor.setTabReplace(self._config.tab_replace)
        self._editor.setTabReplaceSize(self._config.tab_size)
        if self._config.text_font_size and self._config.text_font_size > 0:
            self._editor.setFontSize(self._config.text_font_size)
        self._editor.setLineWrapMode(self._config.line_wrap_mode)
        if (
            self._config.line_wrap_mode == LineWrapMode.FixedPixelWidth
            or self._config.line_wrap_mode == LineWrapMode.FixedColumnWidth
        ):
            assert (
                self._config.line_wrap_width is not None
                and self._config.line_wrap_width > 0
            )
            self._editor.setLineWrapColumnOrWidth(self._config.line_wrap_width)

        self._editor.setWordWrapMode(self._config.word_wrap_mode)

        # noinspection PyArgumentList
        main_layout = QVBoxLayout()
        center_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._editor)
        self.setCentralWidget(center_widget)

        self.set_text(self._config.initial_text)
        self._update_fingerprint()
        self._update_title()

    def _on_close(self) -> bool:
        if not self.check_modification():
            return super()._on_close()

        # noinspection PyUnresolvedReferences
        msgbox = utils.MessageBoxConfig(
            title="Quit",
            text="There are unsaved changes, if you quit, all changes will be lost. Are you sure to quit?",
            buttons=utils.StandardButton.Yes | utils.StandardButton.No,
        ).create_messagebox(self)
        if msgbox.exec_() == utils.StandardButton.Yes:
            return super()._on_close()
        else:
            return False

    def get_text(self) -> str:
        return self._editor.toPlainText()

    def set_text(self, text: str | None):
        text = text or ""
        self._editor.setPlainText(text)

    def set_highlighter(
        self,
        highlighter: Type[QStyleSyntaxHighlighter] | None,
        args: list | tuple | dict | None = None,
    ):
        # noinspection PyTypeChecker
        self._config.highlighter = highlighter
        self._config.highlighter_args = args
        if self._highlighter is not None:
            # noinspection PyTypeChecker
            self._highlighter.setDocument(None)
            self._highlighter.deleteLater()
            self._highlighter = None
        self._highlighter = self.new_highlighter_instance(
            self._config.highlighter, self._config.highlighter_args
        )
        self._highlighter.setParent(self)
        self._editor.setHighlighter(self._highlighter)

    def get_highlighter(self) -> Type[QStyleSyntaxHighlighter] | None:
        return self._config.highlighter

    def set_completer(self, completer: QCompleter | None):
        self._config.completer = completer
        self._editor.setCompleter(self._config.completer)

    def get_completer(self) -> QCompleter | None:
        return self._config.completer

    def enable_auto_indent(self, enable: bool = True):
        self._config.auto_indent = enable
        self._editor.setAutoIndentation(self._config.auto_indent)

    def is_auto_indent_enabled(self) -> bool:
        return self._config.auto_indent

    def enable_auto_parentheses(self, enable: bool):
        self._config.auto_parentheses = enable
        self._editor.setAutoParentheses(self._config.auto_parentheses)

    def is_auto_parentheses_enabled(self) -> bool:
        return self._config.auto_parentheses

    def set_text_font_size(self, size: int | None):
        self._config.text_font_size = size
        if self._config.text_font_size and self._config.font_size > 0:
            self._editor.setFontSize(self._config.font_size)

    def set_tab(self, size: int = 4, tab_replace: bool = True):
        self._config.tab_size = size
        self._config.tab_replace = tab_replace
        self._editor.setTabReplace(self._config.tab_replace)
        self._editor.setTabReplaceSize(self._config.tab_size)

    def is_tab_replace_enabled(self) -> bool:
        return self._config.tab_replace

    def get_tab_size(self) -> int:
        return self._config.tab_size

    def set_wrap_mode(
        self,
        line_wrap: LineWrapMode | None = None,
        line_wrap_width: int | None = None,
        word_wrap_mode: WordWrapMode | None = None,
    ):
        if line_wrap is not None:
            self._config.line_wrap_mode = line_wrap
            self._editor.setLineWrapMode(self._config.line_wrap_mode)
        if line_wrap_width is not None and line_wrap_width > 0:
            self._config.line_wrap_width = line_wrap_width
            self._editor.setLineWrapColumnOrWidth(self._config.line_wrap_width)
        if word_wrap_mode is not None:
            self._config.word_wrap_mode = word_wrap_mode
            self._editor.setWordWrapMode(self._config.word_wrap_mode)

    def get_line_wrap_mode(self) -> LineWrapMode:
        return self._config.line_wrap_mode

    def get_line_wrap_width(self) -> int:
        return self._config.line_wrap_width

    def get_word_wrap_mode(self) -> WordWrapMode:
        return self._config.word_wrap_mode

    def set_code_formatter(
        self, formatter: BaseCodeFormatter | Callable[[str], str] | None
    ):
        assert (
            formatter is None
            or callable(formatter)
            or isinstance(formatter, BaseCodeFormatter)
        )
        self._config.code_formatter = formatter

    def get_code_formatter(self) -> BaseCodeFormatter | Callable[[str], str] | None:
        return self._config.code_formatter

    def set_file_filters(self, filters: str | None):
        assert filters is None or isinstance(filters, str)
        self._config.file_filters = filters

    def get_file_filters(self) -> str | None:
        return self._config.file_filters

    def set_start_dir(self, directory: str | None):
        assert directory is None or isinstance(directory, str)
        self._config.start_dir = directory

    def get_start_dir(self) -> str | None:
        return self._config.start_dir

    def set_show_filename_in_title(self, show: bool):
        self._config.show_filename_in_title = show

    def is_show_filename_in_title(self) -> bool:
        return self._config.show_filename_in_title

    def is_modified(self) -> bool:
        text = self.get_text()
        fingerprint = self._fingerprint(text)
        return fingerprint != self._initial_fingerprint

    def check_modification(self) -> bool:
        if not self._config.check_unsaved_changes:
            return False
        return self.is_modified()

    def open_file(self):
        if self.check_modification():
            # noinspection PyUnresolvedReferences
            ret = utils.show_question_message(
                self,
                message="There are unsaved changes, are you sure to continue",
                title="Confirm",
                buttons=utils.StandardButton.No | utils.StandardButton.Yes,
            )
            if ret != utils.StandardButton.Yes:
                return
        filepath = utils.get_open_file(
            self,
            title="Open File",
            start_dir=self._config.start_dir,
            filters=self._config.file_filters,
        )
        if not filepath:
            return

        try:
            new_text = utils.read_text_file(filepath, encoding="utf-8")
        except Exception as e:
            utils.show_exception_message(
                self,
                exception=e,
                title="Error",
                message=f"Failed to open file '{os.path.abspath(filepath)}': ",
                detail=True,
            )
            return
        self._current_file = os.path.abspath(filepath)
        self.set_text(new_text)
        self._update_fingerprint()
        self._update_title()

    def save_file(self):
        if not self._current_file:
            self.save_as_file()
            return

        if not self.check_modification():
            return

        try:
            utils.write_text_file(self._current_file, self.get_text(), encoding="utf-8")
        except Exception as e:
            utils.show_exception_message(
                self,
                exception=e,
                title="Error",
                message=f"Failed to save file '{os.path.abspath(self._current_file)}'",
            )
        else:
            self._update_fingerprint()

    def save_as_file(self):
        filepath = utils.get_save_file(
            self,
            title="Save File as",
            start_dir=self._config.start_dir,
            filters=self._config.file_filters,
        )
        if not filepath:
            return
        try:
            utils.write_text_file(filepath, self.get_text(), encoding="utf-8")
        except Exception as e:
            utils.show_exception_message(
                self,
                exception=e,
                title="Error",
                message=f"Failed to save file '{os.path.abspath(self._current_file)}'",
            )
        else:
            self._current_file = os.path.abspath(filepath)
            self._update_fingerprint()
            self._update_title()

    def format_code(self):
        if not self._config.code_formatter:
            return

        try:
            if isinstance(self._config.code_formatter, BaseCodeFormatter):
                formatted = self._config.code_formatter.format_code(self.get_text())
            else:
                formatted = self._config.code_formatter(self.get_text())
        except Exception as e:
            utils.show_exception_message(
                self,
                exception=e,
                title="Error",
                message="Failed to format current code: ",
            )
            return
        if isinstance(formatted, str):
            self.set_text(formatted)

    def redo(self):
        self._editor.redo()

    def undo(self):
        self._editor.undo()

    def copy(self):
        self._editor.copy()

    def cut(self):
        self._editor.cut()

    def paste(self):
        self._editor.paste()

    def select_all(self):
        self._editor.selectAll()

    def _update_fingerprint(self):
        self._initial_fingerprint = self._fingerprint(self.get_text())

    def _update_title(self):
        win_title = (self._config.title or "").strip()
        if self._config.show_filename_in_title:
            if not self._current_file:
                filename = "Untitled"
            else:
                filename = os.path.basename(self._current_file)
            win_title = f"{win_title} - {filename}".strip()
        self.setWindowTitle(win_title)

    @staticmethod
    def new_highlighter_instance(
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

    @staticmethod
    def _fingerprint(text: str | None) -> str | None:
        if not text:
            return None
        md5 = hashlib.md5()
        md5.update(text.encode("utf-8"))
        return md5.hexdigest()
