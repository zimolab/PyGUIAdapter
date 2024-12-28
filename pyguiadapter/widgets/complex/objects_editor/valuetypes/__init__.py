from typing import Optional, Any, Union

from qtpy.QtWidgets import (
    QWidget,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QTableWidgetItem,
)

from ...schema import ValueWidgetMixin, ValueTypeBase

DEFAULT_VALUE = 0


class IntValueEditor(QSpinBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: int,
        *,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        step: Optional[int] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ):
        super().__init__(parent)
        if max_value is not None:
            self.setMaximum(max_value)
        if min_value is not None:
            self.setMinimum(min_value)
        if step is not None:
            self.setSingleStep(step)
        if prefix is not None:
            self.setPrefix(prefix)
        if suffix is not None:
            self.setSuffix(suffix)

        self.setValue(default_value)

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: int):
        if value is None:
            value = DEFAULT_VALUE
        if not isinstance(value, int):
            value = self.cast(value)
        self.setValue(value)


class IntValue(ValueTypeBase):

    def __init__(
        self,
        default_value: int = 0,
        *,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        step: Optional[int] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ):
        super().__init__(default_value)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.prefix = prefix
        self.suffix = suffix

    def validate(self, value: Any) -> bool:
        return isinstance(value, int)

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> QWidget:
        editor = IntValueEditor(
            parent,
            default_value=self.default_value,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            prefix=self.prefix,
            suffix=self.suffix,
        )
        return editor

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return self.create_item_delegate_widget(parent, *args, **kwargs)

    def hook_create_item(self) -> bool:
        return False

    def hook_set_item_data(self) -> bool:
        return True

    def on_create_item(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        print(f"create item: {row}, {col}, {data}")

    def on_set_item_data(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        print(f"set item data: {row}, {col}, {data}")


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

    def cast(self, original_value: Any) -> str:
        return str(original_value)

    def get_value(self) -> str:
        return self.text()

    def set_value(self, value: str):
        if value is None:
            value = ""
        if not isinstance(value, str):
            value = str(value)
        self.setText(value)


class StringValue(ValueTypeBase):

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def __init__(self, default_value: str = "", *, placeholder: Optional[str] = None):
        super().__init__(default_value)
        self.placeholder = placeholder

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> QWidget:
        editor = StringValueEditor(
            parent, default_value=self.default_value, placeholder=self.placeholder
        )
        return editor

    def create_item_editor_widget(self, parent: QWidget, *args, **kwargs) -> QWidget:
        return self.create_item_delegate_widget(parent, *args, **kwargs)


class FilePathValueEdit(QWidget, ValueWidgetMixin):
    def __init__(
        self, parent: QWidget, default_value: str, *, placeholder: Optional[str] = None
    ):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._edit = QLineEdit(self)
        self._edit.setText(default_value)
        self._layout.addWidget(self._edit, 9)

        self._button = QPushButton(self)
        self._button.setText("...")
        self._button.clicked.connect(self._on_button_clicked)
        self._layout.addWidget(self._button, 1)

    def set_value(self, value: Any):
        self._edit.setText(value)

    def get_value(self) -> Any:
        return self._edit.text()

    def _on_button_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*)"
        )
        if file_path:
            self._edit.setText(file_path)


class FilePathValue(ValueTypeBase):

    def __init__(self, default_value: str = ""):
        super().__init__(str(default_value))

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def hook_item_double_clicked(self) -> bool:
        return True

    def hook_item_clicked(self) -> bool:
        return False

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return FilePathValueEdit(parent, self.default_value)

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> None:
        return None

    def on_item_double_clicked(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        print(f"Double clicked: {data}")

    def on_item_clicked(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        print(f"Clicked: {data}")
