import abc
import inspect
from datetime import datetime, date, time
from typing import Any, Union, Optional, Dict

from PyQt6.QtCore import QDateTime, QDate, QTime
from PyQt6.QtGui import QColor
from function2widgets import Color

from pyguiadapter.tools.easyconfigs.constants import (
    DEFAULT_QUOTE,
    PARAM_LABEL_PREFIX,
    PARAM_DESC_PREFIX,
    PARAM_DEFAULT_VALUE_DESC_PREFIX,
    PARAM_DEFAULT_VALUE_PREFIX,
    DEFAULT_VALUE_DESC,
    DEFAULT_TR_FUNCTION,
)


class BaseValueMapper(abc.ABC):
    @abc.abstractmethod
    def map(self, raw_value: Any) -> Any:
        pass


class ColorMapper(BaseValueMapper):

    def __init__(self, ctx: "ConstNameValueHelper"):
        self._ctx = ctx

    def map(self, raw_value: Union[Color, QColor, None]) -> Optional[str]:
        if not isinstance(raw_value, (Color, QColor)):
            return None

        if isinstance(raw_value, Color):
            color_str_literal = self._ctx.make_str_literal(raw_value.to_hex_string())
            return f"Color.from_string({color_str_literal})"
        else:
            color_str_literal = self._ctx.make_str_literal(raw_value.name())
            return f"QColor.fromString({color_str_literal})"


class DateTimeMapper(BaseValueMapper):

    def map(
        self, raw_value: Union[datetime, date, time, QDateTime, QDate, QTime, None]
    ) -> Optional[str]:
        if not isinstance(raw_value, (datetime, date, time, QDateTime, QDate, QTime)):
            return None

        if isinstance(raw_value, datetime):
            return "datetime.now()"
        elif isinstance(raw_value, date):
            return "date.today()"
        elif isinstance(raw_value, time):
            return "time()"
        elif isinstance(raw_value, QDateTime):
            return "QDateTime.currentDateTime()"
        elif isinstance(raw_value, QDate):
            return "QDate.currentDate()"
        elif isinstance(raw_value, QTime):
            return "QTime.currentTime()"
        else:
            raise ValueError(f"unsupported type: {type(raw_value)}")


class ListTupleDictMapper(BaseValueMapper):

    def map(self, raw_value: Union[list, tuple, dict]) -> Optional[str]:
        if not isinstance(raw_value, (list, tuple, dict)):
            return None

        value_type = type(raw_value)
        return value_type()


class ConstNameValueHelper(object):

    def __init__(
        self,
        str_quote: str = DEFAULT_QUOTE,
        param_label_prefix: str = PARAM_LABEL_PREFIX,
        param_description_prefix: str = PARAM_DESC_PREFIX,
        param_default_value_description_prefix: str = PARAM_DEFAULT_VALUE_DESC_PREFIX,
        param_default_value_prefix: str = PARAM_DEFAULT_VALUE_PREFIX,
        default_value_description_text: str = DEFAULT_VALUE_DESC,
        tr_function: str = DEFAULT_TR_FUNCTION,
    ):
        self._str_quote = str_quote
        self._param_label_prefix = param_label_prefix
        self._param_desc_prefix = param_description_prefix
        self._param_default_value_desc_prefix = param_default_value_description_prefix
        self._param_default_value_prefix = param_default_value_prefix
        self._default_value_desc = default_value_description_text
        self._tr_function = tr_function

        color_mapper = ColorMapper(self)
        datetime_mapper = DateTimeMapper()
        list_tuple_dict_mapper = ListTupleDictMapper()

        self._value_mappers: Dict[type, BaseValueMapper] = {
            Color: color_mapper,
            QColor: color_mapper,
            datetime: datetime_mapper,
            date: datetime_mapper,
            time: datetime_mapper,
            QDateTime: datetime_mapper,
            QDate: datetime_mapper,
            QTime: datetime_mapper,
            list: list_tuple_dict_mapper,
            tuple: list_tuple_dict_mapper,
            dict: list_tuple_dict_mapper,
        }

    def register_value_mapper(self, default_value_type: type, mapper: BaseValueMapper):
        self._value_mappers[default_value_type] = mapper

    def constname_param_label(self, param_name: str) -> str:
        return f"{self._param_label_prefix}{param_name.upper()}"

    def constname_param_description(self, param_name: str) -> str:
        return f"{self._param_desc_prefix}{param_name.upper()}"

    def constname_param_default_value_description(self, param_name: str) -> str:
        return f"{self._param_default_value_desc_prefix}{param_name.upper()}"

    def constname_param_default_value(self, param_name: str) -> str:
        return f"{self._param_default_value_prefix}{param_name.upper()}"

    def constvalue_param_default_value_description(self) -> str:
        return self.make_tr_str_literal(self._default_value_desc)

    def constvalue_param_label(self, label_text: str) -> str:
        return self.make_tr_str_literal(label_text)

    def constvalue_param_description(self, description_text: str) -> str:
        return self.make_tr_str_literal(description_text)

    def try_make_literal(self, raw_value: Any) -> Any:
        """
        尝试从raw_value中重建其字面量表示。
        注意：此方法并不保证总是可靠和有效，a）一些类型的值可能无法构建字面量表示，b）一些值构建的字面量表示可能与原始值不同。
        """
        if isinstance(raw_value, inspect.Parameter.empty):
            return None
        if isinstance(raw_value, (int, float, bool)):
            return raw_value
        if isinstance(raw_value, str):
            return self.make_str_literal(raw_value)

        mapper = self._value_mappers.get(type(raw_value), None)
        if mapper is None:
            return None
        return mapper.map(raw_value)

    def make_str_literal(self, value: str, multiline: Optional[bool] = None) -> str:
        if multiline is None:
            multiline = self.is_multiline_str(value)
        if multiline:
            return f"{self._str_quote * 3}{value}{self._str_quote * 3}"
        return f"{self._str_quote}{value}{self._str_quote}"

    def make_tr_str_literal(self, value: str, multiline: Optional[bool] = None) -> str:
        str_literal = self.make_str_literal(value, multiline)
        if not self._tr_function:
            return str_literal
        return self._tr_function + f"({str_literal})"

    @staticmethod
    def is_multiline_str(s: str) -> bool:
        return len(s.splitlines()) > 1
