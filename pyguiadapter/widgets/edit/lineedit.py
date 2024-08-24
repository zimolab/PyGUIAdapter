from __future__ import annotations

import dataclasses
from typing import Any, TypeVar, Type

from qtpy.QtCore import QRegularExpression
from qtpy.QtGui import QValidator, QRegularExpressionValidator
from qtpy.QtWidgets import QWidget, QLineEdit

from ..common import CommonParameterWidget, CommonParameterWidgetConfig

EchoMode = QLineEdit.EchoMode


@dataclasses.dataclass(frozen=True)
class LineEditConfig(CommonParameterWidgetConfig):
    placeholder: str = ""
    clear_button_enabled: bool = False
    echo_mode: EchoMode | None = None
    input_mask: str | None = None
    max_length: int | None = None
    validator: QValidator | str | None = "\\d\\d \\w+"

    @classmethod
    def target_widget_class(cls) -> Type["LineEdit"]:
        return LineEdit


class LineEdit(CommonParameterWidget):
    Self = TypeVar("Self", bound="LineEdit")
    ConfigClass = LineEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: LineEditConfig
    ):

        self._config: LineEditConfig = config
        self._value_widget: QLineEdit | None = None

        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            self._value_widget = QLineEdit(self)
            self._value_widget.setObjectName(self.parameter_name)
        self._setup_value_widget()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        self.value_widget.setText(str(value))

    def get_value_from_widget(self) -> str:
        return self.value_widget.text()

    def _setup_value_widget(self):
        self._value_widget.setPlaceholderText(self._config.placeholder or "")
        self._value_widget.setClearButtonEnabled(self._config.clear_button_enabled)
        if self._config.echo_mode is not None:
            self._value_widget.setEchoMode(self._config.echo_mode)

        if self._config.input_mask:
            self._value_widget.setInputMask(self._config.input_mask)

        max_length = self._config.max_length
        if max_length is not None:
            max_length = max(max_length, 1)
            self._value_widget.setMaxLength(max_length)

        validator = self._config.validator
        if isinstance(validator, str):
            regex = QRegularExpression(validator)
            validator = QRegularExpressionValidator(self._value_widget)
            validator.setRegularExpression(regex)
        if validator is not None:
            self._value_widget.setValidator(validator)
