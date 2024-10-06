import dataclasses

from qtpy.QtCore import QRegularExpression, Qt
from qtpy.QtGui import QValidator, QRegularExpressionValidator
from qtpy.QtWidgets import QWidget, QLineEdit
from typing import Type, Optional, Union

from ..common import CommonParameterWidget, CommonParameterWidgetConfig

EchoMode = QLineEdit.EchoMode
Alignment = Qt.Alignment


@dataclasses.dataclass(frozen=True)
class LineEditConfig(CommonParameterWidgetConfig):
    default_value: Optional[str] = ""
    placeholder: str = ""
    clear_button_enabled: bool = False
    echo_mode: Optional[EchoMode] = None
    alignment: Optional[Alignment] = None
    input_mask: Optional[str] = None
    max_length: Optional[int] = None
    validator: Union[QValidator, str, None] = None
    drag_enabled: bool = True
    frame: bool = True
    readonly: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["LineEdit"]:
        return LineEdit


class LineEdit(CommonParameterWidget):
    ConfigClass = LineEditConfig
    EchoMode = EchoMode
    Alignment = Alignment

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: LineEditConfig
    ):

        self._value_widget: Optional[QLineEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            config: LineEditConfig = self.config
            self._value_widget = QLineEdit("", self)
            self._value_widget.setPlaceholderText(config.placeholder or "")
            self._value_widget.setClearButtonEnabled(config.clear_button_enabled)
            if config.echo_mode is not None:
                self._value_widget.setEchoMode(config.echo_mode)

            if config.input_mask:
                self._value_widget.setInputMask(config.input_mask)

            max_length = config.max_length
            if isinstance(max_length, int):
                max_length = max(max_length, 1)
                self._value_widget.setMaxLength(max_length)

            validator = config.validator
            if isinstance(validator, str):
                regex = QRegularExpression(validator)
                validator = QRegularExpressionValidator(self._value_widget)
                validator.setRegularExpression(regex)
            assert isinstance(validator, (QValidator, type(None)))
            if validator:
                self._value_widget.setValidator(validator)

            if config.alignment is not None:
                self._value_widget.setAlignment(config.alignment)

            self._value_widget.setFrame(config.frame is True)
            self._value_widget.setDragEnabled(config.drag_enabled is True)
            self._value_widget.setReadOnly(config.readonly is True)

        return self._value_widget

    def set_value_to_widget(self, value: str):
        self.value_widget.setText(str(value))

    def get_value_from_widget(self) -> str:
        if not self._value_widget.hasAcceptableInput():
            raise ValueError("unacceptable input: validation failed")
        return self.value_widget.text()
