import dataclasses
from typing import Optional, Any, Union, Type

from qtpy.QtGui import QFontDatabase
from qtpy.QtWidgets import QFontComboBox, QWidget

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check

FontFilter = QFontComboBox.FontFilter
"""字体过滤器"""

WritingSystem = QFontDatabase.WritingSystem
"""书写系统"""


class _DefaultFont(object):
    """默认字体"""

    __slots__ = ()


class _FirstFont(object):
    """第一个可用字体"""

    __slots__ = ()


@dataclasses.dataclass(frozen=True)
class FontSelectConfig(CommonParameterWidgetConfig):
    """FontSelect的配置类"""

    default_value: Union[str, Type[_DefaultFont], Type[_FirstFont], None] = _DefaultFont
    """默认值，可以为字体名称（字符串），或者以下特殊值：`_DefaultFont`(默认字体)，`_FirstFont`(第一个可用字体)"""

    font_filters: Union[FontFilter, int, None] = None
    """字体过滤器，可以为单个`FontFilter`枚举值，多种多个枚举值的联合，比如：`FontFilter.ScalableFonts | FontFilter.ProportionalFonts`"""

    writing_system: Optional[WritingSystem] = None
    """书写系统"""

    @classmethod
    def target_widget_class(cls) -> Type["FontSelect"]:
        return FontSelect


class FontSelect(CommonParameterWidget):
    """字体选择控件"""

    ConfigClass = FontSelectConfig

    AllFonts = FontFilter.AllFonts
    """字体过滤器：所有字体"""

    ScalableFonts = FontFilter.ScalableFonts
    """字体过滤器：可缩放字体"""

    NonScalableFonts = FontFilter.NonScalableFonts
    """字体过滤器：不可缩放字体"""

    MonospacedFonts = FontFilter.MonospacedFonts
    """字体过滤器：等宽字体"""

    ProportionalFonts = FontFilter.ProportionalFonts
    """字体过滤器：比例字体"""

    WritingSystem = QFontDatabase.WritingSystem
    """书写系统"""

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: FontSelectConfig
    ):
        super().__init__(parent, parameter_name, config)
        self._value_widget: Optional[QFontComboBox] = None

    @property
    def value_widget(self) -> QWidget:
        self._config: FontSelectConfig

        if self._value_widget is None:
            self._value_widget = QFontComboBox(self)

            if self._config.font_filters is not None:
                self._value_widget.setFontFilters(self._config.font_filters)

            if self._config.writing_system is not None:
                self._value_widget.setWritingSystem(self._config.writing_system)

        return self._value_widget

    def check_value_type(self, value: Any) -> bool:
        if value is _DefaultFont or value is _FirstFont:
            return True
        return type_check(value, (str,), allow_none=True)

    def set_value_to_widget(self, value: str) -> None:
        if value is _DefaultFont:
            return
        if value is _FirstFont:
            self._value_widget.setCurrentIndex(0)
            return
        self._value_widget.setCurrentText(value)

    def get_value_from_widget(self) -> str:
        return self._value_widget.currentText()
