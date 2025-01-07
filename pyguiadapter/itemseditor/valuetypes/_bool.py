from typing import Any, Union, Optional

from qtpy.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QComboBox,
    QRadioButton,
    QButtonGroup,
    QTableWidgetItem,
)

from ..object_tableview import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType

TRUE_TEXT = "True"
FALSE_TEXT = "False"
DEFAULT_VALUE = False


def _to_bool(value: Any, true_text: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value == true_text
    return bool(value)


class BoolCombo(QComboBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: Union[bool, str, None],
        *,
        true_text: str,
        false_text: str,
    ):
        super().__init__(parent)

        self._default_value = None

        self._true_text = true_text
        self._false_text = false_text
        self.addItem(self._true_text, True)
        self.addItem(self._false_text, False)

        self.set_value(default_value)

    def get_value(self) -> bool:
        return _to_bool(self.currentData(), self._true_text)

    def set_value(self, value: Union[bool, str, None]):
        self._default_value = _to_bool(value, self._true_text)

        if self._default_value:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(1)


class BoolBox(QWidget, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: Union[bool, str, None],
        *,
        true_text: str,
        false_text: str,
    ):
        super().__init__(parent)

        self._default_value = None
        self._true_text = true_text
        self._false_text = false_text

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self._true_button = QRadioButton(self)
        self._true_button.setText(self._true_text)
        self._false_button = QRadioButton(self)
        self._false_button.setText(self._false_text)

        self._btn_group = QButtonGroup(self)
        self._btn_group.setExclusive(True)
        self._btn_group.addButton(self._true_button, 0)
        self._btn_group.addButton(self._false_button, 1)

        self._layout.addWidget(self._true_button)
        self._layout.addWidget(self._false_button)

        self.set_value(default_value)

    def get_value(self) -> bool:
        return self._true_button.isChecked()

    def set_value(self, value: Union[bool, str, None]):
        self._default_value = _to_bool(value, self._true_text)
        if self._default_value:
            self._true_button.setChecked(True)
        else:
            self._false_button.setChecked(True)


class BoolValue(ValueType):

    def __init__(
        self,
        default_value: bool = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        true_text: str = TRUE_TEXT,
        false_text: str = FALSE_TEXT,
    ):
        self.true_text = true_text
        self.false_text = false_text

        super().__init__(_to_bool(default_value, true_text), display_name=display_name)

    def validate(self, value: Any) -> bool:
        return isinstance(value, bool) or value in (self.true_text, self.false_text)

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> BoolCombo:
        return BoolCombo(
            parent,
            self.default_value,
            true_text=self.true_text,
            false_text=self.false_text,
        )

    def create_item_editor_widget(self, parent: QWidget, *args, **kwargs) -> BoolBox:
        return BoolBox(
            parent,
            self.default_value,
            true_text=self.true_text,
            false_text=self.false_text,
        )

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        if _to_bool(value, self.true_text):
            item.setText(self.true_text)
        else:
            item.setText(self.false_text)
