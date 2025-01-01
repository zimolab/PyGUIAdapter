import datetime
from typing import Any, Union, Optional

from qtpy.QtCore import QDate, Qt
from qtpy.QtWidgets import QDateEdit, QWidget

from ..schema import ValueType, ValueWidgetMixin

DEFAULT_VALUE = None
# default to ISO 8601 format
STR_FORMAT = "%Y-%m-%d"
DISPLAY_FORMAT = "yyyy-MM-dd"
TIME_SPEC: Optional[Qt.TimeSpec] = None
CALENDAR_POPUP = True

DateType = Union[datetime.date, QDate, str, None]


def to_string(value: DateType, str_format: str = STR_FORMAT) -> str:
    if not value:
        value = datetime.date.today()
        return value.strftime(str_format)
    elif isinstance(value, str):
        return datetime.date.strftime(
            datetime.datetime.strptime(value, str_format), str_format
        )
    elif isinstance(value, datetime.date):
        return value.strftime(str_format)
    elif isinstance(value, QDate):
        return value.toPython().strftime(str_format)
    else:
        raise TypeError(f"unsupported date type: {type(value)}")


def to_qt_date(value: DateType, str_format: str = STR_FORMAT) -> QDate:
    if not value:
        return QDate.currentDate()
    elif isinstance(value, QDate):
        return value
    elif isinstance(value, datetime.date):
        return QDate(value)
    elif isinstance(value, str):
        return QDate(datetime.datetime.strptime(value, str_format))
    else:
        raise TypeError(f"unsupported date type: {type(value)}")


def is_valid_date(value: DateType, str_format: str = STR_FORMAT) -> bool:
    if value is None:
        return True
    if isinstance(value, (datetime.datetime, QDate)):
        return True
    elif isinstance(value, str):
        try:
            datetime.datetime.strptime(value, str_format)
            return True
        except ValueError:
            return False
    else:
        return False


class DateEdit(QDateEdit, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        str_format: str = STR_FORMAT,
        calendar_popup: bool = CALENDAR_POPUP,
        display_format: str = DISPLAY_FORMAT,
        time_spec: Optional[Qt.TimeSpec] = None,
        minimum: Optional[DateType] = None,
        maximum: Optional[DateType] = None,
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

        if maximum:
            self.setMaximumDate(to_qt_date(maximum, self._str_format))

        if minimum:
            self.setMinimumDate(to_qt_date(minimum, self._str_format))

    def set_value(self, value: DateType):
        self._default_value = to_qt_date(value, self._str_format)
        self.setDate(self._default_value)

    def get_value(self) -> str:
        return to_string(self.date(), self._str_format)


class DateValue(ValueType):
    def __init__(
        self,
        default_value: DateType = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        str_format: str = STR_FORMAT,
        display_format: str = DISPLAY_FORMAT,
        calendar_popup: bool = CALENDAR_POPUP,
        time_spec: Optional[Qt.TimeSpec] = TIME_SPEC,
        maximum: Optional[DateType] = None,
        minimum: Optional[DateType] = None,
    ):

        default_value = to_string(default_value)
        self.str_format = str_format
        self.display_format = display_format
        self.calendar_popup = calendar_popup
        self.time_spec = time_spec
        self.maximum = maximum
        self.minimum = minimum

        super().__init__(default_value, display_name=display_name)

    def validate(self, value: Any) -> bool:
        return is_valid_date(value, self.str_format)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return DateEdit(
            parent,
            self.default_value,
            str_format=self.str_format,
            calendar_popup=self.calendar_popup,
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
            calendar_popup=self.calendar_popup,
            display_format=self.display_format,
            time_spec=self.time_spec,
            minimum=self.minimum,
            maximum=self.maximum,
        )
