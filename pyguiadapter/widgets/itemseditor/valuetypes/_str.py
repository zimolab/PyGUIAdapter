from typing import Union, Optional, Any

from qtpy.QtCore import QRegularExpression
from qtpy.QtGui import QValidator, QRegularExpressionValidator
from qtpy.QtWidgets import QLineEdit, QWidget, QTableWidgetItem

from ..object_tableview import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType

EchoMode = QLineEdit.EchoMode
PasswordEchoMode = EchoMode.Password
NormalEchoMode = EchoMode.Normal
PasswordEchoOnEditMode = EchoMode.PasswordEchoOnEdit

DEFAULT_VALUE = ""
ECHO_MODE = None
CLEAR_BUTTON = False
MAX_LENGTH = None
PLACEHOLDER = None
INPUT_MASK = None
VALIDATOR = None
PASSWORD_SYMBOL = "•"
MAX_PASSWORD_SYMBOLS = 10


def _to_str(value: Any) -> str:
    if value is None:
        return DEFAULT_VALUE
    return str(value)


class StrEdit(QLineEdit, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        echo_mode: Union[QLineEdit.EchoMode, int, None],
        clear_button: bool,
        max_length: Optional[int],
        placeholder: Optional[str],
        input_mask: Optional[str],
        validator: Union[QValidator, str, None],
    ):
        super().__init__(parent)

        if echo_mode is not None:
            self.setEchoMode(echo_mode)

        self.setClearButtonEnabled(clear_button)

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
        self.setText(_to_str(value))

    def get_value(self) -> str:
        return self.text()


class StringValue(ValueType):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        echo_mode: Union[QLineEdit.EchoMode, int, None] = ECHO_MODE,
        clear_button: bool = CLEAR_BUTTON,
        max_length: Optional[int] = MAX_LENGTH,
        placeholder: Optional[str] = PLACEHOLDER,
        input_mask: Optional[str] = INPUT_MASK,
        validator: Union[QValidator, str, None] = VALIDATOR,
        password_symbol: str = "•",
        max_password_symbols: int = MAX_PASSWORD_SYMBOLS,
    ):
        self.echo_mode = echo_mode
        self.clear_button = clear_button
        self.max_length = max_length
        self.placeholder = placeholder
        self.input_mask = input_mask
        self.validator = validator
        self.password_symbol = password_symbol
        self.max_password_symbols = max_password_symbols

        super().__init__(_to_str(default_value), display_name=display_name)

    def validate(self, value: str) -> bool:
        return value is None or isinstance(value, str)

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> StrEdit:
        return StrEdit(
            parent,
            self.default_value,
            echo_mode=self.echo_mode,
            clear_button=self.clear_button,
            max_length=self.max_length,
            placeholder=self.placeholder,
            input_mask=self.input_mask,
            validator=self.validator,
        )

    def create_item_editor_widget(self, parent: QWidget, *args, **kwargs) -> StrEdit:
        return self.create_item_delegate_widget(parent)

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: str
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        if self.echo_mode in (PasswordEchoMode, QLineEdit.PasswordEchoOnEdit):
            symbol_len = min(len(value), self.max_password_symbols)
            password_symbol = self.password_symbol * symbol_len
            item.setText(password_symbol)
