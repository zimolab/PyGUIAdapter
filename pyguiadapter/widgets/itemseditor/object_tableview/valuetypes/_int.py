from typing import Optional, Any, Union

from qtpy.QtWidgets import QWidget, QSpinBox

from ..schema import ValueWidgetMixin, ValueType

DEFAULT_VALUE = 0
STEP = 1
MIN_VALUE = -2147483648
MAX_VALUE = 2147483647
PREFIX = ""
SUFFIX = ""


class IntValueEditor(QSpinBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: int = DEFAULT_VALUE,
        *,
        min_value: Optional[int] = MIN_VALUE,
        max_value: Optional[int] = MAX_VALUE,
        step: Optional[int] = STEP,
        prefix: Optional[str] = SUFFIX,
        suffix: Optional[str] = SUFFIX,
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
        self.setValue(int(value))


class IntValue(ValueType):

    def __init__(
        self,
        default_value: int = DEFAULT_VALUE,
        *,
        min_value: Optional[int] = MIN_VALUE,
        max_value: Optional[int] = MAX_VALUE,
        step: Optional[int] = STEP,
        prefix: Optional[str] = PREFIX,
        suffix: Optional[str] = SUFFIX,
    ):
        # do cast, if failed, an error will be raised
        super().__init__(int(default_value))

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
