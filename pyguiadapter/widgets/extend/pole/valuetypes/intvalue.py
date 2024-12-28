from typing import Optional, Any

from qtpy.QtCore import QModelIndex
from qtpy.QtWidgets import QWidget, QSpinBox, QStyleOptionViewItem

from .base import ValueWidgetMixin, ValueTypeBase


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

    def cast_value(self, value: Any) -> int:
        return int(value)

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: int):
        if value is None:
            value = DEFAULT_VALUE
        if not isinstance(value, int):
            value = self.cast_value(value)
        self.setValue(value)


class IntValue(ValueTypeBase):
    def __init__(
        self,
        default_value: int = DEFAULT_VALUE,
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

    def on_create_editor(
        self,
        parent: QWidget,
        option: Optional[QStyleOptionViewItem],
        index: Optional[QModelIndex],
        **kwargs,
    ) -> QWidget:
        _ = option, index, kwargs  # unused
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

    def on_create_edit(self, parent: QWidget, **kwargs) -> QWidget:
        return self.on_create_editor(parent, None, None)
