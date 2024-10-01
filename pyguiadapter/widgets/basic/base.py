import dataclasses
import warnings
from abc import abstractmethod
from typing import Type, TypeVar, Callable, Tuple, Optional, Union

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
from ...codeeditor.constants import (
    MENU_FILE,
    ACTION_SAVE,
    ACTION_SAVE_AS,
    CONFIRM_DIALOG_TITLE,
)
from ...exceptions import ParameterError
from ...window import BaseWindowStateListener

T = TypeVar("T")

ACCEPT_CHANGES_MSG = "Do you want to keep the changes?"
EDITOR_BUTTON_TEXT = "Edit"
EDITOR_TITLE = "Edit - {}"
INDENT_SIZE = 4
MIN_HEIGHT = 180


@dataclasses.dataclass(frozen=True)
class BaseCodeEditConfig(CommonParameterWidgetConfig):
    font_size: Optional[int] = None
    indent_size: int = INDENT_SIZE
    min_height: int = MIN_HEIGHT
    highlighter: Optional[Type[QStyleSyntaxHighlighter]] = None
    highlighter_args: Union[dict, list, tuple, None] = None
    editor_window: bool = True
    editor_button_text: str = EDITOR_BUTTON_TEXT
    editor_title: str = EDITOR_TITLE
    editor_line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    editor_line_wrap_width: int = 88
    editor_word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap
    auto_indent: bool = True
    auto_parentheses: bool = True
    formatter: Union[BaseCodeFormatter, Callable[[str], str], None] = None
    file_filters: Optional[str] = None
    start_dir: Optional[str] = None
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth
    line_wrap_width: int = 88
    word_wrap_mode: WordWrapMode = WordWrapMode.WordWrap
    initial_text: Optional[str] = None
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
    confirm_dialog: bool = True
    confirm_dialog_title: str = CONFIRM_DIALOG_TITLE
    accept_changes_message: str = ACCEPT_CHANGES_MSG

    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseCodeEdit"]:
        pass


class BaseCodeEdit(CommonParameterWidget):
    ConfigClass = BaseCodeEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: BaseCodeEditConfig,
    ):

        self._value_widget: Optional[QWidget] = None
        self._editor_button: Optional[QPushButton] = None
        super().__init__(parent, parameter_name, config)

        self._editor: Optional[QCodeEditor] = None
        self._code_editor: Optional[CodeEditorWindow] = None

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
                self._editor_button.setText(
                    config.editor_button_text or EDITOR_BUTTON_TEXT
                )
                # noinspection PyUnresolvedReferences
                self._editor_button.clicked.connect(self._on_open_code_editor)
                layout.addWidget(self._editor_button)

            if config.min_height and config.min_height > 0:
                self._editor.setMinimumHeight(config.min_height)

            if config.initial_text is not None:
                self._editor.setPlainText(config.initial_text)

            highlighter = create_highlighter(
                config.highlighter, config.highlighter_args
            )
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
        editor_title = config.editor_title or EDITOR_TITLE
        listener = BaseWindowStateListener()
        listener.on_close = self._on_code_editor_close
        code_editor_config = CodeEditorConfig(
            initial_text=self._editor.toPlainText(),
            formatter=config.formatter,
            highlighter=config.highlighter,
            highlighter_args=config.highlighter_args,
            check_unsaved_changes=False,
            show_filename_in_title=False,
            title=editor_title.format(self.parameter_name),
            auto_indent=config.auto_indent,
            auto_parentheses=config.auto_parentheses,
            file_filters=config.file_filters,
            start_dir=config.start_dir,
            line_wrap_mode=config.editor_line_wrap_mode,
            line_wrap_width=config.editor_line_wrap_width,
            word_wrap_mode=config.editor_word_wrap_mode,
            font_size=config.font_size,
            tab_replace=True,
            tab_size=config.indent_size,
            no_file_mode=True,
            use_default_menus=config.use_default_menus,
            use_default_toolbar=config.use_default_toolbar,
            exclude_default_menus=config.exclude_default_menus,
            exclude_default_menu_actions=config.exclude_default_menu_actions,
            exclude_default_toolbar_actions=config.exclude_default_toolbar_actions,
        )
        self._code_editor = CodeEditorWindow(
            self, code_editor_config, listener=listener
        )
        self._code_editor.setWindowModality(Qt.WindowModal)
        self._code_editor.setAttribute(Qt.WA_DeleteOnClose, True)
        self._code_editor.destroyed.connect(self._on_code_editor_destroyed)
        self._code_editor.show()

    def _on_code_editor_close(self, code_editor: CodeEditorWindow) -> bool:
        config: BaseCodeEditConfig = self.config
        if code_editor.is_modified():
            if not config.confirm_dialog:
                new_text = code_editor.get_text()
                self._editor.setPlainText(new_text)
                return True
            # noinspection PyUnresolvedReferences
            ret = utils.show_question_message(
                self,
                title=config.confirm_dialog_title or CONFIRM_DIALOG_TITLE,
                message=config.accept_changes_message or ACCEPT_CHANGES_MSG,
                buttons=utils.StandardButton.Yes | utils.StandardButton.No,
            )
            if ret == utils.StandardButton.Yes:
                new_text = code_editor.get_text()
                self._editor.setPlainText(new_text)
        return True

    def _on_code_editor_destroyed(self):
        self._code_editor = None

    def _do_format(self, code: str) -> Optional[str]:
        config: BaseCodeEditConfig = self.config
        if config.formatter:
            try:
                return config.formatter.format_code(code)
            except Exception as e:
                warnings.warn(f"Failed to format code: {e}")
            return None
        return None

    @abstractmethod
    def _get_data(self, text: str) -> T:
        pass

    @abstractmethod
    def _set_data(self, data: T) -> str:
        pass

    def set_value_to_widget(self, value: T):
        try:
            code_text = self._set_data(value)
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
            obj = self._get_data(self._editor.toPlainText())
        except Exception as e:
            raise ParameterError(
                parameter_name=self.parameter_name, message=str(e)
            ) from e
        return obj
