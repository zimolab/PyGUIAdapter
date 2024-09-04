from __future__ import annotations

import dataclasses
from typing import Type, Any, TypeVar

from qtpy.QtWidgets import QWidget

from ._widget import PathSelectWidget
from ..common import CommonParameterWidgetConfig, CommonParameterWidget


@dataclasses.dataclass(frozen=True)
class DirSelectConfig(CommonParameterWidgetConfig):
    default_value: str = ""
    placeholder: str = ""
    dialog_title: str = "Select Directory"
    start_dir: str = ""
    select_button_text: str = "..."
    clear_button: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["DirSelect"]:
        return DirSelect


class DirSelect(CommonParameterWidget):

    Self = TypeVar("Self", bound="DirSelect")
    ConfigClass = DirSelectConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: DirSelectConfig
    ):
        self._config: DirSelectConfig = config
        self._value_widget: PathSelectWidget | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget: PathSelectWidget = PathSelectWidget(
                self,
                select_directory=True,
                open_file=False,
                save_file=False,
                multiple_files=False,
                select_button_text=self._config.select_button_text,
                dialog_title=self._config.dialog_title,
                start_dir=self._config.start_dir,
                filters=None,
                placeholder=self._config.placeholder,
                clear_button=self._config.clear_button,
            )
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        value = value or ""
        self._value_widget.set_path(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.get_path()
