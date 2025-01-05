from typing import Optional, Any, Union

from qtpy.QtWidgets import QWidget, QDoubleSpinBox, QTableWidgetItem

from ..object_tableview import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType
from ..utils import result_or_none

DEFAULT_VALUE = 0.0
STEP = 0.001
DECIMALS = 3
MIN_VALUE = -2147483648.0
MAX_VALUE = 2147483647.0
PREFIX = ""
SUFFIX = ""
DISPLAY_AFFIX = False
DISPLAY_AS_DECIMALS = False


def _to_float(value: Any) -> float:
    if value is None:
        return DEFAULT_VALUE
    return float(value)


class FloatEdit(QDoubleSpinBox, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: float,
        *,
        min_value: Optional[float],
        max_value: Optional[float],
        step: Optional[float],
        decimals: Optional[int],
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
        self.setValue(_to_float(value))


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
        display_affix: bool = DISPLAY_AFFIX,
        display_as_decimals: bool = DISPLAY_AS_DECIMALS,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.display_affix = display_affix
        self.display_as_decimals = display_as_decimals

        # do cast, if failed, an error will be raised
        super().__init__(float(default_value), display_name=display_name)

    def validate(self, value: Any) -> bool:
        value = result_or_none(_to_float, value)
        if value is None:
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> QWidget:
        return FloatEdit(
            parent,
            default_value=self.default_value,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            decimals=self.decimals,
            prefix=self.prefix,
            suffix=self.suffix,
        )

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return self.create_item_delegate_widget(parent)

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        if self.display_as_decimals and self.decimals:
            value = f"{value:.{self.decimals}f}"
        else:
            value = str(value)
        if self.display_affix:
            value = f"{self.prefix}{value}{self.suffix}"
        item.setText(value)
