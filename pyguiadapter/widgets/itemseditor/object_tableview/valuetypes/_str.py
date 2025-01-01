from typing import Union, Optional

from qtpy.QtCore import QRegularExpression
from qtpy.QtGui import QValidator, QRegularExpressionValidator
from qtpy.QtWidgets import QLineEdit, QWidget

from ..schema import ValueWidgetMixin, ValueType

DEFAULT_VALUE = ""
ECHO_MODE = None
CLEAR_BUTTON_ENABLED = False
MAX_LENGTH = None
PLACEHOLDER = None
INPUT_MASK = None
VALIDATOR = None


class StringEditor(QLineEdit, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str = DEFAULT_VALUE,
        *,
        echo_mode: Union[QLineEdit.EchoMode, int, None] = ECHO_MODE,
        clear_button_enabled: bool = CLEAR_BUTTON_ENABLED,
        max_length: Optional[int] = MAX_LENGTH,
        placeholder: Optional[str] = PLACEHOLDER,
        input_mask: Optional[str] = INPUT_MASK,
        validator: Union[QValidator, str, None] = None
    ):
        super().__init__(parent)

        if echo_mode is not None:
            self.setEchoMode(echo_mode)
        self.setClearButtonEnabled(clear_button_enabled)
        if max_length is not None:
            self.setMaxLength(max_length)
        if placeholder is not None:
            self.setPlaceholderText(placeholder)
        if input_mask is not None:
            self.setInputMask(input_mask)

        if isinstance(validator, str):
            regex = QRegularExpression(validator)
            validator = QRegularExpressionValidator(self)
            validator.setRegularExpression(regex)
        assert isinstance(validator, (QValidator, type(None)))
        if validator:
            self.setValidator(validator)

        self.set_value(default_value)

    def set_value(self, value: str):
        self.setText(str(value))

    def get_value(self) -> str:
        return self.text()


class StringValue(ValueType):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        echo_mode: Union[QLineEdit.EchoMode, int, None] = ECHO_MODE,
        clear_button: bool = CLEAR_BUTTON_ENABLED,
        max_length: Optional[int] = MAX_LENGTH,
        placeholder: Optional[str] = PLACEHOLDER,
        input_mask: Optional[str] = INPUT_MASK,
        validator: Union[QValidator, str, None] = None
    ):
        super().__init__(str(default_value), display_name=display_name)

        self.echo_mode = echo_mode
        self.clear_button = clear_button
        self.max_length = max_length
        self.placeholder = placeholder
        self.input_mask = input_mask
        self.validator = validator

    def validate(self, value: str) -> bool:
        return isinstance(value, str)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> StringEditor:
        return StringEditor(
            parent,
            self.default_value,
            echo_mode=self.echo_mode,
            clear_button_enabled=self.clear_button,
            max_length=self.max_length,
            placeholder=self.placeholder,
            input_mask=self.input_mask,
            validator=self.validator,
        )

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> StringEditor:
        return StringEditor(
            parent,
            self.default_value,
            echo_mode=self.echo_mode,
            clear_button_enabled=self.clear_button,
            max_length=self.max_length,
            placeholder=self.placeholder,
            input_mask=self.input_mask,
            validator=self.validator,
        )
