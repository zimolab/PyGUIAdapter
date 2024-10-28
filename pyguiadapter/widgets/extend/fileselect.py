import dataclasses
import os
from typing import Type, Any, List, Tuple, Set, Optional, Union, Sequence

from qtpy.QtCore import QMimeData, QUrl
from qtpy.QtWidgets import QWidget

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

    drag_n_drop: bool = True
    """是否启用文件拖放功能"""

    normalize_path: bool = False
    """是否将路径标准化。若设置为True，则在获取路径时，将使用os.path.normpath()函数进行标准化"""

    absolutize_path: bool = False
    """是否将路径绝对化。若设置为True，则在获取路径时，将使用os.path.abspath()函数进行绝对化"""

    @classmethod
    def target_widget_class(cls) -> Type["FileSelect"]:
        return FileSelect


class FileSelect(CommonParameterWidget):
    ConfigClass = FileSelectConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: FileSelectConfig
    ):
        self._config: FileSelectConfig
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
        self._config: FileSelectConfig
        value = value or ""
        value = str(value)
        self._value_widget.set_path(value)

    def get_value_from_widget(self) -> str:
        self._config: FileSelectConfig
        value = self._value_widget.get_path()
        if self._config.normalize_path:
            value = os.path.normpath(value)
        if self._config.absolutize_path:
            value = os.path.abspath(value)
        return value

    def on_drag(self, mime_data: QMimeData) -> bool:
        if not mime_data.hasUrls():
            return False
        urls = mime_data.urls()
        file_path = urls[0].toLocalFile()
        if not file_path:
            return False
        if not os.path.isfile(file_path):
            return False
        return True

    def on_drop(self, urls: List[QUrl], mime_data: QMimeData):
        self._config: FileSelectConfig
        if not urls:
            return
        path = urls[0].toLocalFile()
        if self._config.normalize_path:
            path = os.path.normpath(path)
        if self._config.absolutize_path:
            path = os.path.abspath(path)
        self._value_widget.set_paths(os.path.abspath(path))


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

    drag_n_drop: bool = True
    """是否启用文件拖放功能"""

    normalize_path: bool = False
    """是否将路径标准化。若设置为True，则在获取路径时，将使用os.path.normpath()函数进行标准化"""

    absolutize_path: bool = False
    """是否将路径绝对化。若设置为True，则在获取路径时，将使用os.path.abspath()函数进行绝对化"""

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

    def _norm_path(self, path: str) -> str:
        self._config: MultiFileSelectConfig
        if self._config.normalize_path:
            return os.path.normpath(path)
        if self._config.absolutize_path:
            return os.path.abspath(path)
        return path

    def on_drag(self, mime_data: QMimeData) -> bool:
        if not mime_data.hasUrls():
            return False
        if not mime_data.hasUrls():
            return False
        return True

    def on_drop(self, urls: List[QUrl], mime_data: QMimeData):
        self._config: MultiFileSelectConfig
        if not urls:
            return
        paths = [
            self._norm_path(f)
            for f in (url.toLocalFile() for url in urls)
            if os.path.isfile(f)
        ]
        self.set_value(paths)
