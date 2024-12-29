from typing import Any, Union

from qtpy.QtWidgets import QWidget, QHBoxLayout, QComboBox, QRadioButton, QButtonGroup

from ..schema import ValueWidgetMixin, ValueType, CellWidgetMixin

TRUE_TEXT = "True"
FALSE_TEXT = "False"


class BoolCellWidget(QWidget, CellWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: bool = False,
        *,
        true_text: str = TRUE_TEXT,
        false_text: str = FALSE_TEXT,
    ):
        super().__init__(parent)

        self._default_value = default_value
        self._true_text = true_text
        self._false_text = false_text

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self._value_widget = QComboBox(self)
        self._value_widget.addItem(self._true_text, True)
        self._value_widget.addItem(self._false_text, False)
        self._layout.addWidget(self._value_widget)

    def get_value(self) -> bool:
        return self._value_widget.currentData()

    def set_value(self, value: bool):
        if value is None:
            value = False
        if value:
            self._value_widget.setCurrentIndex(0)
        else:
            self._value_widget.setCurrentIndex(1)


class BoolItemEditorWidget(QWidget, ValueWidgetMixin):
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

        if default_value:
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


class BoolValue(ValueType):

    def __init__(
        self,
        default_value: bool = False,
        *,
        true_text: str = TRUE_TEXT,
        false_text: str = FALSE_TEXT,
    ):
        # do cast, if failed, an error will be raised
        super().__init__(bool(default_value))
        self.true_text = true_text
        self.false_text = false_text

    def validate(self, value: Any) -> bool:
        return isinstance(value, bool)

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> None:
        return None

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return BoolItemEditorWidget(
            parent,
            self.default_value,
            true_text=self.true_text,
            false_text=self.false_text,
        )

    def create_cell_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return BoolCellWidget(
            parent,
            self.default_value,
            true_text=self.true_text,
            false_text=self.false_text,
        )
