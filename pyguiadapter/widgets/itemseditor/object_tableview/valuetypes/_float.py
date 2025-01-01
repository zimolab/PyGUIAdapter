from typing import Optional, Any, Union

from qtpy.QtWidgets import QWidget, QDoubleSpinBox

from ..schema import ValueWidgetMixin, ValueType

DEFAULT_VALUE = 0.0
STEP = 0.001
DECIMALS = 3
MIN_VALUE = -2147483648.0
MAX_VALUE = 2147483647.0
PREFIX = ""
SUFFIX = ""


class FloatValueEditor(QDoubleSpinBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: float = DEFAULT_VALUE,
        *,
        min_value: Optional[float] = MIN_VALUE,
        max_value: Optional[float] = MAX_VALUE,
        step: Optional[float] = STEP,
        decimals: Optional[int] = DECIMALS,
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
        if decimals is not None:
            self.setDecimals(decimals)
        if prefix is not None:
            self.setPrefix(prefix)
        if suffix is not None:
            self.setSuffix(suffix)

        self.setValue(default_value)

    def get_value(self) -> float:
        return self.value()

    def set_value(self, value: float):
        if value is None:
            value = DEFAULT_VALUE
        self.setValue(float(value))


class FloatValue(ValueType):

    def __init__(
        self,
        default_value: float = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        min_value: Optional[float] = MIN_VALUE,
        max_value: Optional[float] = MAX_VALUE,
        step: Optional[float] = STEP,
        decimals: Optional[int] = DECIMALS,
        prefix: Optional[str] = SUFFIX,
        suffix: Optional[str] = SUFFIX,
    ):
        # do cast, if failed, an error will be raised
        super().__init__(float(default_value), display_name=display_name)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals

    def validate(self, value: Any) -> bool:
        return isinstance(value, (int, float))

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> QWidget:
        editor = FloatValueEditor(
            parent,
            default_value=self.default_value,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            decimals=self.decimals,
            prefix=self.prefix,
            suffix=self.suffix,
        )
        return editor

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return self.create_item_delegate_widget(parent, *args, **kwargs)
