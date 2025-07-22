"""
@Time    : 2024.10.20
@File    : inputdialog.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 输入对话框相关的工具函数
"""

import ast
import json
from abc import abstractmethod
from typing import Optional, Any, Tuple
from typing import (
    Union,
    List,
    Literal,
    Sequence,
    cast,
    Type,
)

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters import QJSONHighlighter, QPythonHighlighter
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import (
    QLineEdit,
    QInputDialog,
    QColorDialog,
    QTextEdit,
)
from qtpy.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

from ._core import PyLiteralType
from ._ui import get_icon
from ._ui import to_qcolor, convert_color, IconType
from .dialog import BaseCustomDialog
from .messagebox import show_critical_message

# 输入控件的回显模式
# 常量别名，方便开发者直接导入使用
EchoMode = QLineEdit.EchoMode
PasswordEchoMode = EchoMode.Password
PasswordEchoOnEdit = EchoMode.PasswordEchoOnEdit
NormalEchoMode = EchoMode.Normal
NoEcho = EchoMode.NoEcho


def input_integer(
    parent: Optional[QWidget],
    title: str = "Input Integer",
    label: str = "",
    value: int = 0,
    min_value: int = -2147483647,
    max_value: int = 2147483647,
    step: int = 1,
) -> Optional[int]:
    """
    弹出一个整数输入对话框，并返回输入的整数值。

    Args:
        parent: 父窗口
        title: 对话框标题
        label: 提示标签
        value: 初始值
        min_value: 最大值
        max_value: 最小值
        step: 单次增加的步长

    Returns:
        输入的整数值，如果用户取消输入则返回 None。
    """
    ret_val, ok = QInputDialog.getInt(
        parent, title, label, value, min_value, max_value, step
    )
    if not ok:
        return None
    return ret_val


def input_float(
    parent: Optional[QWidget],
    title: str = "Input Float",
    label: str = "",
    value: float = 0.0,
    min_value: float = -2147483647.0,
    max_value: float = 2147483647.0,
    decimals: int = 3,
    step: float = 1.0,
) -> Optional[float]:
    """
    弹出一个浮点数输入对话框，并返回输入的浮点数值。

    Args:
        parent: 父窗口
        title: 对话框标题
        label: 提示标签
        value: 初始值
        min_value: 最小值
        max_value: 最大值
        decimals: 小数位数
        step: 单次增加的步长

    Returns:
        输入的浮点数值，如果用户取消输入则返回 None。
    """
    value = float(value)
    min_value = float(min_value)
    max_value = float(max_value)
    ret_val, ok = QInputDialog.getDouble(
        parent,
        title,
        label,
        value,
        min_value,
        max_value,
        decimals,
        Qt.WindowFlags(),
        step,
    )
    if not ok:
        return None
    return ret_val


def input_text(
    parent: Optional[QWidget],
    title: str = "Input Text",
    label: str = "",
    text: str = "",
):
    """
    弹出一个多行文本输入对话框，并返回输入的文本。

    Args:
        parent: 父窗口
        title: 对话框标题
        label: 提示标签
        text:  初始文本

    Returns:
        输入的文本，如果用户取消输入则返回 None。
    """
    text, ok = QInputDialog.getMultiLineText(parent, title, label, text)
    if not ok:
        return None
    return text


def input_string(
    parent: Optional[QWidget],
    title: str = "Input Text",
    label: str = "",
    echo: Optional[EchoMode] = None,
    text: str = "",
) -> Optional[str]:
    """
    弹出一个单行文本输入对话框，并返回输入的文本。

    Args:
        parent: 父窗口
        title: 对话框标题
        label: 提示标签
        echo:  回显模式，默认为 None，即使用 QLineEdit.Normal 回显模式
        text:  初始文本

    Returns:
        输入的文本，如果用户取消输入则返回 None。
    """
    if echo is None:
        echo = EchoMode.Normal
    text, ok = QInputDialog.getText(parent, title, label, echo, text)
    if ok:
        return text
    return None


def select_item(
    parent: Optional[QWidget],
    items: List[str],
    title: str = "Select Item",
    label: str = "",
    current: int = 0,
    editable: bool = False,
) -> Optional[str]:
    """
    弹出一个选项列表对话框，并返回用户选择的选项。

    Args:
        parent: 父窗口
        items: 选项列表
        title: 对话框标题
        label: 提示标签
        current: 当前选择的选项索引
        editable: 是否允许编辑

    Returns:
        用户选择的选项，如果用户取消输入则返回 None。
    """
    ret_val, ok = QInputDialog.getItem(
        parent, title, label, items, current, editable=editable
    )
    if not ok:
        return None
    return ret_val


def input_color(
    parent: Optional[QWidget],
    initial: Union[QColor, str, tuple] = "white",
    title: str = "",
    alpha_channel: bool = True,
    return_type: Literal["tuple", "str", "QColor"] = "str",
) -> Union[Tuple[int, int, int], Tuple[int, int, int, int], str, QColor, None]:
    initial = to_qcolor(initial)
    """
    弹出一个颜色选择对话框，并返回用户选择的颜色。

    Args:
        parent: 父窗口
        initial: 初始颜色，可以是 QColor 对象，也可以是字符串表示的颜色值，也可以是元组表示的颜色值
        title: 对话框标题
        alpha_channel: 是否显示 alpha 通道
        return_type: 返回值类型，可以是 "tuple"，"str"，"QColor" 之一

    Returns:
        用户选择的颜色，如果用户取消输入则返回 None。
    """
    if alpha_channel:
        ret_val = QColorDialog.getColor(
            initial, parent, title, options=QColorDialog.ShowAlphaChannel
        )
    else:
        ret_val = QColorDialog.getColor(initial, parent, title)
    if ret_val.isValid():
        return convert_color(ret_val, return_type, alpha_channel)
    return None


LineWrapMode = QTextEdit.LineWrapMode


class UniversalInputDialog(BaseCustomDialog):
    """
    通用输入对话框基类，用于实现自定义输入对话框。
    """

    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        **kwargs,
    ):
        """
        构造函数，创建自定义输入对话框。
        Args:
            parent:  父窗口
            title:  对话框标题
            icon:  对话框图标
            size:  对话框大小
            ok_button_text: 确定按钮文本
            cancel_button_text:  取消按钮文本
            **kwargs:  其他参数
        """
        super().__init__(parent, **kwargs)
        self._title = title or ""
        self._icon = icon
        self._size = size
        self._ok_button_text: str = ok_button_text
        self._cancel_button_text: Optional[str] = cancel_button_text

        self._layout: QVBoxLayout = QVBoxLayout()
        self._main_widget: Optional[QWidget] = None
        self._ok_button: QPushButton = QPushButton(self)
        self._cancel_button: Optional[QPushButton] = None

        self.setLayout(self._layout)

        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(self._title)
        icon = get_icon(self._icon)
        if icon:
            self.setWindowIcon(icon)
        if self._size:
            self.resize(*self._size)
        if self._main_widget is None:
            main_widget = self.create_main_widget()
            main_widget.setParent(self)
            self._main_widget = main_widget
        self._layout.addWidget(self._main_widget)
        self._setup_buttons()

    @abstractmethod
    def create_main_widget(self) -> QWidget:
        """
        创建主部件，子类必须实现。

        Returns:
            主部件
        """
        pass

    def _setup_buttons(self):
        self._ok_button.setText(self._ok_button_text)
        # noinspection PyUnresolvedReferences
        self._ok_button.clicked.connect(self.on_accept)
        if self._cancel_button_text:
            self._cancel_button = QPushButton(self)
            self._cancel_button.setText(self._cancel_button_text)
            # noinspection PyUnresolvedReferences
            self._cancel_button.clicked.connect(self.on_reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self._ok_button)
        if self._cancel_button_text:
            button_layout.addWidget(self._cancel_button)
        self._layout.addLayout(button_layout)

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()

    @abstractmethod
    def get_result(self) -> Any:
        """
        获取输入结果，子类必须实现。

        Returns:
            输入结果
        """
        pass

    @classmethod
    def new_instance(cls, parent: QWidget, **kwargs) -> "UniversalInputDialog":
        """
        创建新的实例。

        Args:
            parent: 父窗口
            **kwargs: 构造函数参数

        Returns:
            新的实例
        """
        return super().new_instance(parent, **kwargs)


class CodeEditDialog(UniversalInputDialog):
    """
    代码编辑器输入对话框。
    """

    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (600, 400),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        initial_text: str = "",
        auto_indent: bool = True,
        indent_size: int = 4,
        auto_parentheses: bool = True,
        line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth,
        line_wrap_width: int = 88,
        font_family: Union[str, Sequence[str], None] = None,
        font_size: Optional[int] = None,
        **kwargs,
    ):
        """
        构造函数。

        Args:
            parent: 父窗口
            title:  对话框标题
            icon:  对话框图标
            size:  对话框大小
            ok_button_text: 确定按钮文本
            cancel_button_text:  取消按钮文本
            initial_text:  初始文本
            auto_indent:  自动缩进
            indent_size:  缩进大小
            auto_parentheses:  自动括号匹配
            line_wrap_mode:  换行模式
            line_wrap_width:  换行宽度
            font_family:  字体
            font_size:  字体大小
            **kwargs:  其他参数
        """
        self._initial_text = initial_text
        self._auto_indent = auto_indent
        self._indent_size = indent_size
        self._auto_parentheses = auto_parentheses
        self._line_wrap_mode = line_wrap_mode
        self._line_wrap_width = line_wrap_width
        self._font_family = font_family
        self._font_size = font_size

        super().__init__(
            parent, title, icon, size, ok_button_text, cancel_button_text, **kwargs
        )

    def create_main_widget(self) -> QCodeEditor:
        main_widget = QCodeEditor(self)
        main_widget.setTabReplace(True)
        main_widget.setTabReplaceSize(self._indent_size)
        main_widget.setAutoIndentation(self._auto_indent)
        main_widget.setAutoParentheses(self._auto_parentheses)
        main_widget.setLineWrapMode(self._line_wrap_mode)
        if self._line_wrap_mode in (
            LineWrapMode.FixedPixelWidth,
            LineWrapMode.FixedColumnWidth,
        ):
            main_widget.setLineWrapColumnOrWidth(self._line_wrap_width)
        if self._initial_text:
            main_widget.setPlainText(self._initial_text)
        if self._font_family:
            font_size = main_widget.fontSize()
            font: QFont = main_widget.font()
            if isinstance(self._font_family, str):
                font.setFamily(self._font_family)
            else:
                font.setFamilies(self._font_family)
            main_widget.setFont(font)
            main_widget.setFontSize(font_size)

        if self._font_size and self._font_size > 0:
            main_widget.setFontSize(self._font_size)

        return main_widget

    def get_result(self) -> str:
        return self._main_widget.toPlainText()


class ObjectInputDialog(CodeEditDialog):
    """
    对象输入对话框基类。
    """

    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (600, 400),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        initial_text: str = "",
        auto_indent: bool = True,
        indent_size: int = 4,
        auto_parentheses: bool = True,
        line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth,
        line_wrap_width: int = 88,
        font_family: Union[str, Sequence[str], None] = None,
        font_size: Optional[int] = None,
        **kwargs,
    ):
        """
        构造函数。

        Args:
            parent: 父窗口
            title:  对话框标题
            icon:  对话框图标
            size:  对话框大小
            ok_button_text: 确定按钮文本
            cancel_button_text:  取消按钮文本
            initial_text:  初始文本
            auto_indent:  自动缩进
            indent_size:  缩进大小
            auto_parentheses:  自动括号匹配
            line_wrap_mode:  换行模式
            line_wrap_width:  换行宽度
            font_family:  字体
            font_size:  字体大小
            **kwargs:  其他参数
        """
        super().__init__(
            parent,
            title,
            icon,
            size,
            ok_button_text,
            cancel_button_text,
            initial_text,
            auto_indent,
            indent_size,
            auto_parentheses,
            line_wrap_mode,
            line_wrap_width,
            font_family,
            font_size,
            **kwargs,
        )
        self._current_value: Any = None

    @abstractmethod
    def get_object(self) -> Any:
        """
        获取输入的对象。子类必须实现。

        Returns:
            输入的对象。
        """
        pass

    def on_accept(self):
        try:
            current_value = self.get_object()
        except Exception as e:
            show_critical_message(self, f"{type(e).__name__}: {e}", title="Error")
        else:
            self._current_value = current_value
            self.accept()

    def get_result(self) -> Any:
        return self._current_value


class JsonInputDialog(ObjectInputDialog):
    """
    JSON 输入对话框，从用户输入的 JSON 文本获得 Python 对象。
    """

    def create_main_widget(self) -> QCodeEditor:
        editor = super().create_main_widget()
        highlighter = QJSONHighlighter(editor)
        editor.setHighlighter(highlighter)
        return editor

    def get_object(self) -> Any:
        """
        获取输入的 JSON 对象。

        Returns:
            输入的 JSON 对象。

        Raises:
            Exception: 输入的文本不是合法的 JSON 文本时抛出异常。
        """
        editor = cast(QCodeEditor, self._main_widget)
        text = editor.toPlainText()
        if text.strip() == "":
            self._current_value = None
            self.accept()
            return
        return json.loads(text)


class PyLiteralInputDialog(ObjectInputDialog):
    """
    Python 字面量输入对话框，从用户输入的python字面量代码获得 Python 对象（使用ast.literal_eval()）。
    """

    def create_main_widget(self) -> QCodeEditor:
        editor = super().create_main_widget()
        highlighter = QPythonHighlighter(editor)
        editor.setHighlighter(highlighter)
        return editor

    def get_object(self) -> Any:
        """
        获取输入的 Python 字面量对象。

        Returns:
            输入的 Python 字面量对象。

        Raises:
              Exception: 输入的文本不是合法的python字面量代码时抛出异常。
        """
        editor = cast(QCodeEditor, self._main_widget)
        text = editor.toPlainText()
        if text.strip() == "":
            self._current_value = None
            self.accept()
            return
        return ast.literal_eval(text)


def input_json_object(
    parent: Optional[QWidget],
    title: str = "Input Json",
    icon: IconType = None,
    size: Tuple[int, int] = (600, 400),
    ok_button_text: str = "Ok",
    cancel_button_text: Optional[str] = "Cancel",
    initial_text: str = "",
    auto_indent: bool = True,
    indent_size: int = 4,
    auto_parentheses: bool = True,
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth,
    line_wrap_width: int = 88,
    font_family: Union[str, Sequence[str], None] = None,
    font_size: Optional[int] = None,
    **kwargs,
) -> Any:
    """
    弹出一个 JSON 输入对话框，并返回用户输入的 JSON 对象。

    Args:
        parent:  父窗口
        title:  对话框标题
        icon:  对话框图标
        size:  对话框大小
        ok_button_text: 确定按钮文本
        cancel_button_text:  取消按钮文本
        initial_text:  初始文本
        auto_indent:  自动缩进
        indent_size:  缩进大小
        auto_parentheses:  自动括号匹配
        line_wrap_mode:  换行模式
        line_wrap_width:  换行宽度
        font_family:  字体
        font_size:  字体大小
        **kwargs:  其他参数

    Returns:
        用户输入的 JSON 对象，如果用户取消输入则返回 None。

    Raises:
        Exception: 输入的文本不是合法的 JSON 文本时抛出异常。
    """
    return JsonInputDialog.show_and_get_result(
        parent,
        title=title,
        icon=icon,
        size=size,
        ok_button_text=ok_button_text,
        cancel_button_text=cancel_button_text,
        initial_text=initial_text,
        auto_indent=auto_indent,
        indent_size=indent_size,
        auto_parentheses=auto_parentheses,
        line_wrap_mode=line_wrap_mode,
        line_wrap_width=line_wrap_width,
        font_family=font_family,
        font_size=font_size,
        **kwargs,
    )


def input_py_literal(
    parent: Optional[QWidget],
    title: str = "Input Python Literal",
    icon: IconType = None,
    size: Tuple[int, int] = (600, 400),
    ok_button_text: str = "Ok",
    cancel_button_text: Optional[str] = "Cancel",
    initial_text: str = "",
    auto_indent: bool = True,
    indent_size: int = 4,
    auto_parentheses: bool = True,
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth,
    line_wrap_width: int = 88,
    font_family: Union[str, Sequence[str], None] = None,
    font_size: Optional[int] = None,
    **kwargs,
) -> PyLiteralType:
    """
    弹出一个 Python 字面量输入对话框，并返回用户输入的 Python 字面量对象。

    Args:
        parent:  父窗口
        title:  对话框标题
        icon:  对话框图标
        size:  对话框大小
        ok_button_text: 确定按钮文本
        cancel_button_text:  取消按钮文本
        initial_text:  初始文本
        auto_indent:  自动缩进
        indent_size:  缩进大小
        auto_parentheses:  自动括号匹配
        line_wrap_mode:  换行模式
        line_wrap_width:  换行宽度
        font_family:  字体
        font_size:  字体大小
        **kwargs:  其他参数

    Returns:
        用户输入的 Python 字面量对象，如果用户取消输入则返回 None。

    Raises:
        Exception: 输入的文本不是合法的python字面量代码时抛出异常。
    """
    return PyLiteralInputDialog.show_and_get_result(
        parent,
        title=title,
        icon=icon,
        size=size,
        ok_button_text=ok_button_text,
        cancel_button_text=cancel_button_text,
        initial_text=initial_text,
        auto_indent=auto_indent,
        indent_size=indent_size,
        auto_parentheses=auto_parentheses,
        line_wrap_mode=line_wrap_mode,
        line_wrap_width=line_wrap_width,
        font_family=font_family,
        font_size=font_size,
        **kwargs,
    )


def get_custom_input(
    parent: QWidget, input_dialog_class: Type[UniversalInputDialog], **input_dialog_args
) -> Any:
    """
    弹出一个自定义输入对话框，并返回用户输入的对象。

    Args:
        parent:  父窗口
        input_dialog_class:  自定义输入对话框类
        **input_dialog_args:  自定义输入对话框构造函数参数

    Returns:
        用户输入的对象，如果用户取消输入则返回 None。
    """
    return input_dialog_class.show_and_get_result(parent, **input_dialog_args)
