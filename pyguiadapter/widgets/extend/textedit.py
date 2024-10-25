import dataclasses
from typing import Type, Any, Optional

from qtpy.QtGui import QTextOption
from qtpy.QtWidgets import QWidget, QTextEdit

from ..common import CommonParameterWidget, CommonParameterWidgetConfig
from ...utils import type_check

LineWrapMode = QTextEdit.LineWrapMode
AutoFormatting = QTextEdit.AutoFormattingFlag
WrapMode = QTextOption.WrapMode


@dataclasses.dataclass(frozen=True)
class TextEditConfig(CommonParameterWidgetConfig):
    """TextEdit的配置类"""

    default_value: Optional[str] = ""
    """控件的默认值"""

    placeholder: str = ""
    """控件的占位符"""

    accept_rich_text: bool = False
    """是否接受富文本"""

    auto_formatting: Optional[AutoFormatting] = None
    """是否自动格式化"""

    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth
    """自动换行模式"""

    line_wrap_width: int = 88
    """自动换行宽度"""

    word_wrap_mode: Optional[WrapMode] = None
    """单词换行模式"""

    height: Optional[int] = 200
    """控件高度"""

    width: Optional[int] = None
    """控件宽度"""

    @classmethod
    def target_widget_class(cls) -> Type["TextEdit"]:
        return TextEdit


class TextEdit(CommonParameterWidget):
    ConfigClass = TextEditConfig

    NoLineWrap = LineWrapMode.NoWrap
    """换行模式：不自动换行"""

    WidgetWidth = LineWrapMode.WidgetWidth
    """换行模式：根据控件宽度自动换行"""

    FixedColumnWidth = LineWrapMode.FixedColumnWidth
    """换行模式：固定列宽换行"""

    FixedPixelWidth = LineWrapMode.FixedPixelWidth
    """换行模式：固定像素宽换行"""

    NoWordWrap = WrapMode.NoWrap
    """单词换行模式：不换行"""

    WordWrap = WrapMode.WordWrap
    """单词换行模式：根据单词自动换行"""

    ManualWordWrap = WrapMode.ManualWrap
    """单词换行模式：手动换行"""

    WordWrapAnywhere = WrapMode.WrapAnywhere
    """单词换行模式：任意位置换行"""

    WordWrapAtWordBoundaryOrAnywhere = WrapMode.WrapAtWordBoundaryOrAnywhere
    """单词换行模式：单词边界或任意位置换行"""

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: TextEditConfig,
    ):
        self._value_widget: Optional[QTextEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QTextEdit:
        self._config: TextEditConfig
        if self._value_widget is None:
            self._value_widget = QTextEdit(self)
            self._value_widget.setPlaceholderText(self._config.placeholder)
            self._value_widget.setAcceptRichText(self._config.accept_rich_text)
            auto_formatting = self._config.auto_formatting
            if auto_formatting is not None:
                self._value_widget.setAutoFormatting(auto_formatting)

            line_wrap = self._config.line_wrap_mode
            if line_wrap is not None:
                self._value_widget.setLineWrapMode(line_wrap)

            if (
                line_wrap == LineWrapMode.FixedColumnWidth
                or line_wrap == LineWrapMode.WidgetWidth
            ) and self._config.line_wrap_width > 0:
                self._value_widget.setLineWrapColumnOrWidth(
                    self._config.line_wrap_width
                )

            word_wrap = self._config.word_wrap_mode
            if word_wrap is not None:
                self._value_widget.setWordWrapMode(word_wrap)

            if self._config.height is not None and self._config.height > 0:
                self._value_widget.setFixedHeight(self._config.height)

            if self._config.width is not None and self._config.width > 0:
                self._value_widget.setFixedWidth(self._config.width)

        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (str,), allow_none=True)

    def set_value_to_widget(self, value: Any):
        self.value_widget.setPlainText(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.toPlainText()
