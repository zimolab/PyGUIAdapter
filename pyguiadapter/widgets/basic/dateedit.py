import dataclasses
from datetime import date

from qtpy.QtCore import Qt, QDate
from qtpy.QtWidgets import QWidget, QDateEdit
from typing import Type, Union, Optional, Any

from ..common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)
from ...utils import type_check

Alignment = Qt.AlignmentFlag
TimeSpec = Qt.TimeSpec


@dataclasses.dataclass(frozen=True)
class DateEditConfig(CommonParameterWidgetConfig):
    """DateEdit的配置类。"""

    default_value: Union[date, QDate, None] = date.today()
    """控件的默认值"""

    min_date: Union[date, QDate, None] = None
    """控件的最小日期"""

    max_date: Union[date, QDate, None] = None
    """控件的最大日期"""

    display_format: Optional[str] = None
    """日期的显示格式，可以参考Qt官方文档：
    [displayFormat](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QDateTimeEdit.html#PySide2.QtWidgets.PySide2.QtWidgets.QDateTimeEdit.displayFormat)
    """

    time_spec: Optional[TimeSpec] = None
    """时间日期标准，可以参考Qt官方文档:
    [TimeSpec](https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.TimeSpec)
    """

    alignment: Alignment = Qt.AlignLeft | Qt.AlignVCenter
    """对齐方式，可选值有：AlignLeft、AlignRight、AlignCenter、AlignJustify等。"""

    calendar_popup: bool = False
    """是否显示日历弹窗"""

    @classmethod
    def target_widget_class(cls) -> Type["DateEdit"]:
        return DateEdit


class DateEdit(CommonParameterWidget):
    ConfigClass = DateEditConfig

    AlignLeft = Qt.AlignLeft
    """对齐方式：左对齐"""

    AlignRight = Qt.AlignRight
    """对齐方式：右对齐"""

    AlignCenter = Qt.AlignCenter
    """对齐方式：居中对齐"""

    AlignJustify = Qt.AlignJustify
    """对齐方式：两端对齐"""

    LocalTime = Qt.LocalTime
    """时间日期的标准：本地时间"""

    UTC = Qt.UTC
    """时间日期的标准：UTC"""

    OffsetFromUTC = Qt.OffsetFromUTC
    """时间日期的标准：OffsetFromUTC"""

    TimeZone = Qt.TimeZone
    """时间日期的标准：TimeZone"""

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: DateEditConfig,
    ):
        self._value_widget: Optional[QDateEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QDateEdit:
        self._config: DateEditConfig
        if self._value_widget is None:
            self._value_widget = QDateEdit(self)
            if self._config.min_date is not None:
                self._value_widget.setMinimumDate(QDate(self._config.min_date))

            if self._config.max_date is not None:
                self._value_widget.setMaximumDate(QDate(self._config.max_date))

            if self._config.display_format is not None:
                self._value_widget.setDisplayFormat(self._config.display_format)

            if self._config.time_spec is not None:
                self._value_widget.setTimeSpec(self._config.time_spec)
            self._value_widget.setAlignment(self._config.alignment)
            self._value_widget.setCalendarPopup(self._config.calendar_popup)
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (date, QDate), allow_none=True)

    def set_value_to_widget(self, value: Union[date, QDate]):
        if isinstance(value, QDate):
            pass
        elif isinstance(value, date):
            value = QDate(value)
        else:
            raise TypeError(f"invalid type: {type(value)}")
        self._value_widget.setDate(value)

    def get_value_from_widget(self) -> date:
        value = self._value_widget.date()
        return value.toPython()
