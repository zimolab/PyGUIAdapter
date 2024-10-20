"""
@Time    : 2024.10.20
@File    : uinput.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 提供输入框相关的功能
"""

from concurrent.futures import Future
from typing import (
    List,
    Tuple,
    Literal,
    Callable,
    Any,
    Optional,
    Union,
    Sequence,
    Type,
)

from qtpy.QtCore import QUrl
from qtpy.QtGui import QColor

from .ucontext import _context
from ..utils import EchoMode, inputdialog, filedialog, IconType, PyLiteralType
from ..utils.inputdialog import LineWrapMode, UniversalInputDialog
from ..windows.fnexec import FnExecuteWindow


def _get_input(get_input_impl: Callable[[FnExecuteWindow], Any]) -> Any:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.sig_get_input.emit(result_future, get_input_impl)
    return result_future.result()


def get_string(
    title: str = "Input Text",
    label: str = "",
    echo: Optional[EchoMode] = None,
    text: str = "",
) -> Optional[str]:
    """
    弹出单行文本输入框，返回用户输入的字符串。

    Args:
        title: 对话框标题
        label: 提示标签
        echo:  回显模式
        text:  初始文本

    Returns:
        用户输入的字符串，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return inputdialog.input_string(wind, title, label, echo, text)

    return _get_input(_impl)


def get_text(
    title: str = "Input Text", label: str = "", text: str = ""
) -> Optional[str]:
    """
    弹出多行文本输入框，返回用户输入的字符串。

    Args:
        title: 对话框标题
        label: 提示标签
        text: 初始文本

    Returns:
        用户输入的字符串，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return inputdialog.input_text(wind, title, label, text)

    return _get_input(_impl)


def get_int(
    title: str = "Input Integer",
    label: str = "",
    value: int = 0,
    min_value: int = -2147483647,
    max_value: int = 2147483647,
    step: int = 1,
) -> Optional[int]:
    """
    弹出整数输入框，返回用户输入的整数。

    Args:
        title: 对话框标题
        label: 提示标签
        value: 初始值
        min_value: 最小值
        max_value: 最大值
        step: 步长

    Returns:
        用户输入的整数，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[int]:
        return inputdialog.input_integer(
            wind, title, label, value, min_value, max_value, step
        )

    return _get_input(_impl)


def get_float(
    title: str = "Input Float",
    label: str = "",
    value: float = 0.0,
    min_value: float = -2147483647.0,
    max_value: float = 2147483647.0,
    decimals: int = 3,
    step: float = 1.0,
) -> Optional[float]:
    """
    弹出浮点数输入框，返回用户输入的浮点数。

    Args:
        title: 对话框标题
        label: 提示标签
        value: 初始值
        min_value: 最小值
        max_value: 最大值
        decimals: 小数位数
        step: 步长

    Returns:
        用户输入的浮点数，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[float]:
        return inputdialog.input_float(
            wind, title, label, value, min_value, max_value, decimals, step
        )

    return _get_input(_impl)


def get_selected_item(
    items: List[str],
    title: str = "Select Item",
    label: str = "",
    current: int = 0,
    editable: bool = False,
) -> Optional[str]:
    """
    弹出选项列表，返回用户选择的项目。

    Args:
        items: 项目列表
        title: 对话框标题
        label: 提示标签
        current: 当前选择项索引
        editable: 是否可编辑

    Returns:
        用户选择的项目，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]):
        return inputdialog.select_item(wind, items, title, label, current, editable)

    return _get_input(_impl)


def get_color(
    initial: Union[QColor, str, tuple] = "white",
    title: str = "",
    alpha_channel: bool = True,
    return_type: Literal["tuple", "str", "QColor"] = "str",
) -> Union[Tuple[int, int, int], Tuple[int, int, int], str, QColor, None]:
    """
    弹出颜色选择框，返回用户选择的颜色。

    Args:
        initial: 初始颜色
        title: 对话框标题
        alpha_channel: 是否显示Alpha通道
        return_type: 返回类型，可以是tuple、str、QColor

    Returns:
        用户选择的颜色，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[QColor]:
        return inputdialog.input_color(wind, initial, title, alpha_channel, return_type)

    return _get_input(_impl)


def get_json_object(
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
    弹出Json输入框，返回用户输入的Json对象。

    Args:
        title: 对话框标题
        icon: 窗口图标
        size: 窗口大小
        ok_button_text: 确定按钮文本
        cancel_button_text: 取消按钮文本
        initial_text: 初始文本
        auto_indent: 是否自动缩进
        indent_size: 缩进大小
        auto_parentheses: 是否自动匹配括号
        line_wrap_mode: 换行模式
        line_wrap_width: 换行宽度
        font_family: 字体
        font_size: 字体大小
        **kwargs: 其他参数

    Returns:
        用户输入的Json对象，如果用户取消输入则返回None。

    Raises:
        Exception: 如果输入了非法的Json文本，则会抛出异常。

    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Any:
        return inputdialog.input_json_object(
            wind,
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

    return _get_input(_impl)


def get_py_literal(
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
    弹出Python字面量输入框，返回用户输入的Python字面量。

    Args:
        title: 对话框标题
        icon: 窗口图标
        size: 窗口大小
        ok_button_text: 确定按钮文本
        cancel_button_text: 取消按钮文本
        initial_text: 初始文本
        auto_indent: 是否自动缩进
        indent_size: 缩进大小
        auto_parentheses: 是否自动匹配括号
        line_wrap_mode: 换行模式
        line_wrap_width: 换行宽度
        font_family: 字体
        font_size: 字体大小
        **kwargs: 其他参数

    Returns:
        用户输入的Python字面量，如果用户取消输入则返回None。

    Raises:
        Exception: 如果输入了非法的Python字面量（即ast.literal_eval()无法解析的内容），则会抛出异常。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Any:
        return inputdialog.input_py_literal(
            wind,
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

    return _get_input(_impl)


def get_custom_input(
    input_dialog_class: Type[UniversalInputDialog],
    **input_dialog_args,
) -> Any:
    """
    弹出自定义输入框，返回用户输入的内容。

    Args:
        input_dialog_class: 自定义输入框类
        **input_dialog_args: 自定义输入框参数

    Returns:
        用户输入的内容，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Any:
        return inputdialog.get_custom_input(
            wind, input_dialog_class, **input_dialog_args
        )

    return _get_input(_impl)


def get_existing_directory(
    title: str = "",
    start_dir: str = "",
) -> Optional[str]:
    """
    弹出选择文件夹对话框，返回用户选择的目录。

    Args:
        title: 对话框标题
        start_dir: 起始目录

    Returns:
        用户选择的目录，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return filedialog.get_existing_directory(wind, title, start_dir)

    return _get_input(_impl)


def get_existing_directory_url(
    title: str = "",
    start_dir: Optional[QUrl] = None,
    supported_schemes: Optional[List[str]] = None,
) -> Optional[QUrl]:
    """
    弹出选择文件夹对话框，返回用户选择的目录的URL。

    Args:
        title: 对话框标题
        start_dir: 起始目录
        supported_schemes: 支持的协议

    Returns:
        用户选择的目录的URL，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> QUrl:
        return filedialog.get_existing_directory_url(
            wind, title, start_dir, supported_schemes
        )

    return _get_input(_impl)


def get_open_file(
    title: str = "",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    """
    弹出打开文件对话框，返回用户选择的文件。

    Args:
        title: 对话框标题
        start_dir: 起始目录
        filters: 文件过滤器

    Returns:
        用户选择的文件路径，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return filedialog.get_open_file(wind, title, start_dir, filters)

    return _get_input(_impl)


def get_open_files(
    title: str = "",
    start_dir: str = "",
    filters: str = "",
) -> Optional[List[str]]:
    """
    弹出打开文件对话框，返回用户选择的多个文件。
    Args:
        title: 对话框标题
        start_dir: 起始目录
        filters: 文件过滤器

    Returns:
        用户选择的文件路径列表，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[List[str]]:
        return filedialog.get_open_files(wind, title, start_dir, filters)

    return _get_input(_impl)


def get_save_file(
    title: str = "",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    """
    弹出保存文件对话框，返回用户输入或选择的文件路径。

    Args:
        title: 对话框标题
        start_dir: 起始目录
        filters: 文件过滤器

    Returns:
        用户输入或选择的文件路径，如果用户取消输入则返回None。
    """

    def _impl(wind: Optional[FnExecuteWindow]) -> Optional[str]:
        return filedialog.get_save_file(wind, title, start_dir, filters)

    return _get_input(_impl)
