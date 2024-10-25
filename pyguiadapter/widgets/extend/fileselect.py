import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Any, List, Tuple, Set, Optional, Union, Sequence

from ._path import PathSelectWidget
from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class FileSelectConfig(CommonParameterWidgetConfig):
    """FileSelect的配置类。"""

    default_value: Optional[str] = ""
    """默认值"""

    placeholder: str = ""
    """占位符文字"""

    dialog_title: str = ""
    """文件对话框标题"""

    start_dir: str = ""
    """文件对话框起始路径"""

    filters: str = ""
    """文件对话框的文件过滤器"""

    save_file: bool = False
    """是否为保存文件对话框"""

    select_button_text: str = "..."
    """选择按钮文字"""

    clear_button: bool = False
    """是否显示清除按钮"""

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
    """MultiFileSelect的配置类。"""

    default_value: Union[Sequence[str], str, type(None)] = ()
    """默认值"""

    placeholder: str = ""
    """占位符文字"""

    dialog_title: str = ""
    """文件对话框标题"""

    start_dir: str = ""
    """文件对话框起始路径"""

    filters: str = ""
    """文件对话框的文件过滤器"""

    file_separator: str = ";;"
    """文件分隔符"""

    select_button_text: str = "..."
    """选择按钮文字"""

    clear_button: bool = False
    """是否显示清除按钮"""

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
