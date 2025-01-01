import datetime
from typing import Any, Union, Optional

from qtpy.QtCore import QTime, Qt
from qtpy.QtWidgets import QTimeEdit, QWidget

from ..schema import ValueType, ValueWidgetMixin

DEFAULT_VALUE = None
# default to ISO 8601 format
STR_FORMAT = "%H:%M:%S"
DISPLAY_FORMAT = "HH:mm:ss"
TIME_SPEC: Optional[Qt.TimeSpec] = None

TimeType = Union[datetime.time, QTime, str, None]


def to_string(value: TimeType, str_format: str = STR_FORMAT) -> str:
    if not value:
        value = datetime.datetime.now().time()
        return value.strftime(str_format)
    elif isinstance(value, str):
        value = datetime.datetime.strptime(value, str_format).time()
        return value.strftime(str_format)
    elif isinstance(value, datetime.time):
        return value.strftime(str_format)
    elif isinstance(value, QTime):
        return value.toPython().strftime(str_format)
    else:
        raise TypeError(f"unsupported time type: {type(value)}")


def to_qt_time(value: TimeType, str_format: str = STR_FORMAT) -> QTime:
    if not value:
        return QTime.currentTime()
    elif isinstance(value, QTime):
        return value
    elif isinstance(value, datetime.time):
        return QTime(value)
    elif isinstance(value, str):
        return QTime(datetime.datetime.strptime(value, str_format).time())
    else:
        raise TypeError(f"unsupported time type: {type(value)}")


def is_valid_time(value: TimeType, str_format: str = STR_FORMAT) -> bool:
    if value is None:
        return True
    if isinstance(value, (datetime.time, QTime)):
        return True
    elif isinstance(value, str):
        try:
            datetime.datetime.strptime(value, str_format)
            return True
        except ValueError:
            return False
    else:
        return False


class DateEdit(QTimeEdit, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        str_format: str = STR_FORMAT,
        display_format: str = DISPLAY_FORMAT,
        time_spec: Optional[Qt.TimeSpec] = None,
        minimum: Optional[TimeType] = None,
        maximum: Optional[TimeType] = None,
    ):
        self._default_value = default_value
        self._str_format = str_format
        self._display_format = display_format
        self._time_spec = time_spec

        super().__init__(parent)
        if self._display_format:
            self.setDisplayFormat(self._display_format)
        if self._time_spec:
            self.setTimeSpec(self._time_spec)
        if minimum:
            self.setMinimumTime(to_qt_time(minimum, self._str_format))
        if maximum:
            self.setMaximumTime(to_qt_time(maximum, self._str_format))

    def set_value(self, value: TimeType):
        self._default_value = to_qt_time(value, self._str_format)
        self.setTime(self._default_value)

    def get_value(self) -> str:
        return to_string(self.time(), self._str_format)


class TimeValue(ValueType):
    def __init__(
        self,
        default_value: TimeType = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        str_format: str = STR_FORMAT,
        display_format: str = DISPLAY_FORMAT,
        time_spec: Optional[Qt.TimeSpec] = TIME_SPEC,
        minimum: Optional[TimeType] = None,
        maximum: Optional[TimeType] = None,
    ):

        default_value = to_string(default_value)
        self.str_format = str_format
        self.display_format = display_format
        self.time_spec = time_spec
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(default_value, display_name=display_name)

    def validate(self, value: Any) -> bool:
        return is_valid_time(value, self.str_format)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return DateEdit(
            parent,
            self.default_value,
            str_format=self.str_format,
            display_format=self.display_format,
            time_spec=self.time_spec,
            minimum=self.minimum,
            maximum=self.maximum,
        )

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return DateEdit(
            parent,
            self.default_value,
            str_format=self.str_format,
            display_format=self.display_format,
            time_spec=self.time_spec,
            minimum=self.minimum,
            maximum=self.maximum,
        )
