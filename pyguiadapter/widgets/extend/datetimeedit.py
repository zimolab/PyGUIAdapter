from __future__ import annotations

import dataclasses
from datetime import datetime
from typing import Type, TypeVar

from qtpy.QtCore import Qt, QDateTime
from qtpy.QtWidgets import QWidget, QDateTimeEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


Alignment = Qt.Alignment
ButtonSymbols = QDateTimeEdit.ButtonSymbols
CorrectionMode = QDateTimeEdit.CorrectionMode
TimeSpec = Qt.TimeSpec


@dataclasses.dataclass(frozen=True)
class DateTimeEditConfig(CommonParameterWidgetConfig):
    default_value: datetime | QDateTime | None = None
    min_datetime: datetime | QDateTime | None = None
    max_datetime: datetime | QDateTime | None = None
    display_format: str | None = None
    time_spec: TimeSpec | None = None
    wrapping: bool = False
    frame: bool = True
    alignment: Alignment = Qt.AlignLeft | Qt.AlignVCenter
    button_symbols: ButtonSymbols | None = None
    correction_mode: CorrectionMode | None = None
    keyboard_tracking: bool = True
    accelerated: bool = False
    calendar_popup: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["DateTimeEdit"]:
        return DateTimeEdit


class DateTimeEdit(CommonParameterWidget):
    ConfigClass = DateTimeEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: DateTimeEditConfig,
    ):
        self._value_widget: QDateTimeEdit | None = None
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

            self._value_widget.setWrapping(self._config.wrapping)
            self._value_widget.setFrame(self._config.frame)
            self._value_widget.setAlignment(self._config.alignment)
            if self._config.button_symbols is not None:
                self._value_widget.setButtonSymbols(self._config.button_symbols)
            if self._config.correction_mode is not None:
                self._value_widget.setCorrectionMode(self._config.correction_mode)
            self._value_widget.setKeyboardTracking(self._config.keyboard_tracking)
            self._value_widget.setAccelerated(self._config.accelerated)
            self._value_widget.setCalendarPopup(self._config.calendar_popup)

        return self._value_widget

    def set_value_to_widget(self, value: datetime | QDateTime):
        if not isinstance(value, (datetime, QDateTime)):
            raise ValueError("value must be datetime or QDateTime")
        if isinstance(value, datetime):
            value = QDateTime(value)
        self._value_widget.setDateTime(value)

    def get_value_from_widget(self) -> datetime:
        value = self._value_widget.dateTime()
        return value.toPython()
