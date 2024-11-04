import dataclasses
import os
from typing import Type, Any, List, Tuple, Set, Optional, Union, Sequence, Callable

from qtpy.QtCore import QMimeData, QUrl
from qtpy.QtWidgets import QWidget

from ._dnd import default_dnd_filter
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

    drag_n_drop_filter: Optional[Callable[[str, str], bool]] = default_dnd_filter
    """文件拖放功能的过滤函数。该函数应接收两个参数：文件过滤器（即本类的`filters`属性）和拖放的文件路径。
    若返回True，则表示该文件可以被拖放；否则，则表示该文件不能被拖放。该属性也可以设置为None，表示不对拖放文件进行过滤。
    默认情况下，使用`default_dnd_filter`函数作为过滤函数，该函数会将待拖放的文件的文件名与文件过滤器进行匹配，若命中任意文件过滤器，则返回True，
    否则返回False。比如，若文件过滤器为'Text files (*.txt);;Python files (*.py)', 则文件'hello.txt'可以被拖放，因为其命中了'Text files (*.txt)';
    文件'hello.py'也可以被拖放，因为其命中了'Python files (*.py)'；文件'hello.png'则不能被拖放，因为其没有命中任何文件过滤器。"""

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
                normalize_path=self._config.normalize_path,
                absolutize_path=self._config.absolutize_path,
            )
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (str,), allow_none=True)

    def set_value_to_widget(self, value: Any):
        self._value_widget.set_path(str(value or ""))

    def get_value_from_widget(self) -> str:
        return self._value_widget.get_path()

    def on_drag(self, mime_data: QMimeData) -> bool:
        self._config: FileSelectConfig
        if not mime_data.hasUrls():
            return False
        urls = mime_data.urls()
        file_path = urls[0].toLocalFile()
        if not file_path:
            return False
        if not os.path.isfile(file_path):
            return False
        if self._config.drag_n_drop_filter:
            return self._config.drag_n_drop_filter(self._config.filters, file_path)
        return True

    def on_drop(self, urls: List[QUrl], mime_data: QMimeData):
        self._config: FileSelectConfig
        if not urls:
            return
        path = urls[0].toLocalFile()
        self._value_widget.set_path(path)


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

    clear_button: bool = True
    """是否显示清除按钮"""

    drag_n_drop: bool = True
    """是否启用文件拖放功能"""

    drag_n_drop_filter: Optional[Callable[[str, str], bool]] = default_dnd_filter
    """文件拖放功能的过滤函数。该函数应接收两个参数：文件过滤器（即本类的`filters`属性）和拖放的文件路径。
    若返回True，则表示该文件可以被拖放；否则，则表示该文件不能被拖放。该属性也可以设置为None，表示不对拖放文件进行过滤。
    默认情况下，使用`default_dnd_filter`函数作为过滤函数，该函数会将待拖放的文件的文件名与文件过滤器进行匹配，若命中任意文件过滤器，则返回True，
    否则返回False。比如，若文件过滤器为'Text files (*.txt);;Python files (*.py)', 则文件'hello.txt'可以被拖放，因为其命中了'Text files (*.txt)';
    文件'hello.py'也可以被拖放，因为其命中了'Python files (*.py)'；文件'hello.png'则不能被拖放，因为其没有命中任何文件过滤器。"""

    normalize_path: bool = False
    """是否将路径标准化。若设置为True，则在设置控件值或者从控件获取值时，使用os.path.normpath()函数进行标准化"""

    absolutize_path: bool = False
    """是否将路径绝对化。若设置为True，则在设置控件值或者从控件获取值时，将使用os.path.abspath()函数进行绝对化"""

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
                normalize_path=self._config.normalize_path,
                absolutize_path=self._config.absolutize_path,
            )
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (str, list, tuple, set), allow_none=True)

    def set_value_to_widget(
        self, value: Union[str, List[str], Tuple[str, ...], Set[str]]
    ):
        self._value_widget.set_paths(value or [])

    def get_value_from_widget(self) -> List[str]:
        return self._value_widget.get_paths()

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
            f
            for f in (url.toLocalFile() for url in urls)
            if os.path.isfile(f)
            and (
                self._config.drag_n_drop_filter is None
                or self._config.drag_n_drop_filter(self._config.filters, f) is True
            )
        ]
        if not paths:
            return
        self._value_widget.set_paths(paths)
