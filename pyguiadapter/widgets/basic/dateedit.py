from __future__ import annotations

import dataclasses
from datetime import date
from typing import Type

from qtpy.QtCore import Qt, QDate
from qtpy.QtWidgets import QWidget, QDateEdit

from ..common import (
    CommonParameterWidgetConfig,
    CommonParameterWidget,
)

Alignment = Qt.Alignment
ButtonSymbols = QDateEdit.ButtonSymbols
CorrectionMode = QDateEdit.CorrectionMode
TimeSpec = Qt.TimeSpec


@dataclasses.dataclass(frozen=True)
class DateEditConfig(CommonParameterWidgetConfig):
    default_value: date | QDate | None = date.today()
    min_date: date | QDate | None = None
    max_date: date | QDate | None = None
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
    def target_widget_class(cls) -> Type["DateEdit"]:
        return DateEdit


class DateEdit(CommonParameterWidget):
    ConfigClass = DateEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: DateEditConfig,
    ):
        self._value_widget: QDateEdit | None = None
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

    def set_value_to_widget(self, value: date | QDate):
        if not isinstance(value, (date, QDate)):
            raise ValueError("value must be date or QDate")
        if isinstance(value, date):
            value = QDate(value)
        self._value_widget.setDate(value)

    def get_value_from_widget(self) -> date:
        value = self._value_widget.date()
        return value.toPython()
