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
    default_value: Optional[str] = ""
    placeholder: str = ""
    accept_rich_text: bool = False
    auto_formatting: Optional[AutoFormatting] = None
    line_wrap: LineWrapMode = LineWrapMode.WidgetWidth
    line_wrap_column_or_width: int = 88
    word_wrap: Optional[WrapMode] = None
    min_height: Optional[int] = 200

    @classmethod
    def target_widget_class(cls) -> Type["TextEdit"]:
        return TextEdit


class TextEdit(CommonParameterWidget):
    ConfigClass = TextEditConfig

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

            line_wrap = self._config.line_wrap
            if line_wrap is not None:
                self._value_widget.setLineWrapMode(line_wrap)

            if (
                line_wrap == LineWrapMode.FixedColumnWidth
                or line_wrap == LineWrapMode.WidgetWidth
            ) and self._config.line_wrap_column_or_width > 0:
                self._value_widget.setLineWrapColumnOrWidth(
                    self._config.line_wrap_column_or_width
                )

            word_wrap = self._config.word_wrap
            if word_wrap is not None:
                self._value_widget.setWordWrapMode(word_wrap)

            if self._config.min_height is not None and self._config.min_height > 0:
                self._value_widget.setMinimumHeight(self._config.min_height)

        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (str,), allow_none=True)

    def set_value_to_widget(self, value: Any):
        self.value_widget.setPlainText(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.toPlainText()
