import ast
import json
from abc import abstractmethod
from typing import Optional, Union, List, Literal, Tuple, Any, Sequence, cast

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters import QJSONHighlighter, QPythonHighlighter
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import (
    QLineEdit,
    QInputDialog,
    QColorDialog,
    QWidget,
    QDialog,
    QTextEdit,
)

from ._core import PyLiteralType
from ._ui import to_qcolor, convert_color, IconType
from .dialog import UniversalInputDialog
from .messagebox import show_critical_message

EchoMode = QLineEdit.EchoMode


def input_integer(
    parent: Optional[QWidget],
    title: str = "Input Integer",
    label: str = "",
    value: int = 0,
    min_value: int = -2147483647,
    max_value: int = 2147483647,
    step: int = 1,
) -> Optional[int]:
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
) -> Union[Tuple[int, int, int], Tuple[int, int, int], str, QColor, None]:
    initial = to_qcolor(initial)
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


class CodeEditDialog(UniversalInputDialog):
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
        font_family: Union[str, Sequence[str], None] = "Consolas",
        font_size: Optional[int] = None,
        **kwargs,
    ):
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
        assert self._main_widget is not None
        return self._main_widget.toPlainText()


class ObjectInputDialog(CodeEditDialog):
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
        font_family: Union[str, Sequence[str], None] = "Consolas",
        font_size: Optional[int] = None,
        **kwargs,
    ):
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
        assert self._main_widget is not None
        return self._current_value


class JsonInputDialog(ObjectInputDialog):
    def create_main_widget(self) -> QCodeEditor:
        editor = super().create_main_widget()
        highlighter = QJSONHighlighter(editor)
        editor.setHighlighter(highlighter)
        return editor

    def get_object(self) -> Any:
        editor = cast(QCodeEditor, self._main_widget)
        text = editor.toPlainText()
        if text.strip() == "":
            self._current_value = None
            self.accept()
            return
        return json.loads(text)


class PyLiteralInputDialog(ObjectInputDialog):
    def create_main_widget(self) -> QCodeEditor:
        editor = super().create_main_widget()
        highlighter = QPythonHighlighter(editor)
        editor.setHighlighter(highlighter)
        return editor

    def get_object(self) -> Any:
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
    font_family: Union[str, Sequence[str], None] = "Consolas",
    font_size: Optional[int] = None,
    **kwargs,
) -> Any:
    json_dialog = JsonInputDialog(
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
    ret = json_dialog.exec_()
    if ret == QDialog.Accepted:
        return json_dialog.get_result()
    return None


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
    font_family: Union[str, Sequence[str], None] = "Consolas",
    font_size: Optional[int] = None,
    **kwargs,
) -> Any:
    py_dialog = PyLiteralInputDialog(
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
    ret = py_dialog.exec_()
    if ret == QDialog.Accepted:
        return py_dialog.get_result()
    return None
