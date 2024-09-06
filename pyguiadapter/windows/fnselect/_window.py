from __future__ import annotations

import dataclasses
from typing import Tuple, Dict, Literal, List

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QSplitter,
    QToolBox,
    QVBoxLayout,
    QTextBrowser,
    QPushButton,
    QWidget,
)

from ._group import FnGroupPage
from .._docbrowser import DocumentBrowserConfig
from ..fnexec import FnExecuteWindow
from ... import utils
from ...bundle import FnBundle
from ...window import BaseWindow, BaseWindowConfig

DEFAULT_FN_ICON_SIZE = (48, 48)
WARNING_MSG_NO_FN_SELECTED = "No Selected Function!"


@dataclasses.dataclass
class FnSelectWindowConfig(BaseWindowConfig):
    title: str = "Select Function"
    select_button_text: str = "Select"
    icon_mode: bool = False
    icon_size: Tuple[int, int] | QSize | None = DEFAULT_FN_ICON_SIZE
    default_fn_group_name: str = "Main Function"
    default_fn_group_icon: utils.IconType = None
    fn_group_icons: Dict[str, utils.IconType] = dataclasses.field(default_factory=dict)
    document_browser: DocumentBrowserConfig | None = dataclasses.field(
        default_factory=DocumentBrowserConfig
    )
    document_browser_ratio: float = 0.35


class FnSelectWindow(BaseWindow):
    # noinspection SpellCheckingInspection
    def __init__(
        self,
        parent: QWidget | None,
        bundles: List[FnBundle],
        config: FnSelectWindowConfig | None,
    ):
        self._config: FnSelectWindowConfig = config or FnSelectWindowConfig()
        self._initial_bundles = bundles.copy()
        self._group_pages: Dict[str, FnGroupPage] = {}
        self._current_exec_window: FnSelectWindow | None = None

        self._function_group_toolbox: QToolBox | None = None
        self._document_textbrowser: QTextBrowser | None = None
        self._select_button: QPushButton | None = None

        super().__init__(parent, config)

    def _setup_ui(self):
        super()._setup_ui()

        # central widget
        _central_widget: QWidget = QWidget(self)
        # main layout
        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout(_central_widget)
        self.setCentralWidget(_central_widget)

        # Splitter
        # noinspection PyArgumentList
        _splitter = QSplitter(_central_widget)
        _splitter.setOrientation(Qt.Horizontal)
        self._layout_main.addWidget(_splitter)

        # left area
        # toolbox
        self._function_group_toolbox: QToolBox = QToolBox(_splitter)
        # noinspection PyUnresolvedReferences
        self._function_group_toolbox.currentChanged.connect(
            self._on_current_group_change
        )
        _splitter.addWidget(self._function_group_toolbox)

        # right area
        # right layout
        right_area = QWidget(_splitter)
        # noinspection PyArgumentList
        _layout_right_area = QVBoxLayout(right_area)
        _layout_right_area.setContentsMargins(0, 0, 0, 0)
        # fn document browser
        # noinspection SpellCheckingInspection
        self._document_textbrowser: QTextBrowser = QTextBrowser(right_area)
        document_browser_config = (
            self._config.document_browser or DocumentBrowserConfig()
        )
        document_browser_config.apply_to(self._document_textbrowser)
        _layout_right_area.addWidget(self._document_textbrowser)
        # select button
        self._select_button = QPushButton(right_area)
        self._select_button.setText(self._config.select_button_text)
        _layout_right_area.addWidget(self._select_button)

        left_area_ratio = self._config.document_browser_ratio
        right_area_ratio = 1.0 - left_area_ratio
        left_area_width = int(self.width() * left_area_ratio)
        right_area_width = int(self.width() * right_area_ratio)
        _splitter.setSizes([left_area_width, right_area_width])

        # noinspection PyUnresolvedReferences
        self._select_button.clicked.connect(self._on_button_select_click)

    def add_bundle(self, bundle: FnBundle):
        fn = bundle.fn_info
        page = self._get_group_page(self._group_name(fn.group))
        page.add_bundle(bundle)

    def get_bundles_of(self, group_name: str | None) -> Tuple[FnBundle, ...]:
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

    def remove_group(self, group_name: str | None):
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
            utils.show_warning_message(self, WARNING_MSG_NO_FN_SELECTED)
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

    def _get_group_page(self, group_name: str | None) -> FnGroupPage:
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
        page.current_bundle_changed.connect(self._on_current_bundle_change)
        # noinspection PyUnresolvedReferences
        page.item_double_clicked.connect(self._on_item_double_click)
        group_icon = self._group_icon(group_name)
        self._function_group_toolbox.addItem(page, group_icon, group_name)
        self._function_group_toolbox.setCurrentWidget(page)
        self._group_pages[group_name] = page
        return page

    def _group_icon(self, group_name: str | None):
        if group_name is None or group_name == self._config.default_fn_group_name:
            return utils.get_icon(self._config.default_fn_group_icon) or QIcon()
        icon_src = self._config.fn_group_icons.get(group_name, None)
        if icon_src is None:
            return QIcon()
        return utils.get_icon(icon_src) or QIcon()

    def _update_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        utils.set_textbrowser_content(
            self._document_textbrowser, document, document_format
        )

    def _current_bundle(self) -> FnBundle | None:
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

    def _group_name(self, group_name: str | None):
        if group_name is None:
            return self._config.default_fn_group_name
        return group_name
