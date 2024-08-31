from __future__ import annotations

import dataclasses
import hashlib
import os.path
from typing import Callable

from qtpy.QtGui import QIcon, QAction
from qtpy.QtWidgets import (
    QMainWindow,
    QWidget,
    QCompleter,
    QVBoxLayout,
    QMenu,
    QToolBar,
    QMessageBox,
)
from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.QStyleSyntaxHighlighter import QSyntaxHighlighter
from qtawesome import icon

from ... import utils

CodeFormatter = Callable[[str], str]


@dataclasses.dataclass
class CodeEditorConfig(object):
    title: str = "Editor"
    icon: utils.IconType = None
    highlighter: QSyntaxHighlighter | None = None
    completer: QCompleter | None = None
    tab_size: int = 4
    tab_replace: bool = True
    initial_text: str = ""
    code_formatter: CodeFormatter | None = None
    file_filters: str | None = None
    start_dir: str | None = None
    check_unsaved_changes: bool = True
    show_filename_on_title: bool = True


class CodeEditor(QMainWindow):
    def __init__(self, parent: QWidget | None, config: CodeEditorConfig | None = None):
        super().__init__(parent)

        config = config or CodeEditorConfig()

        self._title: str = config.title or ""
        self._code_formatter = config.code_formatter
        self._file_filters = config.file_filters
        self._start_dir = config.start_dir
        self._check_unsaved_changes = config.check_unsaved_changes
        self._show_filename_on_title = config.show_filename_on_title

        self._editor: QCodeEditor | None = None

        self._current_file: str | None = None
        self._initial_fingerprint: str | None = self._text_fingerprint(
            config.initial_text
        )

        self._action_open = QAction(self)
        self._action_open.setIcon(icon("fa.folder-open-o"))
        self._action_open.setText("Open")
        self._action_open.triggered.connect(self.open_file)

        self._action_save = QAction(self)
        self._action_save.setIcon(icon("fa.save"))
        self._action_save.setText("Save")

        menu_file = QMenu(self)
        menu_file.setTitle("File")
        menu_file.addAction(self._action_open)
        menu_file.addAction(self._action_save)

        menu_edit = QMenu(self)
        menu_edit.setTitle("Edit")

        self._builtin_menus = (menu_file, menu_edit)

        self._setup_ui(config)

    def _setup_ui(self, config: CodeEditorConfig):
        center_widget = QWidget(self)
        self._editor = QCodeEditor(center_widget)
        main_layout = QVBoxLayout(center_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._editor)
        self.setCentralWidget(center_widget)

        self.update_title()
        win_icon = utils.get_icon(config.icon) or QIcon()
        self.setWindowIcon(win_icon)
        self.set_highlighter(config.highlighter)
        self.set_completer(config.completer)
        self.set_tab(config.tab_size, config.tab_replace)
        self.set_text(config.initial_text)

        for menu in self._builtin_menus:
            self.menuBar().addMenu(menu)

    def get_text(self) -> str:
        return self._editor.toPlainText()

    def set_text(self, text: str | None):
        text = text or ""
        self._initial_fingerprint = self._text_fingerprint(text)
        self._editor.setPlainText(text)

    def set_highlighter(self, highlighter: QSyntaxHighlighter | None):
        # noinspection PyTypeChecker
        self._editor.setHighlighter(highlighter)

    def set_completer(self, completer: QCompleter | None):
        self._editor.setCompleter(completer)

    def set_tab(self, size: int = 4, tab_replace: bool = True):
        self._editor.setTabReplace(tab_replace)
        self._editor.setTabReplaceSize(size)

    def set_code_formatter(self, formatter: CodeFormatter | None):
        self._code_formatter = formatter

    def set_file_filters(self, filters: str | None):
        self._file_filters = filters

    def open_file(self):
        if self._check_unsaved_changes and self.is_modified():
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
            start_dir=self._start_dir,
            filters=self._file_filters,
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
        self.update_title()

    def save_file(self):
        pass

    def new_file(self):
        pass

    def format_code(self):
        if not self._code_formatter:
            return
        formatted = self._code_formatter(self.get_text())
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

    def delete(self):
        self._editor.delete()

    def select_all(self):
        self._editor.selectAll()

    def quit(self):
        pass

    def is_modified(self) -> bool:
        text = self.get_text()
        fingerprint = self._text_fingerprint(text)
        return fingerprint != self._initial_fingerprint

    def update_title(self):
        win_title = self._title.strip()
        if self._show_filename_on_title:
            if not self._current_file:
                filename = "Untitled"
            else:
                filename = os.path.basename(self._current_file)
            win_title = f"{win_title} - {filename}".strip()
        self.setWindowTitle(win_title)

    @staticmethod
    def _text_fingerprint(text: str | None) -> str | None:
        if not text:
            return None
        md5 = hashlib.md5()
        md5.update(text.encode("utf-8"))
        return md5.hexdigest()
