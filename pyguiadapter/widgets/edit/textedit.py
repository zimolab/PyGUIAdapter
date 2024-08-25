from __future__ import annotations

import dataclasses
from typing import Type, Any, TypeVar

from qtpy.QtGui import QTextOption
from qtpy.QtWidgets import QWidget, QTextEdit

from ..common import CommonParameterWidget, CommonParameterWidgetConfig

LineWrapMode = QTextEdit.LineWrapMode
AutoFormatting = QTextEdit.AutoFormatting
WrapMode = QTextOption.WrapMode


@dataclasses.dataclass(frozen=True)
class TextEditConfig(CommonParameterWidgetConfig):
    placeholder: str = ""
    accept_rich_text: bool = False
    auto_formatting: AutoFormatting | None = None
    line_wrap: LineWrapMode = LineWrapMode.WidgetWidth
    line_wrap_column_or_width: int = 0
    word_wrap: WrapMode | None = None

    @classmethod
    def target_widget_class(cls) -> Type["TextEdit"]:
        return TextEdit


class TextEdit(CommonParameterWidget):

    Self = TypeVar("Self", bound="TextEdit")
    ConfigClass = TextEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: TextEditConfig,
    ):
        self._config: TextEditConfig = config
        self._value_widget: QTextEdit | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QTextEdit:
        if self._value_widget is None:
            self._value_widget = QTextEdit(self)
        self._setup_value_widget()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        self.value_widget.setPlainText(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.toPlainText()

    def _setup_value_widget(self):
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
