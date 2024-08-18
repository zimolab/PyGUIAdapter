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
LEFT_AREA_RATIO = 0.4
RIGHT_AREA_RATIO = 1.0 - LEFT_AREA_RATIO


@dataclasses.dataclass
class FnSelectWindowConfig(BaseWindowConfig):
    title: str = "Select Function"
    select_button_text: str = "Select"
    icon_mode: bool = False
    fn_icon_size: Tuple[int, int] | QSize | None = None
    default_fn_group_name: str = "Main Function"
    default_fn_group_icon: utils.IconType = None
    fn_group_icons: Dict[str, utils.IconType] = dataclasses.field(default_factory=dict)
    document_browser_config: DocumentBrowserConfig | None = dataclasses.field(
        default_factory=DocumentBrowserConfig
    )
    always_show_select_window: bool = True


class FnSelectWindow(BaseWindow):
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
        super().__init__(parent, config)

    def _update_ui(self):
        super()._update_ui()
        self.setObjectName("FnSelectWindow")
        # Central widget
        self._central_widget: QWidget = QWidget(self)
        self._central_widget.setObjectName("central_widget")
        self.setCentralWidget(self._central_widget)

        # main layout
        self._vlayout_main = QVBoxLayout(self._central_widget)
        self._vlayout_main.setObjectName("vlayout_central")

        # Splitter
        self._spliter = QSplitter(self._central_widget)
        self._spliter.setObjectName("spliter")
        self._spliter.setOrientation(Qt.Horizontal)
        self._vlayout_main.addWidget(self._spliter)

        # left area
        # toolbox
        self._toolbox_fn_groups: QToolBox = QToolBox(self._spliter)
        self._toolbox_fn_groups.setObjectName("toolbox_fn_groups")
        # noinspection PyUnresolvedReferences
        self._toolbox_fn_groups.currentChanged.connect(self._on_current_group_change)
        self._spliter.addWidget(self._toolbox_fn_groups)

        # right area
        # right layout
        widget_right = QWidget(self._spliter)
        self._vlayout_right = QVBoxLayout(widget_right)
        self._vlayout_right.setObjectName("vlayout_right")
        self._vlayout_right.setContentsMargins(0, 0, 0, 0)
        # fn document display widget
        self._textbrowser_fn_document: QTextBrowser = QTextBrowser(widget_right)
        self._textbrowser_fn_document.setObjectName("textbrowser_fn_document")
        document_browser_config = (
            self._config.document_browser_config or DocumentBrowserConfig()
        )
        document_browser_config.apply_to(self._textbrowser_fn_document)
        self._vlayout_right.addWidget(self._textbrowser_fn_document)

        # select button
        self._button_select = QPushButton(widget_right)
        self._button_select.setObjectName("button_select")
        self._button_select.setText(self._config.select_button_text)
        self._vlayout_right.addWidget(self._button_select)

        left_area_width = self.width() * LEFT_AREA_RATIO
        right_area_width = self.width() * RIGHT_AREA_RATIO

        self._spliter.setSizes([left_area_width, right_area_width])

        # noinspection PyUnresolvedReferences
        self._button_select.clicked.connect(self._on_button_select_click)

    def add_bundle(self, bundle: FnBundle):
        fn = bundle.fn_info
        page = self._get_group_page(self._group_name(fn.group))
        page.add_bundle(bundle)

    def get_bundles(self, group_name: str | None) -> Tuple[FnBundle, ...]:
        group_name = self._group_name(group_name)
        group_page = self._group_pages.get(group_name, None)
        return group_page.bundles() if group_page is not None else ()

    def get_all_bundles(self) -> List[FnBundle]:
        bundles = []
        for page in self._group_pages.values():
            bs = page.bundles()
            if bs:
                bundles.extend(bs)
        return bundles

    def get_group_names(self) -> List[str]:
        return list(self._group_pages.keys())

    def remove_group(self, group_name: str | None):
        group_name = self._group_name(group_name)
        group_page = self._group_pages.get(group_name, None)
        if group_page is None:
            raise ValueError(f"function group not found: {group_name}")
        group_page.clear_bundles()
        group_page_index = self._toolbox_fn_groups.indexOf(group_page)
        if group_page_index < 0:
            return
        self._toolbox_fn_groups.removeItem(group_page_index)
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
        self._toolbox_fn_groups.setCurrentIndex(0)
        self.show()

    def _start_exec_window(self, bundle: FnBundle):
        assert isinstance(bundle, FnBundle)
        exec_window = FnExecuteWindow(self, bundle)
        exec_window.setWindowModality(Qt.ApplicationModal)
        exec_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        exec_window.show()

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
        current_page = self._toolbox_fn_groups.widget(index)
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
            self._toolbox_fn_groups.setCurrentWidget(page)
            return page
        # if no existing page, create a new one
        icon_size = self._config.fn_icon_size or DEFAULT_FN_ICON_SIZE
        page = FnGroupPage(self._toolbox_fn_groups, self._config.icon_mode, icon_size)
        # noinspection PyUnresolvedReferences
        page.current_bundle_changed.connect(self._on_current_bundle_change)
        # noinspection PyUnresolvedReferences
        page.item_double_clicked.connect(self._on_item_double_click)
        group_icon = self._group_icon(group_name)
        self._toolbox_fn_groups.addItem(page, group_icon, group_name)
        self._toolbox_fn_groups.setCurrentWidget(page)
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
            self._textbrowser_fn_document, document, document_format
        )

    def _current_bundle(self) -> FnBundle | None:
        current_page = self._toolbox_fn_groups.currentWidget()
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
