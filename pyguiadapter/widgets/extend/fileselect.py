import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Any, List, Tuple, Set, Optional, Union, Sequence

from ._path import PathSelectWidget
from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class FileSelectConfig(CommonParameterWidgetConfig):
    default_value: Optional[str] = ""
    placeholder: str = ""
    dialog_title: str = ""
    start_dir: str = ""
    filters: str = ""
    save_file: bool = False
    select_button_text: str = "..."
    clear_button: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["FileSelect"]:
        return FileSelect


class FileSelect(CommonParameterWidget):
    ConfigClass = FileSelectConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: FileSelectConfig
    ):
        self._value_widget: Optional[PathSelectWidget] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> PathSelectWidget:
        self._config: FileSelectConfig
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

    def check_value_type(self, value: Any):
        type_check(value, (str,), allow_none=True)

    def set_value_to_widget(self, value: Any):
        value = value or ""
        self._value_widget.set_path(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.get_path()


@dataclasses.dataclass(frozen=True)
class MultiFileSelectConfig(CommonParameterWidgetConfig):
    default_value: Union[Sequence[str], str, type(None)] = ()
    placeholder: str = ""
    dialog_title: str = ""
    start_dir: str = ""
    filters: str = ""
    file_separator: str = ";;"
    select_button_text: str = "..."
    clear_button: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["MultiFileSelect"]:
        return MultiFileSelect


class MultiFileSelect(CommonParameterWidget):

    ConfigClass = MultiFileSelectConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: MultiFileSelectConfig,
    ):
        self._value_widget: Optional[PathSelectWidget] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> PathSelectWidget:
        self._config: MultiFileSelectConfig
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

    def check_value_type(self, value: Any):
        type_check(value, (str, list, tuple, set), allow_none=True)

    def set_value_to_widget(
        self, value: Union[str, List[str], Tuple[str, ...], Set[str]]
    ):
        value = value or []
        self._value_widget.set_paths(value)

    def get_value_from_widget(self) -> List[str]:
        return self._value_widget.get_paths()
