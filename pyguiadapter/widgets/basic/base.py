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
from ...utils import messagebox
from ...window import SimpleWindowEventListener

T = TypeVar("T")

CONFIRM_MSG = "Do you want to keep the changes?"
STANDALONE_EDITOR_BUTTON = "Edit"
STANDALONE_EDITOR_TITLE = "Parameter - {}"
LINE_WRAP_WIDTH = 88
INDENT_SIZE = 4
EDITOR_HEIGHT = 110
EDITOR_WIDTH = 230


@dataclasses.dataclass
class StandaloneCodeEditorConfig(object):
    """standalone编辑器配置类"""

    title: str = STANDALONE_EDITOR_TITLE
    """standalone编辑器窗口标题"""

    text_font_family: Optional[str] = None
    """standalone编辑器字体"""

    text_font_size: Optional[int] = None
    """standalone编辑器字体大小"""

    line_wrap_mode: LineWrapMode = LineWrapMode.NoWrap
    """standalone编辑器行折叠模式"""

    line_wrap_width: int = LINE_WRAP_WIDTH
    """standalone编辑器行折叠宽度"""

    word_wrap_mode: WordWrapMode = WordWrapMode.NoWrap
    """standalone编辑器字词折叠模式"""

    file_filters: Optional[str] = None
    """standalone编辑器文件对话框的文件过滤器"""

    start_dir: Optional[str] = None
    """standalone编辑器文件对话框的起始目录"""

    use_default_menus: bool = True
    """是否使用默认菜单栏"""

    excluded_menus: Tuple[str] = ()
    """禁用的默认菜单"""

    excluded_menu_actions: Tuple[Tuple[str, str]] = (
        (MENU_FILE, ACTION_SAVE),
        (MENU_FILE, ACTION_SAVE_AS),
    )
    """禁用的默认菜单项"""

    use_default_toolbar: bool = True
    """是否启用默认工具栏"""

    excluded_toolbar_actions: Tuple[str] = (
        ACTION_SAVE,
        ACTION_SAVE_AS,
    )
    """禁用的默认工具栏项"""

    confirm_dialog: bool = True
    """standalone编辑器退出时是否显示确认对话框"""

    confirm_dialog_title: str = CONFIRM_DIALOG_TITLE
    """确认对话框标题"""

    confirm_dialog_message: str = CONFIRM_MSG
    """确认对话框显示的内容"""


@dataclasses.dataclass(frozen=True)
class BaseCodeEditConfig(CommonParameterWidgetConfig):
    """BaseCodeEdit的配置类"""

    # 以下属性适用于inplace编辑器
    text_font_size: Optional[int] = None
    """inplace编辑器字体大小"""

    text_font_family: Optional[str] = None
    """inplace编辑器字体"""

    width: Optional[int] = EDITOR_WIDTH
    """inplace编辑器宽度"""

    height: Optional[int] = EDITOR_HEIGHT
    """inplace编辑器高度"""

    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth
    """inplace编辑器行折叠模式"""

    line_wrap_width: int = LINE_WRAP_WIDTH
    """inplace编辑器行折叠宽度"""

    word_wrap_mode: WordWrapMode = WordWrapMode.WordWrap
    """inplace编辑器字词折叠模式"""

    initial_text: Optional[str] = None
    """inplace编辑器的初始文本"""

    standalone_editor: bool = True
    """是否启用standalone编辑器"""

    standalone_editor_button: str = STANDALONE_EDITOR_BUTTON
    """standalone编辑器窗口打开按钮的文本"""

    standalone_editor_config: StandaloneCodeEditorConfig = StandaloneCodeEditorConfig()
    """standalone编辑器配置"""

    # 以下属性同时适用于inplace和standalone编辑器
    indent_size: int = INDENT_SIZE
    """缩进大小，该属性适用于inplace编辑器和standalone编辑器"""

    auto_indent: bool = True
    """是否自动缩进，该属性适用于inplace编辑器和standalone编辑器"""

    auto_parentheses: bool = True
    """是否自动匹配括号， 该属性适用于inplace编辑器和standalone编辑器"""

    formatter: Union[BaseCodeFormatter, Callable[[str], str], None] = None
    """代码格式化器，该属性适用于inplace编辑器和standalone编辑器"""

    highlighter: Optional[Type[QStyleSyntaxHighlighter]] = None
    """语法高亮器类，该属性适用于inplace编辑器和standalone编辑器"""

    highlighter_args: Union[dict, list, tuple, None] = None
    """语法高亮器参数，该属性适用于inplace编辑器和standalone编辑器"""

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

        self._inplace_editor: Optional[QCodeEditor] = None
        self._standalone_editor: Optional[CodeEditorWindow] = None

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            config: BaseCodeEditConfig = self.config
            self._value_widget = QWidget(self)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self._value_widget.setLayout(layout)

            self._inplace_editor = QCodeEditor(self._value_widget)
            layout.addWidget(self._inplace_editor)

            if config.standalone_editor:
                self._editor_button = QPushButton(self._value_widget)
                self._editor_button.setText(
                    config.standalone_editor_button or STANDALONE_EDITOR_BUTTON
                )
                # noinspection PyUnresolvedReferences
                self._editor_button.clicked.connect(self._on_open_standalone_editor)
                layout.addWidget(self._editor_button)

            # if config.min_height and config.min_height > 0:
            #     self._inplace_editor.setMinimumHeight(config.min_height)
            #
            # if config.min_width and config.min_width > 0:
            #     self._inplace_editor.setMinimumWidth(config.min_width)

            if config.height is not None and config.height >= 0:
                if config.height == 0:
                    self._inplace_editor.setVisible(False)
                self._inplace_editor.setFixedHeight(config.height)

            if config.width is not None and config.width >= 0:
                if config.width == 0:
                    self._inplace_editor.setVisible(False)
                self._inplace_editor.setFixedWidth(config.width)

            self._inplace_editor.setPlainText(config.initial_text or "")

            highlighter = create_highlighter(
                config.highlighter, config.highlighter_args
            )
            highlighter.setParent(self)
            self._inplace_editor.setHighlighter(highlighter)
            self._inplace_editor.setTabReplace(True)
            self._inplace_editor.setTabReplaceSize(config.indent_size)
            self._inplace_editor.setLineWrapMode(config.line_wrap_mode)
            if (
                config.line_wrap_width
                in (
                    LineWrapMode.FixedPixelWidth,
                    LineWrapMode.FixedColumnWidth,
                )
                and config.line_wrap_width > 0
            ):
                self._inplace_editor.setLineWrapWidth(config.line_wrap_width)

            self._inplace_editor.setWordWrapMode(config.word_wrap_mode)

            if config.text_font_size and config.text_font_size > 0:
                self._inplace_editor.setFontSize(config.text_font_size)

            if config.text_font_family and config.text_font_family.strip() != "":
                self._inplace_editor.setFontFamily(config.text_font_family)

        return self._value_widget

    def _on_open_standalone_editor(self):
        if self._standalone_editor is not None:
            self._standalone_editor.close()
            self._standalone_editor.deleteLater()
            self._standalone_editor = None

        config: BaseCodeEditConfig = self.config
        standalone_config = config.standalone_editor_config
        event_listener = SimpleWindowEventListener(
            on_close=self._on_standalone_editor_close
        )
        editor_config = CodeEditorConfig(
            initial_text=self._inplace_editor.toPlainText(),
            formatter=config.formatter,
            highlighter=config.highlighter,
            highlighter_args=config.highlighter_args,
            check_unsaved_changes=False,
            show_filename_in_title=False,
            title=standalone_config.title.format(self.parameter_name),
            auto_indent=config.auto_indent,
            auto_parentheses=config.auto_parentheses,
            file_filters=standalone_config.file_filters,
            start_dir=standalone_config.start_dir,
            line_wrap_mode=standalone_config.line_wrap_mode,
            line_wrap_width=standalone_config.line_wrap_width,
            word_wrap_mode=standalone_config.word_wrap_mode,
            text_font_size=standalone_config.text_font_size,
            text_font_family=standalone_config.text_font_family,
            tab_replace=True,
            tab_size=config.indent_size,
            no_file_mode=True,
            use_default_menus=standalone_config.use_default_menus,
            use_default_toolbar=standalone_config.use_default_toolbar,
            excluded_menus=standalone_config.excluded_menus,
            excluded_menu_actions=standalone_config.excluded_menu_actions,
            excluded_toolbar_actions=standalone_config.excluded_toolbar_actions,
        )
        self._standalone_editor = CodeEditorWindow(
            self, editor_config, listener=event_listener
        )
        self._standalone_editor.setWindowModality(Qt.WindowModal)
        self._standalone_editor.setAttribute(Qt.WA_DeleteOnClose, True)
        self._standalone_editor.destroyed.connect(self._on_standalone_editor_destroyed)
        self._standalone_editor.show()

    def _on_standalone_editor_close(self, editor: CodeEditorWindow) -> bool:
        standalone_config = self.config.standalone_editor_config
        if editor.is_modified():
            if not standalone_config.confirm_dialog:
                new_code_text = editor.get_text()
                self._inplace_editor.setPlainText(new_code_text)
                return True
            # noinspection PyUnresolvedReferences
            ret = messagebox.show_question_message(
                self,
                title=standalone_config.confirm_dialog_title,
                message=standalone_config.confirm_dialog_message,
                buttons=messagebox.Yes | messagebox.No,
            )
            if ret == messagebox.Yes:
                new_code_text = editor.get_text().rstrip()
                self._inplace_editor.setPlainText(new_code_text)
        return True

    def _on_standalone_editor_destroyed(self):
        self._standalone_editor = None

    def _do_format(self, code: str) -> Optional[str]:
        config: BaseCodeEditConfig = self.config
        if config.formatter:
            try:
                formatted = config.formatter.format_code(code)
                return formatted.rstrip()
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
                self._inplace_editor.setPlainText(formatted)
            else:
                self._inplace_editor.setPlainText(code_text)

    def get_value_from_widget(self) -> T:
        try:
            obj = self._get_data(self._inplace_editor.toPlainText())
        except Exception as e:
            raise ParameterError(
                parameter_name=self.parameter_name, message=str(e)
            ) from e
        return obj
