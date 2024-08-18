from __future__ import annotations

import dataclasses
from typing import Tuple, Literal, Dict, Union, Type, Any, List

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from ._docarea import FnDocumentArea
from ._logarea import (
    ProgressBarConfig,
    LogOutputConfig,
    FnExecuteLogOutputArea,
)
from ._paramarea import FnParameterArea
from .._docbrowser import DocumentBrowserConfig
from ... import utils
from ...adapter import context
from ...bundle import FnBundle
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    is_parameter_widget_class,
)
from ...window import BaseWindow, BaseWindowConfig

DEFAULT_WINDOW_SIZE = (1024, 768)

ParameterWidgetType = Union[
    Tuple[Type[BaseParameterWidget], Union[BaseParameterWidgetConfig, dict]],
    BaseParameterWidgetConfig,
]


@dataclasses.dataclass
class FnExecuteWindowConfig(BaseWindowConfig):
    title: str = ""
    size: Tuple[int, int] | QSize = DEFAULT_WINDOW_SIZE
    log_output_dock_title: str = "Log Output"
    log_output_dock_ratio: float = 0.3
    document_dock_title: str = "Document"
    document_dock_ratio: float = 0.65
    progressbar: ProgressBarConfig | None = None
    log_output: LogOutputConfig = dataclasses.field(default_factory=LogOutputConfig)
    document_browser: DocumentBrowserConfig | None = dataclasses.field(
        default_factory=DocumentBrowserConfig
    )
    default_parameter_group_name: str = "Main Parameters"
    default_parameter_group_icon: utils.IconType = None
    parameter_group_icons: Dict[str, utils.IconType] = dataclasses.field(
        default_factory=dict
    )
    execute_button_text: str = "Execute"
    cancel_button_text: str = "Cancel"
    clear_checkbox_text: str = "Clear log output"


class FnExecuteWindow(BaseWindow):
    def __init__(self, parent: QWidget | None, bundle: FnBundle):

        self._bundle = bundle

        super().__init__(parent, bundle.window_config)
        context.window_created(self)
        self.add_paramters(self._bundle.widget_configs)

    def update_progressbar_config(self, config: ProgressBarConfig | None):
        self._area_log_output.update_progressbar_config(config)

    def show_progressbar(self):
        self._area_log_output.show_progressbar()

    def hide_progressbar(self):
        self._area_log_output.hide_progressbar()

    def update_progress(self, current_value: int, message: str | None = None):
        self._area_log_output.update_progress(current_value, message)

    def append_log_output(self, log_text: str, html: bool = False):
        self._area_log_output.append_log_output(log_text, html)

    def clear_log_output(self):
        self._area_log_output.clear_log_output()

    def update_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ):
        self._area_document.set_fn_document(document, document_format)

    def add_parameter(self, parameter_name: str, config: ParameterWidgetType):
        if isinstance(config, tuple):
            assert len(config) == 2
            assert is_parameter_widget_class(config[0])
            assert isinstance(config[1], (BaseParameterWidgetConfig, dict))
            widget_class, widget_config = config
        elif isinstance(config, BaseParameterWidgetConfig):
            widget_class = config.target_widget_class()
            widget_config = config
        else:
            raise TypeError(f"Invalid type for widget_config: {type(config)}")

        if isinstance(widget_config, dict):
            widget_config = widget_class.ConfigClass.new(**widget_config)

        groupbox = self._area_parameters.parameter_group_box
        groupbox.add_paramter(parameter_name, widget_class, widget_config)

    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        groupbox = self._area_parameters.parameter_group_box
        groupbox.remove_parameter(parameter_name, safe_remove=safe_remove)

    def clear_parameters(self):
        groupbox = self._area_parameters.parameter_group_box
        groupbox.clear_parameters()
        groupbox.add_default_group()

    def get_parameter_value(self, parameter_name: str) -> Any:
        groupbox = self._area_parameters.parameter_group_box
        return groupbox.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        groupbox = self._area_parameters.parameter_group_box
        return groupbox.get_parameter_values()

    def set_parameter_value(
        self, parameter_name: str, value: Any, ignore_unknown_parameter: bool = True
    ):
        groupbox = self._area_parameters.parameter_group_box
        groupbox.set_parameter_value(
            parameter_name, value, ignore_unknown_parameter=ignore_unknown_parameter
        )

    def set_parameter_values(self, values: Dict[str, Any]) -> List[str]:
        groupbox = self._area_parameters.parameter_group_box
        return groupbox.set_parameter_values(values)

    def add_paramters(self, configs: Dict[str, ParameterWidgetType]):
        for parameter_name, config in configs.items():
            self.add_parameter(parameter_name, config)

    def _update_ui(self):
        super()._update_ui()

        fn_info = self._bundle.fn_info
        window_config = self._bundle.window_config

        # set title and icon
        title = self._config.title or fn_info.display_name
        icon = self._config.icon or fn_info.icon
        icon = utils.get_icon(icon) or QIcon()
        self.setWindowTitle(title)
        self.setWindowIcon(icon)

        # central widget and layout
        self._center_widget = QWidget(self)
        self._vlayout_main = QVBoxLayout(self._center_widget)
        self._vlayout_main.setObjectName("vlayout_main")
        self.setCentralWidget(self._center_widget)

        # create the area for parameter widgets
        self._area_parameters = FnParameterArea(self._center_widget, window_config)
        self._vlayout_main.addWidget(self._area_parameters)

        # create the dock widget and document area
        self._dockwidget_document = QDockWidget(self)
        self._dockwidget_document.setObjectName("dockwidget_document")
        self._dockwidget_document.setWindowTitle(window_config.document_dock_title)
        self._area_document = FnDocumentArea(
            self._dockwidget_document, window_config.document_browser
        )
        self._dockwidget_document.setWidget(self._area_document)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockwidget_document)
        # display the document content
        self.update_document(fn_info.document, fn_info.document_format)

        # create the dock widget and log output area
        self._dockwidget_log_output = QDockWidget(self)
        self._dockwidget_log_output.setObjectName("dockwidget_log_output")
        self._dockwidget_log_output.setWindowTitle(window_config.log_output_dock_title)
        self._area_log_output = FnExecuteLogOutputArea(
            self._dockwidget_log_output,
            progressbar_config=window_config.progressbar,
            log_output_config=window_config.log_output,
        )
        self._dockwidget_log_output.setWidget(self._area_log_output)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._dockwidget_log_output)
        if window_config.progressbar is None:
            self.hide_progressbar()
        else:
            self.show_progressbar()

        # resize the docks
        current_width = self.width()
        current_height = self.height()
        log_output_dock_ratio = window_config.log_output_dock_ratio
        log_output_dock_ratio = min(max(log_output_dock_ratio, 0.1), 1.0)
        dock_height = int(current_height * log_output_dock_ratio)
        document_dock_ratio = min(max(window_config.document_dock_ratio, 0.1), 1.0)
        dock_width = int(current_width * document_dock_ratio)
        self.resizeDocks([self._dockwidget_log_output], [dock_height], Qt.Vertical)
        self.resizeDocks(
            [self._dockwidget_document],
            [dock_width],
            Qt.Horizontal,
        )

    def _on_destroy(self):
        super()._on_destroy()
        context.window_closed(self)
