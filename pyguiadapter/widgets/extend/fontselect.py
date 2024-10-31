import dataclasses
from typing import Optional, Any, Union, Type

from qtpy.QtGui import QFontDatabase
from qtpy.QtWidgets import QFontComboBox, QWidget

from .. import CommonParameterWidget
from ..common import CommonParameterWidgetConfig

FontFilter = QFontComboBox.FontFilter
"""字体过滤器"""

WritingSystem = QFontDatabase.WritingSystem
"""书写系统"""


@dataclasses.dataclass(frozen=True)
class FontSelectConfig(CommonParameterWidgetConfig):
    default_value: Optional[str] = ""
    """默认值"""

    font_filters: Union[FontFilter, int, None] = FontFilter.AllFonts
    """字体过滤器"""

    writing_system: Optional[WritingSystem] = None
    """书写系统"""

    @classmethod
    def target_widget_class(cls) -> Type["FontSelect"]:
        return FontSelect


class FontSelect(CommonParameterWidget):
    """字体选择器"""

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
        self._font_combo: Optional[QFontComboBox] = None

    @property
    def value_widget(self) -> QWidget:
        self._config: FontSelectConfig

        if self._font_combo is None:
            self._font_combo = QFontComboBox(self)

            if self._config.font_filters is not None:
                self._font_combo.setFontFilters(self._config.font_filters)

            if self._config.writing_system is not None:
                self._font_combo.setWritingSystem(self._config.writing_system)

        return self._font_combo

    def set_value_to_widget(self, value: Any) -> None:
        pass

    def get_value_from_widget(self) -> Any:
        pass
