from __future__ import annotations

from typing import Dict

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBox,
    QCheckBox,
    QPushButton,
    QScrollArea,
)

from . import _window
from ... import utils


class FnParameterGroupPage(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._parameters = {}

        self._vlayout_main = QVBoxLayout(self)
        self._vlayout_main.setContentsMargins(0, 0, 0, 0)

        self._scrollarea_param_container = QScrollArea(self)
        self._widget_scrollarea_content = QWidget(self._scrollarea_param_container)
        self._widget_scrollarea_content.setObjectName("widget_scrollarea_content")
        self._vlayout_scrollarea_content = QVBoxLayout(self._widget_scrollarea_content)
        self._scrollarea_param_container.setWidget(self._widget_scrollarea_content)

        self._vlayout_main.addWidget(self._scrollarea_param_container)

    def add_parameter(self, parameter_name: str, parameter_group: str | None):
        pass


class FnParameterGroupBox(QToolBox):
    def __init__(self, parent: QWidget, config: _window.FnExecuteWindowConfig):
        super().__init__(parent)
        self._config = config

        self._groups: Dict[str, FnParameterGroupPage] = {}

    def add_parameter_group(self, group_name: str | None) -> FnParameterGroupPage:
        if group_name is None:
            group_name = self._config.default_parameter_group_name
        if group_name in self._groups:
            return self._groups[group_name]
        page = FnParameterGroupPage(self)
        self.addItem(page, QIcon(), group_name)
        self._groups[group_name] = page
        return page

    def get_parameter_group(
        self, group_name: str | None
    ) -> FnParameterGroupPage | None:
        if group_name is None:
            group_name = self._config.default_parameter_group_name
        return self._groups.get(group_name, None)

    def get_parameter_groups(self) -> Dict[str, FnParameterGroupPage]:
        return self._groups.copy()


class FnParameterArea(QWidget):
    def __init__(self, parent: QWidget, config: _window.FnExecuteWindowConfig):
        super().__init__(parent)

        self._config: _window.FnExecuteWindowConfig = config

        self._vlayout_main = QVBoxLayout(self)
        self._setup_top_zone()
        self._setup_bottom_zone()

    def _setup_top_zone(self):
        self._parameter_group_box = FnParameterGroupBox(self, self._config)
        # create a parameter group box for parameters of default group (group name is None)
        self._parameter_group_box.add_parameter_group(None)
        self._parameter_group_box.setObjectName("_parameter_group_box")
        self._vlayout_main.addWidget(self._parameter_group_box)

    def _setup_bottom_zone(self):
        self._widget_operation_container = QWidget(self)
        self._widget_operation_container.setObjectName("widget_operation_container")
        self._vlayout_operation_container = QVBoxLayout(
            self._widget_operation_container
        )
        # self._vlayout_operation_container.setContentsMargins(0, 0, 0, 0)
        # self._vlayout_operation_container.setSpacing(2)

        self._vlayout_operation_container.addWidget(
            utils.hline(self._widget_operation_container)
        )

        self._checkbox_clear_log_output = QCheckBox(self._widget_operation_container)
        self._checkbox_clear_log_output.setText(self._config.clear_checkbox_text)
        self._vlayout_operation_container.addWidget(self._checkbox_clear_log_output)

        self._hlayout_buttons = QHBoxLayout(self._widget_operation_container)
        self._button_execute = QPushButton(self)
        self._button_execute.setText(self._config.execute_button_text)
        self._hlayout_buttons.addWidget(self._button_execute)
        self._button_cancel = QPushButton(self)
        self._button_cancel.setText(self._config.cancel_button_text)
        self._hlayout_buttons.addWidget(self._button_cancel)
        self._vlayout_operation_container.addLayout(self._hlayout_buttons)

        self._vlayout_main.addWidget(self._widget_operation_container)
