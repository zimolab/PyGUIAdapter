from typing import Any, Union, Optional, Sequence

from qtpy.QtWidgets import QWidget, QComboBox

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
    ):
        if not choices:
            raise ValueError("choices cannot be empty")

        self.choices = choices
        self.editable = editable

        if isinstance(default_value, int):
            if default_value < 0 or default_value >= len(choices):
                raise IndexError(f"index out of range: {default_value}")
            default_value = choices[default_value]

        super().__init__(default_value, display_name=display_name)

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
