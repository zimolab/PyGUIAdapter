from __future__ import annotations

import dataclasses
import warnings
from abc import abstractmethod
from typing import Type, TypeVar, Callable

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ..codeeditor import (
    BaseCodeFormatter,
    LineWrapMode,
    WordWrapMode,
    CodeEditorWindow,
    CodeEditorConfig,
)
from ..common import (
    CommonParameterWidget,
    CommonParameterWidgetConfig,
)
from ...exceptions import ParameterError
from ... import utils

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class BaseDataEditConfig(CommonParameterWidgetConfig):
    font_size: int | None = None
    indent_size: int = 4
    min_height: int = 180
    highlighter: Type[QStyleSyntaxHighlighter] | None = None
    highlighter_args: dict | list | tuple | None = None
    enable_code_editor: bool = True
    editor_button_text: str = "Edit"
    editor_title: str = "Edit - {}"
    auto_indent: bool = True
    auto_parentheses: bool = True
    code_formatter: BaseCodeFormatter | Callable[[str], str] | None = None
    file_filters: str | None = None
    start_dir: str | None = None
    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    line_wrap_width: int = 88
    word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap
    initial_text: str | None = None

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseDataEdit"]:
        pass


class BaseDataEdit(CommonParameterWidget):
    Self = TypeVar("Self", bound="BaseDataEdit")
    ConfigClass = BaseDataEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BaseDataEditConfig,
    ):

        self._config: BaseDataEditConfig = config
        self._value_widget: QWidget | None = None
        self._editor_button: QPushButton | None = None
        super().__init__(parent, parameter_name, config)

        self._editor: QCodeEditor | None = None
        self._code_editor: CodeEditorWindow | None = None

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self._value_widget.setLayout(layout)

            self._editor = QCodeEditor(self._value_widget)
            layout.addWidget(self._editor)

            if self._config.enable_code_editor:
                self._editor_button = QPushButton(self._value_widget)
                self._editor_button.setText(self._config.editor_button_text)
                self._editor_button.clicked.connect(self._on_open_code_editor)
                layout.addWidget(self._editor_button)

            self._setup_value_widget()

        return self._value_widget

    def _setup_value_widget(self):
        if self._config.min_height and self._config.min_height > 0:
            self._editor.setMinimumHeight(self._config.min_height)

        if self._config.initial_text is not None:
            self._editor.setPlainText(self._config.initial_text)

        highlighter = self._inplace_editor_highlighter()
        highlighter.setParent(self)
        self._editor.setHighlighter(highlighter)
        self._editor.setTabReplace(True)
        self._editor.setTabReplaceSize(self._config.indent_size)
        self._editor.setLineWrapMode(self._config.line_wrap_mode)
        if (
            self._config.line_wrap_mode == LineWrapMode.FixedPixelWidth
            or self._config.line_wrap_mode == LineWrapMode.FixedColumnWidth
        ):
            if self._config.line_wrap_width > 0:
                self._editor.setLineWrapWidth(self._config.line_wrap_width)
        self._editor.setWordWrapMode(self._config.word_wrap_mode)
        if self._config.font_size and self._config.font_size > 0:
            self._editor.setFontSize(self._config.font_size)

    def _on_open_code_editor(self):
        if self._code_editor is not None:
            self._code_editor.close()
            self._code_editor.destroyed.disconnect(self._on_code_editor_destroyed)
            self._code_editor.deleteLater()
            self._code_editor = None

        code_editor_config = CodeEditorConfig(
            initial_text=self._editor.toPlainText(),
            code_formatter=self._config.code_formatter,
            highlighter=self._config.highlighter,
            highlighter_args=self._config.highlighter_args,
            check_unsaved_changes=False,
            show_filename_in_title=False,
            title=self._config.editor_title.format(self.parameter_name),
            auto_indent=self._config.auto_indent,
            auto_parentheses=self._config.auto_parentheses,
            file_filters=self._config.file_filters,
            start_dir=self._config.start_dir,
            line_wrap_mode=self._config.line_wrap_mode,
            line_wrap_width=self._config.line_wrap_width,
            word_wrap_mode=self._config.word_wrap_mode,
            font_size=self._config.font_size,
            tab_replace=True,
            tab_size=self._config.indent_size,
            on_close=self._on_code_editor_close,
        )
        self._code_editor = CodeEditorWindow(self, code_editor_config)
        self._code_editor.setWindowModality(Qt.WindowModal)
        self._code_editor.setAttribute(Qt.WA_DeleteOnClose, True)
        self._code_editor.destroyed.connect(self._on_code_editor_destroyed)
        self._code_editor.show()

    def _on_code_editor_close(self, code_editor: CodeEditorWindow) -> bool:
        if code_editor.is_modified():
            # noinspection PyUnresolvedReferences
            ret = utils.show_question_message(
                self,
                title="Confirm",
                message="Do you want to accept the changes?",
                buttons=utils.StandardButton.Yes | utils.StandardButton.No,
            )
            if ret == utils.StandardButton.Yes:
                new_text = code_editor.get_text()
                self._editor.setPlainText(new_text)
        return True

    def _on_code_editor_destroyed(self):
        self._code_editor = None

    def _do_format(self, code: str) -> str | None:
        if self._config.code_formatter:
            try:
                return self._config.code_formatter.format_code(code)
            except Exception as e:
                warnings.warn(f"Failed to format code: {e}")
            return None
        return None

    @abstractmethod
    def to_data(self, text: str) -> T:
        pass

    @abstractmethod
    def from_data(self, data: T) -> str:
        pass

    def set_value_to_widget(self, value: T):
        try:
            code_text = self.from_data(value)
        except Exception as e:
            raise ParameterError(
                parameter_name=self.parameter_name, message=str(e)
            ) from e
        else:
            formatted = self._do_format(code_text)
            if formatted is not None:
                self._editor.setPlainText(formatted)
            else:
                self._editor.setPlainText(code_text)

    def get_value_from_widget(self) -> T:
        try:
            obj = self.to_data(self._editor.toPlainText())
        except Exception as e:
            raise ParameterError(
                parameter_name=self.parameter_name, message=str(e)
            ) from e
        return obj

    def _inplace_editor_highlighter(self) -> QStyleSyntaxHighlighter | None:
        return CodeEditorWindow.new_highlighter_instance(
            self._config.highlighter, self._config.highlighter_args
        )
