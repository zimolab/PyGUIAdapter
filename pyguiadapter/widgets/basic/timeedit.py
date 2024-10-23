import dataclasses
from datetime import time, datetime
from typing import Type, Union, Optional, Any

from qtpy.QtCore import Qt, QTime
from qtpy.QtWidgets import QWidget, QTimeEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check

Alignment = Qt.AlignmentFlag
TimeSpec = Qt.TimeSpec


@dataclasses.dataclass(frozen=True)
class TimeEditConfig(CommonParameterWidgetConfig):
    """TimeEdit的配置类"""

    default_value: Union[time, QTime, None] = datetime.now().time()
    """控件的默认值"""

    min_time: Union[time, QTime, None] = None
    """控件的最小时间值"""

    max_time: Union[time, QTime, None] = None
    """控件的最大时间值"""

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

    @classmethod
    def target_widget_class(cls) -> Type["TimeEdit"]:
        return TimeEdit


class TimeEdit(CommonParameterWidget):
    ConfigClass = TimeEditConfig

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
        config: TimeEditConfig,
    ):
        self._value_widget: Optional[QTimeEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: TimeEditConfig
        if self._value_widget is None:
            self._value_widget = QTimeEdit(self)
            if self._config.min_time is not None:
                self._value_widget.setMinimumTime(QTime(self._config.min_time))

            if self._config.max_time is not None:
                self._value_widget.setMaximumTime(QTime(self._config.max_time))

            if self._config.display_format is not None:
                self._value_widget.setDisplayFormat(self._config.display_format)

            if self._config.time_spec is not None:
                self._value_widget.setTimeSpec(self._config.time_spec)

            self._value_widget.setAlignment(self._config.alignment)

        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, allowed_types=(time, QTime), allow_none=True)

    def set_value_to_widget(self, value: Union[time, QTime]):
        if isinstance(value, QTime):
            pass
        elif isinstance(value, time):
            value = QTime(value)
        else:
            raise TypeError(f"invalid type: {type(value)}")
        self._value_widget.setTime(value)

    def get_value_from_widget(self) -> time:
        value = self._value_widget.time()
        return value.toPython()
