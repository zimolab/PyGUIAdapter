"""
@Time    : 2024.10.20
@File    : document_browser.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 文档浏览器类的实现
"""

import dataclasses
import re
from typing import Optional
from urllib.parse import unquote

from qtpy.QtCore import QUrl, Signal
from qtpy.QtWidgets import QWidget

from ..constants.color import COLOR_PAGE_BACKGROUND, COLOR_PRIMARY_TEXT
from ..textbrowser import TextBrowserConfig, TextBrowser, LineWrapMode


@dataclasses.dataclass
class DocumentBrowserConfig(TextBrowserConfig):
    """文档浏览器配置类。"""

    text_color: str = COLOR_PRIMARY_TEXT
    background_color: str = COLOR_PAGE_BACKGROUND
    line_wrap_mode: LineWrapMode = LineWrapMode.WidgetWidth

    parameter_anchor: bool = True
    """是否启用参数锚点。当启用时，用户点击文档中的参数锚点，会自动跳转到对应的参数控件处。"""

    parameter_anchor_pattern: str = r"^#\s*param\s*=\s*([\w]+)\s*$"
    """参数锚点的格式。默认格式为：#param=参数名。"""

    group_anchor: bool = True
    """是否启用参数分组锚点。当启用时，用户点击文档中的参数分组锚点，会自动展开对应的参数分组。"""

    group_anchor_pattern: str = r"^#\s*group\s*=\s*([\w\s]*)\s*$"
    """参数分组锚点的格式。默认格式为：#group=分组名。"""


class DocumentBrowser(TextBrowser):
    """文档浏览器类。"""

    sig_parameter_anchor_clicked = Signal(str)
    sig_group_anchor_clicked = Signal(str)

    def __init__(
        self, parent: Optional[QWidget], config: Optional[DocumentBrowserConfig]
    ):
        config = config or DocumentBrowserConfig()
        super().__init__(parent, config)

        if config.parameter_anchor:
            self.anchorClicked.connect(self._anchor_clicked)

    def _anchor_clicked(self, anchor: QUrl):
        self._config: DocumentBrowserConfig
        if not self._config.parameter_anchor and not self._config.group_anchor:
            return
        anchor_str = unquote(anchor.toString()).strip()
        del anchor
        if self._process_parameter_anchor(anchor_str):
            return
        self._process_group_anchor(anchor_str)

    def _process_parameter_anchor(self, anchor_str: str) -> bool:
        self._config: DocumentBrowserConfig
        param_pattern = self._config.parameter_anchor_pattern
        if not param_pattern:
            return False
        match = re.match(param_pattern, anchor_str)
        if not match:
            return False
        param_name = match.group(1).strip()
        self.sig_parameter_anchor_clicked.emit(param_name)
        return True

    def _process_group_anchor(self, anchor_str: str) -> bool:
        self._config: DocumentBrowserConfig
        group_pattern = self._config.group_anchor_pattern
        if not group_pattern:
            return False
        match = re.match(group_pattern, anchor_str)
        if not match:
            return False
        group_name = match.group(1)
        if group_name.strip() == "":
            group_name = ""
        self.sig_group_anchor_clicked.emit(group_name)
        return True
