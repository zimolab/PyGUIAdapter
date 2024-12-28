from typing import Optional, Any

from qtpy.QtCore import QModelIndex
from qtpy.QtWidgets import QWidget, QLineEdit, QStyleOptionViewItem

from .base import ValueWidgetMixin, ValueTypeBase

_DEFAULT_VALUE = ""


class StringValueEditor(QLineEdit, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        placeholder: Optional[str] = None,
    ):
        super().__init__(parent)
        if placeholder is not None:
            self.setPlaceholderText(placeholder)

        self.setText(default_value)

    def cast_value(self, original_value: Any) -> str:
        return str(original_value)

    def get_value(self) -> str:
        return self.text()

    def set_value(self, value: str):
        if value is None:
            value = _DEFAULT_VALUE
        if not isinstance(value, str):
            value = str(value)
        self.setText(value)


class StringValue(ValueTypeBase):

    def __init__(
        self, default_value: str = _DEFAULT_VALUE, *, placeholder: Optional[str] = None
    ):
        super().__init__(default_value)
        self.placeholder = placeholder

    def on_create_editor(
        self,
        parent: QWidget,
        option: Optional[QStyleOptionViewItem],
        index: Optional[QModelIndex],
        **kwargs,
    ) -> QWidget:
        editor = StringValueEditor(
            parent, default_value=self.default_value, placeholder=self.placeholder
        )
        return editor

    def on_create_edit(self, parent: QWidget, **kwargs) -> QWidget:
        return self.on_create_editor(parent, None, None)
