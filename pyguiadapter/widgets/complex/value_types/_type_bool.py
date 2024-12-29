from qtpy.QtWidgets import QWidget, QRadioButton, QButtonGroup, QHBoxLayout
from typing import Any, Union

from ..schema import ValueWidgetMixin, ValueTypeBase, CellWidgetMixin

TRUE_TEXT = "True"
FALSE_TEXT = "False"


class BoolValueEditor(QWidget, CellWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: bool = False,
        true_text: str = TRUE_TEXT,
        false_text: str = FALSE_TEXT,
    ):
        super().__init__(parent)

        self._default_value = default_value
        self._true_text = true_text
        self._false_text = false_text

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self._true_button = QRadioButton(self._true_text)
        self._false_button = QRadioButton(self._false_text)
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)

        self._layout.addStretch(1)
        self._layout.addWidget(self._true_button)
        self._layout.addWidget(self._false_button)
        self._layout.addStretch(1)

        self._button_group.addButton(self._true_button)
        self._button_group.addButton(self._false_button)

        if self._default_value:
            self._true_button.setChecked(True)
        else:
            self._false_button.setChecked(True)

    def get_value(self) -> bool:
        return self._true_button.isChecked()

    def set_value(self, value: bool):
        if value is None:
            value = False
        if value:
            self._true_button.setChecked(True)
        else:
            self._false_button.setChecked(True)


class BoolValue(ValueTypeBase):

    def __init__(self, default_value: bool = False):
        # do cast, if failed, an error will be raised
        super().__init__(bool(default_value))

    def validate(self, value: Any) -> bool:
        return isinstance(value, bool)

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> None:
        return None

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return self.create_cell_widget(parent, *args, **kwargs)

    def create_cell_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return BoolValueEditor(parent, self.default_value)
