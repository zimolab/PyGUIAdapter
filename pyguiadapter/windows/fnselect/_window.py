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
from ...menu import MenuConfig
from ...toolbar import ToolBarConfig
from ...bundle import FnBundle
from ...window import BaseWindow, BaseWindowConfig, BaseWindowStateListener

DEFAULT_FN_ICON_SIZE = (48, 48)
WARNING_MSG_NO_FN_SELECTED = "No Selected Function!"


@dataclasses.dataclass(frozen=True)
class FnSelectWindowConfig(BaseWindowConfig):
    title: str = "Select Function"
    size: Union[Tuple[int, int], QSize] = (800, 600)
    select_button_text: str = "Select"
    icon_mode: bool = False
    icon_size: Union[Tuple[int, int], int, QSize, None] = DEFAULT_FN_ICON_SIZE
    default_fn_group_name: str = "Main Functions"
    default_fn_group_icon: IconType = None
    fn_group_icons: Dict[str, IconType] = dataclasses.field(default_factory=dict)
    document_browser_config: Optional[DocumentBrowserConfig] = None
    document_browser_width: int = 490


class FnSelectWindow(BaseWindow):
    # noinspection SpellCheckingInspection
    def __init__(
        self,
        parent: Optional[QWidget],
        bundles: List[FnBundle],
        config: Optional[FnSelectWindowConfig],
        listener: Optional[BaseWindowStateListener] = None,
        toolbar: Optional[ToolBarConfig] = None,
        menus: Optional[List[Union[MenuConfig, Separator]]] = None,
    ):
        self._initial_bundles = bundles.copy()
        self._group_pages: Dict[str, FnGroupPage] = {}
        self._current_exec_window: Optional[FnSelectWindow] = None
        self._function_group_toolbox: Optional[QToolBox] = None
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

        self._function_group_toolbox: QToolBox = QToolBox(splitter)
        # noinspection PyUnresolvedReferences
        self._function_group_toolbox.currentChanged.connect(
            self._on_current_group_change
        )
        splitter.addWidget(self._function_group_toolbox)

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

    def set_select_button_text(self, text: str):
        self._select_button.setText(text)

    def set_document_browser_width(self, width: int):
        if width <= 0:
            raise ValueError(f"invalid width: {width}")
        left_width = self.width() - width
        self._splitter.setSizes([left_width, width])

    def add_bundle(self, bundle: FnBundle):
        fn = bundle.fn_info
        page = self._get_group_page(self._group_name(fn.group))
        page.add_bundle(bundle)

    def get_bundles_of(self, group_name: Optional[str]) -> Tuple[FnBundle, ...]:
        group_name = self._group_name(group_name)
        group_page = self._group_pages.get(group_name, None)
        return group_page.bundles() if group_page is not None else ()

    def get_group_names(self) -> List[str]:
        return list(self._group_pages.keys())

    def get_all_bundles(self) -> List[FnBundle]:
        bundles = []
        for page in self._group_pages.values():
            bs = page.bundles()
            if bs:
                bundles.extend(bs)
        return bundles

    def remove_group(self, group_name: Optional[str]):
        group_name = self._group_name(group_name)
        group_page = self._group_pages.get(group_name, None)
        if group_page is None:
            raise ValueError(f"function group not found: {group_name}")
        group_page.clear_bundles()
        group_page_index = self._function_group_toolbox.indexOf(group_page)
        if group_page_index < 0:
            return
        self._function_group_toolbox.removeItem(group_page_index)
        group_page.deleteLater()

    def remove_bundle(self, bundle: FnBundle):
        group_name = self._group_name(bundle.fn_info.group)
        group_page = self._group_pages.get(group_name, None)
        if group_page is not None:
            group_page.remove_bundle(bundle)

    def start(self):
        for bundle in self._initial_bundles:
            self.add_bundle(bundle)
        del self._initial_bundles
        self._function_group_toolbox.setCurrentIndex(0)
        self.show()

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
        current_page = self._function_group_toolbox.widget(index)
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
            self._function_group_toolbox.setCurrentWidget(page)
            return page
        # if no existing page, create a new one
        icon_size = self._config.icon_size or DEFAULT_FN_ICON_SIZE
        page = FnGroupPage(
            self._function_group_toolbox, self._config.icon_mode, icon_size
        )
        # noinspection PyUnresolvedReferences
        page.sig_current_bundle_changed.connect(self._on_current_bundle_change)
        # noinspection PyUnresolvedReferences
        page.sig_item_double_clicked.connect(self._on_item_double_click)
        group_icon = self._group_icon(group_name)
        self._function_group_toolbox.addItem(page, group_icon, group_name)
        self._function_group_toolbox.setCurrentWidget(page)
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
        current_page = self._function_group_toolbox.currentWidget()
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
