from __future__ import annotations

import dataclasses
import warnings
from abc import abstractmethod
from typing import Type, TypeVar, Callable, Tuple

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.QStyleSyntaxHighlighter import QStyleSyntaxHighlighter
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ..common import (
    CommonParameterWidget,
    CommonParameterWidgetConfig,
)
from ... import utils
from ...codeeditor import (
    BaseCodeFormatter,
    CodeEditorWindow,
    CodeEditorConfig,
    LineWrapMode,
    WordWrapMode,
    create_highlighter,
)
from ...codeeditor.constants import MENU_FILE, ACTION_SAVE, ACTION_SAVE_AS
from ...exceptions import ParameterError

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class BaseCodeEditConfig(CommonParameterWidgetConfig):
    font_size: int | None = None
    indent_size: int = 4
    min_height: int = 180
    highlighter: Type[QStyleSyntaxHighlighter] | None = None
    highlighter_args: dict | list | tuple | None = None
    editor_window: bool = True
    editor_button_text: str = "Edit"
    editor_title: str = "Edit - {}"
    auto_indent: bool = True
    auto_parentheses: bool = True
    formatter: BaseCodeFormatter | Callable[[str], str] | None = None
    file_filters: str | None = None
    start_dir: str | None = None
    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    line_wrap_width: int = 88
    word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap
    initial_text: str | None = None

    use_default_menus: bool = True
    use_default_toolbar: bool = True
    exclude_default_menus: Tuple[str] = ()
    exclude_default_menu_actions: Tuple[Tuple[str, str]] = (
        (MENU_FILE, ACTION_SAVE),
        (MENU_FILE, ACTION_SAVE_AS),
    )
    exclude_default_toolbar_actions: Tuple[str] = (
        ACTION_SAVE,
        ACTION_SAVE_AS,
    )

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseCodeEdit"]:
        pass


class BaseCodeEdit(CommonParameterWidget):
    ConfigClass = BaseCodeEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: BaseCodeEditConfig,
    ):

        self._value_widget: QWidget | None = None
        self._editor_button: QPushButton | None = None
        super().__init__(parent, parameter_name, config)

        self._editor: QCodeEditor | None = None
        self._code_editor: CodeEditorWindow | None = None

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            config: BaseCodeEditConfig = self.config
            self._value_widget = QWidget(self)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self._value_widget.setLayout(layout)

            self._editor = QCodeEditor(self._value_widget)
            layout.addWidget(self._editor)

            if config.editor_window:
                self._editor_button = QPushButton(self._value_widget)
                self._editor_button.setText(config.editor_button_text)
                # noinspection PyUnresolvedReferences
                self._editor_button.clicked.connect(self._on_open_code_editor)
                layout.addWidget(self._editor_button)

            if config.min_height and config.min_height > 0:
                self._editor.setMinimumHeight(config.min_height)

            if config.initial_text is not None:
                self._editor.setPlainText(config.initial_text)

            highlighter = self._inplace_editor_highlighter()
            highlighter.setParent(self)
            self._editor.setHighlighter(highlighter)
            self._editor.setTabReplace(True)
            self._editor.setTabReplaceSize(config.indent_size)
            self._editor.setLineWrapMode(config.line_wrap_mode)
            if (
                config.line_wrap_mode == LineWrapMode.FixedPixelWidth
                or config.line_wrap_mode == LineWrapMode.FixedColumnWidth
            ):
                if config.line_wrap_width > 0:
                    self._editor.setLineWrapWidth(config.line_wrap_width)
            self._editor.setWordWrapMode(config.word_wrap_mode)
            if config.font_size and config.font_size > 0:
                self._editor.setFontSize(config.font_size)

        return self._value_widget

    def _on_open_code_editor(self):
        if self._code_editor is not None:
            self._code_editor.close()
            self._code_editor.destroyed.disconnect(self._on_code_editor_destroyed)
            self._code_editor.deleteLater()
            self._code_editor = None
        config: BaseCodeEditConfig = self.config
        code_editor_config = CodeEditorConfig(
            initial_text=self._editor.toPlainText(),
            formatter=config.formatter,
            highlighter=config.highlighter,
            highlighter_args=config.highlighter_args,
            check_unsaved_changes=False,
            show_filename_in_title=False,
            title=config.editor_title.format(self.parameter_name),
            auto_indent=config.auto_indent,
            auto_parentheses=config.auto_parentheses,
            file_filters=config.file_filters,
            start_dir=config.start_dir,
            line_wrap_mode=config.line_wrap_mode,
            line_wrap_width=config.line_wrap_width,
            word_wrap_mode=config.word_wrap_mode,
            font_size=config.font_size,
            tab_replace=True,
            tab_size=config.indent_size,
            no_file_mode=True,
            on_close=self._on_code_editor_close,
            use_default_menus=config.use_default_menus,
            use_default_toolbar=config.use_default_toolbar,
            exclude_default_menus=config.exclude_default_menus,
            exclude_default_menu_actions=config.exclude_default_menu_actions,
            exclude_default_toolbar_actions=config.exclude_default_toolbar_actions,
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
        config: BaseCodeEditConfig = self.config
        if config.formatter:
            try:
                return config.formatter.format_code(code)
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
        config: BaseCodeEditConfig = self.config
        return create_highlighter(config.highlighter, config.highlighter_args)
