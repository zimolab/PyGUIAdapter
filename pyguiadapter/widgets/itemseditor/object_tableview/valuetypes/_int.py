from typing import Optional, Any

from qtpy.QtWidgets import QWidget, QSpinBox, QTableWidgetItem

from .. import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType
from ...utils import result_or_none

DEFAULT_VALUE = 0
STEP = 1
MIN_VALUE = -2147483648
MAX_VALUE = 2147483647
PREFIX = ""
SUFFIX = ""
DISPLAY_AFFIX = False


def _to_int(value: Any) -> int:
    if value is None:
        return DEFAULT_VALUE
    return int(value)


class IntEdit(QSpinBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: int,
        *,
        min_value: Optional[int],
        max_value: Optional[int],
        step: Optional[int],
        prefix: Optional[str],
        suffix: Optional[str],
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

        self.set_value(default_value)

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: int):
        self.setValue(_to_int(value))


class IntValue(ValueType):

    def __init__(
        self,
        default_value: int = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        min_value: Optional[int] = MIN_VALUE,
        max_value: Optional[int] = MAX_VALUE,
        step: Optional[int] = STEP,
        prefix: Optional[str] = PREFIX,
        suffix: Optional[str] = SUFFIX,
        display_affix: bool = DISPLAY_AFFIX,
    ):
        super().__init__(_to_int(default_value), display_name=display_name)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.prefix = prefix
        self.suffix = suffix
        self.display_affix = display_affix

    def validate(self, value: Any) -> bool:
        value = result_or_none(_to_int, value)
        if value is None:
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> IntEdit:
        return IntEdit(
            parent,
            default_value=self.default_value,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            prefix=self.prefix,
            suffix=self.suffix,
        )

    def create_item_editor_widget(self, parent: QWidget, *args, **kwargs) -> IntEdit:
        return self.create_item_delegate_widget(parent)

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        if not self.display_affix:
            return
        display_text = f"{self.prefix}{value}{self.suffix}"
        item.setText(display_text)
