from typing import Any, Union, Optional, Sequence

from qtpy.QtWidgets import QWidget, QComboBox, QTableWidgetItem

from ..object_tableview import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType

EDITABLE = False


class ChoiceCombo(QComboBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        choices: Sequence[str],
        *,
        editable: bool,
    ):
        super().__init__(parent)

        for choice in choices:
            # noinspection PyArgumentList
            self.addItem(choice)

        self.setEditable(editable)

        self.set_value(default_value)

    def get_value(self) -> str:
        return self.currentText()

    def set_value(self, value: Union[int, str]):
        if isinstance(value, int):
            self.setCurrentIndex(value)
        else:
            self.setCurrentText(value)


class ChoiceValue(ValueType):

    def __init__(
        self,
        default_value: Union[int, str],
        choices: Sequence[str],
        *,
        display_name: Optional[str] = None,
        editable: bool = EDITABLE,
        readonly: bool = False,
        hidden: bool = False,
    ):
        if not choices:
            raise ValueError("choices cannot be empty")

        self.choices = choices
        self.editable = editable

        if isinstance(default_value, int):
            if default_value < 0 or default_value >= len(choices):
                raise IndexError(f"index out of range: {default_value}")
            default_value = choices[default_value]

        super().__init__(
            default_value, display_name=display_name, readonly=readonly, hidden=hidden
        )

    def validate(self, value: Any) -> bool:
        if isinstance(value, int):
            return 0 <= value < len(self.choices)
        elif isinstance(value, str):
            return value in self.choices
        else:
            return False

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> ChoiceCombo:
        return ChoiceCombo(
            parent, self.default_value, self.choices, editable=self.editable
        )

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> ChoiceCombo:
        return self.create_item_delegate_widget(parent)

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        if isinstance(value, int) and 0 <= value < len(self.choices):
            item.setText(self.choices[value])
