from typing import Any, Union, List, Tuple, Dict, Optional

from qtpy.QtWidgets import QWidget, QComboBox

from ..schema import ValueWidgetMixin, ValueType

DEFAULT_VALUE = 0


class ChoiceEditor(QComboBox, ValueWidgetMixin):
    def __init__(self, parent: QWidget, default_value: str, choices: Dict[str, Any]):
        super().__init__(parent)

        self._choices = choices.copy()
        for text, value in self._choices.items():
            self.addItem(text, value)

        self.set_value(default_value)

    def get_value(self) -> Any:
        return self.currentData()

    def set_value(self, value: Union[int, str]):
        if value is None:
            value = DEFAULT_VALUE
        if isinstance(value, str):
            for index in range(self.count()):
                text = self.itemText(index)
                if text == value:
                    self.setCurrentIndex(index)
                    return
        elif isinstance(value, int):
            self.setCurrentIndex(value)
        else:
            raise TypeError("value must be an int or str")


class ChoiceValue(ValueType):

    def __init__(
        self,
        default_value: Union[int, str],
        choices: Union[List[Any], Tuple[Any, ...], Dict[str, Any]],
        *,
        display_name: Optional[str] = None
    ):
        if not isinstance(choices, (list, tuple, dict)):
            raise TypeError("choices must be a list, tuple or dict")

        if isinstance(choices, (list, tuple)):
            choices = {str(v): v for v in choices}

        if isinstance(default_value, int):
            default_value = list(choices.keys())[default_value]

        super().__init__(default_value, display_name=display_name)
        self.choices = choices

    def validate(self, value: Any) -> bool:
        return isinstance(value, (int, str))

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> QWidget:
        return ChoiceEditor(parent, self.default_value, self.choices)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return self.create_item_delegate_widget(parent, *args, **kwargs)
