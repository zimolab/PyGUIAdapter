import dataclasses
from typing import Type, Any, Optional

from qtpy.QtWidgets import QWidget

from ._path import PathSelectWidget
from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class DirSelectConfig(CommonParameterWidgetConfig):
    """DirSelect的配置类。"""

    default_value: Optional[str] = ""
    """默认值"""

    placeholder: str = ""
    """占位符文字"""

    start_dir: str = ""
    """起始目录"""

    dialog_title: str = ""
    """文件对话框标题"""

    select_button_text: str = "..."
    """选择按钮文字"""

    clear_button: bool = False
    """是否显示清除按钮"""

    @classmethod
    def target_widget_class(cls) -> Type["DirSelect"]:
        return DirSelect


class DirSelect(CommonParameterWidget):
    ConfigClass = DirSelectConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: DirSelectConfig
    ):
        self._value_widget: Optional[PathSelectWidget] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> PathSelectWidget:
        self._config: DirSelectConfig
        if self._value_widget is None:
            self._value_widget = PathSelectWidget(
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

    def check_value_type(self, value: Any):
        type_check(value, (str,), allow_none=True)

    def set_value_to_widget(self, value: Any):
        value = value or ""
        self._value_widget.set_path(str(value))

    def get_value_from_widget(self) -> str:
        return self._value_widget.get_path()
