import datetime
from typing import Any, Union, Optional

from qtpy.QtCore import QDateTime, Qt
from qtpy.QtWidgets import QDateTimeEdit, QWidget

from ..schema import ValueType, ValueWidgetMixin

DEFAULT_VALUE = None
# default to ISO 8601 format
STR_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DISPLAY_FORMAT = "yyyy-MM-dd HH:mm:ss"
TIME_SPEC: Optional[Qt.TimeSpec] = None
CALENDAR_POPUP = True

DateTimeType = Union[datetime.datetime, QDateTime, str, None]


def to_string(value: DateTimeType, str_format: str = STR_FORMAT) -> str:
    if not value:
        value = datetime.datetime.now()
        return value.strftime(str_format)
    elif isinstance(value, str):
        return datetime.datetime.strptime(value, str_format).strftime(str_format)
    elif isinstance(value, datetime.datetime):
        return value.strftime(str_format)
    elif isinstance(value, QDateTime):
        return value.toPython().strftime(str_format)
    else:
        raise TypeError(f"unsupported datetime type: {type(value)}")


# def to_datetime(value: DateTimeType, str_format: str = STR_FORMAT) -> datetime.datetime:
#     if not value:
#         return datetime.datetime.now()
#     elif isinstance(value, datetime.datetime):
#         return value
#     elif isinstance(value, str):
#         return datetime.datetime.strptime(value, str_format)
#     elif isinstance(value, QDateTime):
#         return value.toPython()
#     else:
#         raise TypeError(f"unsupported datetime type: {type(value)}")


def to_qt_datetime(value: DateTimeType, str_format: str = STR_FORMAT) -> QDateTime:
    if not value:
        return QDateTime.currentDateTime()
    elif isinstance(value, QDateTime):
        return value
    elif isinstance(value, datetime.datetime):
        return QDateTime(value)
    elif isinstance(value, str):
        return QDateTime(datetime.datetime.strptime(value, str_format))
    else:
        raise TypeError(f"unsupported datetime type: {type(value)}")


def is_valid_datetime(value: DateTimeType, str_format: str = STR_FORMAT) -> bool:
    if value is None:
        return True
    if isinstance(value, (datetime.datetime, QDateTime)):
        return True
    elif isinstance(value, str):
        try:
            datetime.datetime.strptime(value, str_format)
            return True
        except ValueError:
            return False
    else:
        return False


class DateTimeEdit(QDateTimeEdit, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        str_format: str = STR_FORMAT,
        calendar_popup: bool = CALENDAR_POPUP,
        display_format: str = DISPLAY_FORMAT,
        time_spec: Optional[Qt.TimeSpec] = None,
    ):
        self._default_value = default_value
        self._str_format = str_format
        self._display_format = display_format
        self._time_spec = time_spec

        super().__init__(parent)
        self.setCalendarPopup(calendar_popup)
        if self._display_format:
            self.setDisplayFormat(self._display_format)
        if self._time_spec:
            self.setTimeSpec(self._time_spec)

    def set_value(self, value: DateTimeType):
        self._default_value = to_qt_datetime(value, self._str_format)
        self.setDateTime(self._default_value)

    def get_value(self) -> str:
        return to_string(self.dateTime(), self._str_format)


class DateTimeValue(ValueType):
    def __init__(
        self,
        default_value: DateTimeType = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        str_format: str = STR_FORMAT,
        display_format: str = DISPLAY_FORMAT,
        calendar_popup: bool = CALENDAR_POPUP,
        time_spec: Optional[Qt.TimeSpec] = TIME_SPEC,
    ):

        default_value = to_string(default_value)
        self.str_format = str_format
        self.display_format = display_format
        self.calendar_popup = calendar_popup
        self.time_spec = time_spec

        super().__init__(default_value, display_name=display_name)

    def validate(self, value: Any) -> bool:
        return is_valid_datetime(value, self.str_format)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return DateTimeEdit(
            parent,
            self.default_value,
            str_format=self.str_format,
            calendar_popup=self.calendar_popup,
            display_format=self.display_format,
            time_spec=self.time_spec,
        )

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return DateTimeEdit(
            parent,
            self.default_value,
            str_format=self.str_format,
            calendar_popup=self.calendar_popup,
            display_format=self.display_format,
            time_spec=self.time_spec,
        )
