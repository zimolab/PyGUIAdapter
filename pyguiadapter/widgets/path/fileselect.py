from __future__ import annotations

import dataclasses
from email.policy import default
from typing import Type, Any, TypeVar, List, Tuple, Set

from qtpy.QtWidgets import QWidget

from ._widget import PathSelectWidget
from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...exceptions import ParameterValidationError


@dataclasses.dataclass(frozen=True)
class FileSelectConfig(CommonParameterWidgetConfig):
    default_value: str = ""
    placeholder: str = ""
    dialog_title: str = "Select File"
    start_dir: str = ""
    filters: str = ""
    save_file: bool = False
    select_button_text: str = "..."
    clear_button: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["FileSelect"]:
        return FileSelect


class FileSelect(CommonParameterWidget):

    Self = TypeVar("Self", bound="FileSelect")
    ConfigClass = FileSelectConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: FileSelectConfig
    ):
        self._config: FileSelectConfig = config
        self._value_widget: PathSelectWidget | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> PathSelectWidget:
        if self._value_widget is None:
            self._value_widget = PathSelectWidget(
                self,
                select_directory=False,
                open_file=not self._config.save_file,
                save_file=self._config.save_file,
                multiple_files=False,
                select_button_text=self._config.select_button_text,
                dialog_title=self._config.dialog_title,
                start_dir=self._config.start_dir,
                filters=self._config.filters,
                placeholder=self._config.placeholder,
                clear_button=self._config.clear_button,
            )
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        value = value or ""
        self._value_widget.set_path(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.get_path()


@dataclasses.dataclass(frozen=True)
class MultiFileSelectConfig(CommonParameterWidgetConfig):
    default_value: List[str] = dataclasses.field(default_factory=list)
    placeholder: str = ""
    dialog_title: str = "Select Files"
    start_dir: str = ""
    filters: str = ""
    file_separator: str = ";;"
    select_button_text: str = "..."
    clear_button: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["MultiFileSelect"]:
        return MultiFileSelect


class MultiFileSelect(CommonParameterWidget):

    Self = TypeVar("Self", bound="MultiFileSelect")
    ConfigClass = MultiFileSelectConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: MultiFileSelectConfig
    ):
        self._config: MultiFileSelectConfig = config
        self._value_widget: PathSelectWidget | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> PathSelectWidget:
        if self._value_widget is None:
            self._value_widget = PathSelectWidget(
                self,
                select_directory=False,
                open_file=True,
                save_file=False,
                multiple_files=True,
                select_button_text=self._config.select_button_text,
                dialog_title=self._config.dialog_title,
                start_dir=self._config.start_dir,
                filters=self._config.filters,
                placeholder=self._config.placeholder,
                clear_button=self._config.clear_button,
                file_separator=self._config.file_separator,
            )
        return self._value_widget

    def set_value_to_widget(self, value: str | List[str] | Tuple[str, ...] | Set[str]):
        value = value or []
        if not isinstance(value, (str, list, tuple, set)):
            raise ParameterValidationError(
                self.parameter_name,
                f"invalid type of value, expect str or a sequence of str, got {type(value)}",
            )
        self._value_widget.set_paths(value)

    def get_value_from_widget(self) -> List[str]:
        return self._value_widget.get_paths()
