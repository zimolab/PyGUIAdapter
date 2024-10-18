import dataclasses
from typing import Tuple, Dict, Literal, List, Union, Optional

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QSplitter,
    QToolBox,
    QVBoxLayout,
    QPushButton,
    QWidget,
)

from ._group import FnGroupPage
from ..document_browser import DocumentBrowserConfig, DocumentBrowser
from ..fnexec import FnExecuteWindow
from ...utils import IconType, get_icon, set_textbrowser_content, messagebox
from ...action import Separator
from ...menu import Menu
from ...toolbar import ToolBar
from ...bundle import FnBundle
from ...window import BaseWindow, BaseWindowConfig, BaseWindowEventListener

DEFAULT_FN_ICON_SIZE = (48, 48)
WARNING_MSG_NO_FN_SELECTED = "No Selected Function!"


@dataclasses.dataclass(frozen=True)
class FnSelectWindowConfig(BaseWindowConfig):
    title: str = "Select Function"
    """窗口标题"""

    size: Union[Tuple[int, int], QSize] = (800, 600)
    """窗口尺寸"""

    select_button_text: str = "Select"
    """选择按钮文字"""

    icon_mode: bool = False
    """函数列表是否启用图标模式"""

    icon_size: Union[Tuple[int, int], int, QSize, None] = DEFAULT_FN_ICON_SIZE
    """函数图标大小"""

    default_fn_group_name: str = "Main Functions"
    """默认函数分组名称"""

    default_fn_group_icon: IconType = None
    """默认函数分组图标"""

    fn_group_icons: Dict[str, IconType] = dataclasses.field(default_factory=dict)
    """其他函数分组图标"""

    document_browser_config: Optional[DocumentBrowserConfig] = None
    """文档浏览器配置"""

    document_browser_width: int = 490
    """文档浏览器宽度"""


class FnSelectWindow(BaseWindow):
    # noinspection SpellCheckingInspection
    def __init__(
        self,
        parent: Optional[QWidget],
        bundles: List[FnBundle],
        config: Optional[FnSelectWindowConfig],
        listener: Optional[BaseWindowEventListener] = None,
        toolbar: Optional[ToolBar] = None,
        menus: Optional[List[Union[Menu, Separator]]] = None,
    ):
        self._initial_bundles = bundles.copy()
        self._group_pages: Dict[str, FnGroupPage] = {}
        self._current_exec_window: Optional[FnSelectWindow] = None
        self._fn_group_toolbox: Optional[QToolBox] = None
        self._document_browser: Optional[DocumentBrowser] = None
        self._select_button: Optional[QPushButton] = None
        self._splitter: Optional[QSplitter] = None

        super().__init__(parent, config, listener, toolbar, menus)

    def _create_ui(self):
        self._config: FnSelectWindowConfig

        central_widget: QWidget = QWidget(self)
        # noinspection PyArgumentList
        layout_main = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # noinspection PyArgumentList
        splitter = QSplitter(central_widget)
        splitter.setOrientation(Qt.Horizontal)
        layout_main.addWidget(splitter)

        self._fn_group_toolbox: QToolBox = QToolBox(splitter)
        # noinspection PyUnresolvedReferences
        self._fn_group_toolbox.currentChanged.connect(self._on_current_group_change)
        splitter.addWidget(self._fn_group_toolbox)

        right_area = QWidget(splitter)
        # noinspection PyArgumentList
        layout_right_area = QVBoxLayout()
        layout_right_area.setContentsMargins(0, 0, 0, 0)

        self._document_browser = DocumentBrowser(
            right_area, self._config.document_browser_config
        )
        layout_right_area.addWidget(self._document_browser)

        self._select_button = QPushButton(right_area)
        layout_right_area.addWidget(self._select_button)
        right_area.setLayout(layout_right_area)

        # noinspection PyUnresolvedReferences
        self._select_button.clicked.connect(self._on_button_select_click)
        self._splitter = splitter

    def apply_configs(self):
        super().apply_configs()
        self._config: FnSelectWindowConfig
        self.set_select_button_text(self._config.select_button_text)
        self.set_document_browser_width(self._config.document_browser_width)

    def set_select_button_text(self, text: str) -> None:
        """
        设置选择按钮文字。

        Args:
            text: 带设置的文字

        Returns:
            无返回值

        """
        self._select_button.setText(text)

    def get_select_button_text(self) -> str:
        """
        获取选择按钮文字。

        Returns:
            返回当前选择按钮上的文字。
        """
        return self._select_button.text()

    def set_document_browser_width(self, width: int) -> None:
        """
        设置文档浏览器宽度。

        Args:
            width: 目标宽度

        Returns:
            无返回值

        """
        if width <= 0:
            raise ValueError(f"invalid width: {width}")
        left_width = self.width() - width
        self._splitter.setSizes([left_width, width])

    def get_group_names(self) -> List[str]:
        """
        获取所有函数分组名称。

        Returns:
            返回函数分组名称列表。
        """
        return list(self._group_pages.keys())

    def remove_group(self, group_name: Optional[str]) -> None:
        """
        移除指定函数分组。

        Args:
            group_name: 待移除的函数分组名称。

        Returns:
            无返回值

        Raises:
            ValueError: 当指定函数分组名称不存在时，将抛出`ValueError`。

        """
        group_name = self._group_name(group_name)
        group_page = self._group_pages.get(group_name, None)
        if group_page is None:
            raise ValueError(f"group not found: {group_name}")
        group_page.clear_bundles()
        group_page_index = self._fn_group_toolbox.indexOf(group_page)
        if group_page_index < 0:
            return
        self._fn_group_toolbox.removeItem(group_page_index)
        group_page.deleteLater()

    def start(self):
        for bundle in self._initial_bundles:
            self._add_bundle(bundle)
        del self._initial_bundles
        self._fn_group_toolbox.setCurrentIndex(0)
        self.show()

    def _add_bundle(self, bundle: FnBundle):
        fn = bundle.fn_info
        page = self._get_group_page(self._group_name(fn.group))
        page.add_bundle(bundle)

    def _get_bundles_of(self, group_name: Optional[str]) -> Tuple[FnBundle, ...]:
        group_name = self._group_name(group_name)
        group_page = self._group_pages.get(group_name, None)
        return group_page.bundles() if group_page is not None else ()

    def _get_all_bundles(self) -> List[FnBundle]:
        bundles = []
        for page in self._group_pages.values():
            bs = page.bundles()
            if bs:
                bundles.extend(bs)
        return bundles

    def _remove_bundle(self, bundle: FnBundle) -> None:
        group_name = self._group_name(bundle.fn_info.group)
        group_page = self._group_pages.get(group_name, None)
        if group_page is not None:
            group_page.remove_bundle(bundle)

    def _start_exec_window(self, bundle: FnBundle):
        assert isinstance(bundle, FnBundle)
        self._current_exec_window = FnExecuteWindow(self, bundle)
        self._current_exec_window.setWindowModality(Qt.ApplicationModal)
        self._current_exec_window.setAttribute(Qt.WA_DeleteOnClose, True)
        # noinspection PyUnresolvedReferences
        self._current_exec_window.destroyed.connect(
            self._on_current_exec_window_destroyed
        )
        self._current_exec_window.show()

    def _on_current_exec_window_destroyed(self):
        self._current_exec_window = None

    def _on_button_select_click(self):
        bundle = self._current_bundle()
        if bundle is None:
            messagebox.show_warning_message(self, WARNING_MSG_NO_FN_SELECTED)
            return
        self._start_exec_window(bundle)

    # noinspection PyUnusedLocal
    def _on_current_bundle_change(self, bundle: FnBundle, page: FnGroupPage):
        doc = ""
        doc_format = "plaintext"
        if bundle is not None:
            doc = bundle.fn_info.document
            doc_format = bundle.fn_info.document_format
        # noinspection PyTypeChecker
        self._update_document(doc, doc_format)

    # noinspection PyUnusedLocal
    def _on_item_double_click(self, bundle: FnBundle, page: FnGroupPage):
        self._start_exec_window(bundle)

    def _on_current_group_change(self, index: int):
        current_page = self._fn_group_toolbox.widget(index)
        if not isinstance(current_page, FnGroupPage):
            return
        bundle = current_page.current_bundle()
        if bundle is None:
            current_page.set_current_index(0)
            return
        self._on_current_bundle_change(bundle, current_page)

    def _get_group_page(self, group_name: Optional[str]) -> FnGroupPage:
        self._config: FnSelectWindowConfig
        group_name = self._group_name(group_name)
        # return existing page
        if group_name in self._group_pages:
            page = self._group_pages[group_name]
            self._fn_group_toolbox.setCurrentWidget(page)
            return page
        # if no existing page, create a new one
        icon_size = self._config.icon_size or DEFAULT_FN_ICON_SIZE
        page = FnGroupPage(self._fn_group_toolbox, self._config.icon_mode, icon_size)
        # noinspection PyUnresolvedReferences
        page.sig_current_bundle_changed.connect(self._on_current_bundle_change)
        # noinspection PyUnresolvedReferences
        page.sig_item_double_clicked.connect(self._on_item_double_click)
        group_icon = self._group_icon(group_name)
        self._fn_group_toolbox.addItem(page, group_icon, group_name)
        self._fn_group_toolbox.setCurrentWidget(page)
        self._group_pages[group_name] = page
        return page

    def _group_icon(self, group_name: Optional[str]):
        self._config: FnSelectWindowConfig
        if group_name is None or group_name == self._config.default_fn_group_name:
            return get_icon(self._config.default_fn_group_icon) or QIcon()
        icon_src = self._config.fn_group_icons.get(group_name, None)
        if icon_src is None:
            return QIcon()
        return get_icon(icon_src) or QIcon()

    def _update_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        set_textbrowser_content(self._document_browser, document, document_format)

    def _current_bundle(self) -> Optional[FnBundle]:
        current_page = self._fn_group_toolbox.currentWidget()
        if not isinstance(current_page, FnGroupPage):
            return None
        return current_page.current_bundle()

    def _on_cleanup(self):
        super()._on_cleanup()
        for group_page in self._group_pages.values():
            group_page.clear_bundles()
            group_page.deleteLater()
        self._group_pages.clear()

    def _group_name(self, group_name: Optional[str]):
        self._config: FnSelectWindowConfig
        if group_name is None:
            return self._config.default_fn_group_name
        return group_name
