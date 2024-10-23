import dataclasses
from datetime import datetime

from qtpy.QtCore import Qt, QDateTime
from qtpy.QtWidgets import QWidget, QDateTimeEdit
from typing import Type, Union, Optional, Any

from ..common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)
from ...utils import type_check

Alignment = Qt.AlignmentFlag
TimeSpec = Qt.TimeSpec


@dataclasses.dataclass(frozen=True)
class DateTimeEditConfig(CommonParameterWidgetConfig):
    """DateTimeEdit的配置类。"""

    default_value: Union[datetime, QDateTime, None] = dataclasses.field(
        default_factory=datetime.now
    )
    """控件的默认值"""

    min_datetime: Union[datetime, QDateTime, None] = None
    """时间日期的最小值"""

    max_datetime: Union[datetime, QDateTime, None] = None
    """时间日期的最大值"""

    display_format: Optional[str] = None
    """时间日期的显示格式。可参考Qt官方文档：
    [displayFormat](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QDateTimeEdit.html#PySide2.QtWidgets.PySide2.QtWidgets.QDateTimeEdit.displayFormat)
    """

    time_spec: Optional[TimeSpec] = None
    """时间日期标准，可选值有：LocalTime、UTC、OffsetFromUTC、TimeZone。
    可参考Qt官方文档：
    [TimeSpec](https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.TimeSpec)
    """

    alignment: Alignment = Qt.AlignLeft | Qt.AlignVCenter
    """对齐方式，可选值有：AlignLeft、AlignRight、AlignCenter、AlignJustify等。"""

    calendar_popup: bool = True
    """是否显示日历弹窗"""

    @classmethod
    def target_widget_class(cls) -> Type["DateTimeEdit"]:
        return DateTimeEdit


class DateTimeEdit(CommonParameterWidget):
    ConfigClass = DateTimeEditConfig

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
        config: DateTimeEditConfig,
    ):
        self._value_widget: Optional[QDateTimeEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: DateTimeEditConfig
        if self._value_widget is None:
            self._value_widget = QDateTimeEdit(self)
            if self._config.min_datetime is not None:
                self._value_widget.setMinimumDateTime(
                    QDateTime(self._config.min_datetime)
                )

            if self._config.max_datetime is not None:
                self._value_widget.setMaximumDateTime(
                    QDateTime(self._config.max_datetime)
                )

            if self._config.display_format is not None:
                self._value_widget.setDisplayFormat(self._config.display_format)

            if self._config.time_spec is not None:
                self._value_widget.setTimeSpec(self._config.time_spec)

            if self._config.alignment is not None:
                self._value_widget.setAlignment(self._config.alignment)

            self._value_widget.setCalendarPopup(self._config.calendar_popup)
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (datetime, QDateTime), allow_none=True)

    def set_value_to_widget(self, value: Union[datetime, QDateTime]):
        if isinstance(value, QDateTime):
            pass
        elif isinstance(value, datetime):
            value = QDateTime(value)
        else:
            raise TypeError(f"invalid type: {type(value)}")
        self._value_widget.setDateTime(value)

    def get_value_from_widget(self) -> datetime:
        value = self._value_widget.dateTime()
        return value.toPython()
