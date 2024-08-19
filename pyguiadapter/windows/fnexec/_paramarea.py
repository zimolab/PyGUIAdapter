from __future__ import annotations

from collections import OrderedDict
from typing import Dict, Any, List, Tuple, Type, Literal

from qtpy.QtCore import Signal
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBox,
    QCheckBox,
    QPushButton,
    QScrollArea,
    QSpacerItem,
    QSizePolicy,
)

from . import _window
from ._common import (
    ParameterAlreadyExistError,
    ParameterNotFoundError,
)
from ... import utils
from ...paramwidget import BaseParameterWidget, BaseParameterWidgetConfig


class FnParameterGroupPage(QWidget):
    def __init__(self, parent: QWidget, group_name: str):
        super().__init__(parent)

        self._group_name = group_name
        self._parameters: Dict[str, BaseParameterWidget] = OrderedDict()

        self._vlayout_main = QVBoxLayout(self)
        self._vlayout_main.setContentsMargins(0, 0, 0, 0)

        self._scrollarea_parameters = QScrollArea(self)
        self._scrollarea_parameters.setWidgetResizable(True)

        self._scrollarea_content = QWidget(self._scrollarea_parameters)
        self._scrollarea_content.setObjectName("widget_scrollarea_content")
        self._vlayout_content = QVBoxLayout(self._scrollarea_content)
        self._scrollarea_content.setLayout(self._vlayout_content)

        self._scrollarea_parameters.setWidget(self._scrollarea_content)
        self._vlayout_main.addWidget(self._scrollarea_parameters)

        self._bottom_spacer = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

    @property
    def group_name(self) -> str:
        return self._group_name

    def scroll_to(self, parameter_name: str, x: int = 50, y: int = 50) -> None:
        widget = self.get_parameter_widget(parameter_name)
        if widget is None:
            return
        self._scrollarea_parameters.ensureWidgetVisible(widget, x, y)

    def upsert_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
        index: int | None = None,
    ):
        if parameter_name.strip() == "":
            raise ValueError("parameter_name is an empty-string")
        # if there is an old widget for the parameter, remove it from the layout
        # and then release it
        if parameter_name in self._parameters:
            old_widget = self._parameters[parameter_name]
            old_index = self._vlayout_content.indexOf(old_widget)
            if old_index >= 0:
                self._vlayout_content.takeAt(index)
            old_widget.deleteLater()
            del self._parameters[parameter_name]
            if index is None:
                index = old_index
        else:
            if index is None:
                index = -1

        # add new widget to the layout
        new_widget = widget_class.new(
            self._scrollarea_content, parameter_name, widget_config
        )
        self._add_to_scrollarea(new_widget, index)
        self._parameters[parameter_name] = new_widget

    def insert_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
        index: int = -1,
    ):
        if parameter_name.strip() == "":
            raise ValueError("parameter_name is an empty-string")

        if parameter_name in self._parameters:
            raise ParameterAlreadyExistError(parameter_name)

        self.upsert_parameter_widget(parameter_name, widget_class, widget_config, index)

    def update_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
    ):
        if parameter_name.strip() == "":
            raise ValueError("parameter_name is an empty-string")
        if parameter_name not in self._parameters:
            raise ParameterNotFoundError(parameter_name)
        self.upsert_parameter_widget(parameter_name, widget_class, widget_config, None)

    def get_parameter_widget(self, parameter_name: str) -> BaseParameterWidget | None:
        return self._parameters.get(parameter_name, None)

    def has_parameter_widget(self, parameter_name: str) -> bool:
        if not self._parameters:
            return False
        return parameter_name in self._parameters

    def remove_parameter_widget(self, parameter_name: str):
        if parameter_name.strip() == "":
            raise ValueError("parameter_name is an empty-string")
        if parameter_name not in self._parameters:
            return
        widget = self._parameters[parameter_name]
        index = self._vlayout_content.indexOf(widget)
        self._vlayout_content.takeAt(index)
        widget.deleteLater()
        del self._parameters[parameter_name]

    def clear_parameter_widgets(self):
        param_names = list(self._parameters.keys())
        for param_name in param_names:
            self.remove_parameter_widget(param_name)

    def parameter_count(self) -> int:
        return len(self._parameters)

    def get_parameter_names(self) -> List[str]:
        return list(self._parameters.keys())

    def get_parameter_value(self, parameter_name: str) -> Any:
        widget = self.get_parameter_widget(parameter_name)
        if widget is None:
            raise ParameterNotFoundError(parameter_name)
        return widget.get_value()

    def set_parameter_value(
        self, parameter_name: str, value: Any, ignore_unknown_parameter: bool = False
    ):
        widget = self.get_parameter_widget(parameter_name)
        if widget is None:
            if ignore_unknown_parameter:
                return
            raise ParameterNotFoundError(parameter_name)
        widget.set_value(value)

    def get_parameter_values(self) -> Dict[str, Any]:
        params = OrderedDict()
        for param_name, param_widget in self._parameters.items():
            param_value = param_widget.get_value()
            params[param_name] = param_value
        return params

    def set_parameter_values(
        self,
        values: Dict[str, Any],
        strategy: Literal[
            "collect_known_params", "collect_unknown_params", "fail_on_unknown_params"
        ] = "fail_on_unknown_params",
    ) -> List[str]:
        ret = []
        for param_name, param_value in values.items():
            widget = self.get_parameter_widget(param_name)
            if widget is None:
                if strategy == "fail_on_unknown_param":
                    raise ParameterNotFoundError(param_name)
                if strategy == "collect_unknown_param":
                    ret.append(param_name)
            else:
                widget.set_value(param_value)
                if strategy == "collect_known_param":
                    ret.append(param_name)
        return ret

    def _add_to_scrollarea(self, widget: BaseParameterWidget, index: int):
        self._vlayout_content.removeItem(self._bottom_spacer)
        self._vlayout_content.insertWidget(index, widget)
        self._vlayout_content.addSpacerItem(self._bottom_spacer)


class FnParameterGroupBox(QToolBox):
    def __init__(self, parent: QWidget, config: _window.FnExecuteWindowConfig):
        self._config = config
        self._groups: Dict[str, FnParameterGroupPage] = OrderedDict()

        super().__init__(parent)

    def upsert_parameter_group(self, group_name: str | None) -> FnParameterGroupPage:
        group_name = self._group_name(group_name)
        if group_name in self._groups:
            return self._groups[group_name]

        page = FnParameterGroupPage(self, group_name=group_name)
        icon = self._group_icon(group_name)
        self.addItem(page, icon, group_name)
        self._groups[group_name] = page
        return page

    def add_default_group(self) -> FnParameterGroupPage:
        return self.upsert_parameter_group(None)

    def has_parameter_group(self, group_name: str | None) -> bool:
        return self._group_name(group_name) in self._groups

    def _get_parameter_group(
        self, group_name: str | None
    ) -> FnParameterGroupPage | None:
        return self._groups.get(self._group_name(group_name), None)

    def remove_parameter_group(self, group_name: str | None):
        group = self._groups.get(self._group_name(group_name), None)
        if group is None:
            return
        self._remove_group(group)

    def get_parameter_group_names(self) -> List[str]:
        return list(self._groups.keys())

    def _get_parameter_group_of(
        self, parameter_name: str
    ) -> FnParameterGroupPage | None:
        for group_name, group in self._groups.items():
            if group.has_parameter_widget(parameter_name):
                return group
        return None

    def has_parameter(self, parameter_name: str) -> bool:
        if not self._groups:
            return False
        return any(
            group.has_parameter_widget(parameter_name)
            for group in self._groups.values()
        )

    def add_parameter(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
    ):
        if self.has_parameter(parameter_name):
            raise ParameterAlreadyExistError(parameter_name)
        group_page = self.upsert_parameter_group(widget_config.group)
        group_page.insert_parameter_widget(parameter_name, widget_class, widget_config)

    def remove_parameter(self, parameter_name: str, safe_remove: bool = True):
        group, widget = self._get_group_and_widget(parameter_name)
        if group is None or widget is None:
            if safe_remove:
                return
            raise ParameterNotFoundError(parameter_name)
        group.remove_parameter_widget(parameter_name)
        if group.parameter_count() <= 0:
            self._remove_group(group)

    def clear_parameters(self):
        for group in list(self._groups.values()):
            self._remove_group(group)
        self._groups.clear()

    def get_parameter_value(self, parameter_name: str) -> Any:
        _, widget = self._get_group_and_widget(parameter_name)
        if widget is None:
            raise ParameterNotFoundError(parameter_name)
        return widget.get_value()

    def get_parameter_values(self) -> Dict[str, Any]:
        params = OrderedDict()
        for group_page in self._groups.values():
            params.update(group_page.get_parameter_values())
        return params

    def get_parameter_values_of(self, group_name: str | None) -> Dict[str, Any]:
        group_name = self._group_name(group_name)
        group = self._get_parameter_group(group_name)
        if group is None:
            return {}
        return group.get_parameter_values()

    def get_parameter_names(self) -> List[str]:
        return [
            parameter_name
            for group_page in self._groups.values()
            for parameter_name in group_page.get_parameter_names()
        ]

    def get_parameter_names_of(self, group_name: str) -> List[str]:
        group = self._get_parameter_group(group_name)
        if group is None:
            return []
        return group.get_parameter_names()

    def set_parameter_value(
        self, parameter_name: str, value: Any, ignore_unknown_parameter: bool = False
    ):
        _, widget = self._get_group_and_widget(parameter_name)
        if widget is None:
            if ignore_unknown_parameter:
                return
            raise ParameterNotFoundError(parameter_name)
        widget.set_value(value)

    def set_parameter_values(self, params: Dict[str, Any]) -> List[str]:
        """
        Set the value of the parameters and collect the unknown parameter names
        """
        params = params.copy()
        for group_page in self._groups.values():
            used_params = group_page.set_parameter_values(
                params, strategy="collect_known_params"
            )
            for used_param in used_params:
                del params[used_param]
        return list(params.keys())

    def active_parameter_group(self, group_name: str | None) -> bool:
        group = self._get_parameter_group(group_name)
        if group is None:
            return False
        index = self.indexOf(group)
        if index >= 0:
            self.setCurrentIndex(index)
            return True
        return False

    def scroll_to_parameter(self, parameter_name: str, x: int = 50, y: int = 50):
        group, widget = self._get_group_and_widget(parameter_name)
        if group is None or widget is None:
            return

        if not self.active_parameter_group(group_name=group.group_name):
            return
        group.scroll_to(parameter_name, x, y)

    def _get_group_and_widget(
        self, parameter_name: str
    ) -> Tuple[FnParameterGroupPage | None, BaseParameterWidget | None]:
        if not self._groups:
            return None, None
        for group_page in self._groups.values():
            widget = group_page.get_parameter_widget(parameter_name)
            if widget is not None:
                return group_page, widget
        return None, None

    def _remove_group(self, group: FnParameterGroupPage):
        if not group:
            return
        index = self.indexOf(group)
        if index >= 0:
            self.removeItem(index)
        group.clear_parameter_widgets()
        group.deleteLater()
        if group.group_name in self._groups:
            del self._groups[group.group_name]

    def _group_name(self, name: str | None) -> str:
        if name is None:
            return self._config.default_parameter_group_name
        return name

    def _group_icon(self, group_name: str | None) -> QIcon:
        group_name = self._group_name(group_name)
        if group_name == self._config.default_parameter_group_icon:
            icon = self._config.default_parameter_group_icon
        elif group_name in self._config.parameter_group_icons:
            icon = self._config.parameter_group_icons[group_name]
        else:
            return QIcon()
        return utils.get_icon(icon) or QIcon()


class FnParameterArea(QWidget):

    execute_button_clicked = Signal()
    cancel_button_clicked = Signal()
    clear_button_clicked = Signal()

    def __init__(self, parent: QWidget, config: _window.FnExecuteWindowConfig):
        super().__init__(parent)
        self._config: _window.FnExecuteWindowConfig = config
        self._vlayout_main = QVBoxLayout(self)
        self._setup_top_zone()
        self._setup_bottom_zone()

    def _setup_top_zone(self):
        self._groupbox_parameters = FnParameterGroupBox(self, self._config)
        self._groupbox_parameters.add_default_group()
        self._groupbox_parameters.setObjectName("_group_box_parameters")
        self._vlayout_main.addWidget(self._groupbox_parameters)

    def _setup_bottom_zone(self):

        widget_texts = self._config.widget_texts

        self._widget_op_area = QWidget(self)
        self._vlayout_op_widgets = QVBoxLayout(self._widget_op_area)
        self._vlayout_op_widgets.setContentsMargins(0, 0, 0, 0)

        self._vlayout_op_widgets.addWidget(utils.hline(self._widget_op_area))

        self._checkbox_clear_log_output = QCheckBox(self._widget_op_area)
        self._checkbox_clear_log_output.setText(widget_texts.clear_checkbox_text)
        self._vlayout_op_widgets.addWidget(self._checkbox_clear_log_output)

        self._hlayout_buttons = QHBoxLayout(self._widget_op_area)

        # Execute button
        self._button_execute = QPushButton(self)
        self._button_execute.setText(widget_texts.execute_button_text)
        # noinspection PyUnresolvedReferences
        self._button_execute.clicked.connect(self.execute_button_clicked)
        self._hlayout_buttons.addWidget(self._button_execute)

        # Clear button
        self._button_clear = QPushButton(self)
        self._button_clear.setText(widget_texts.clear_button_text)
        # noinspection PyUnresolvedReferences
        self._button_clear.clicked.connect(self.clear_button_clicked)
        self._hlayout_buttons.addWidget(self._button_clear)

        # Cancel button
        self._button_cancel = QPushButton(self)
        self._button_cancel.setText(widget_texts.cancel_button_text)
        # noinspection PyUnresolvedReferences
        self._button_cancel.clicked.connect(self.cancel_button_clicked)
        self._hlayout_buttons.addWidget(self._button_cancel)

        self._vlayout_op_widgets.addLayout(self._hlayout_buttons)
        self._vlayout_main.addWidget(self._widget_op_area)

    @property
    def parameter_group_box(self) -> FnParameterGroupBox:
        return self._groupbox_parameters

    @property
    def is_auto_clear_enabled(self) -> bool:
        return self._checkbox_clear_log_output.isChecked()

    def hide_cancel_button(self):
        self._button_cancel.hide()

    def show_cancel_button(self):
        self._button_cancel.show()

    def hide_clear_button(self):
        self._button_clear.hide()

    def show_clear_button(self):
        self._button_clear.show()

    def enable_auto_clear(self, enable: bool):
        self._checkbox_clear_log_output.setChecked(enable)

    def enable_execute_button(self, enable: bool):
        self._button_execute.setEnabled(enable)

    def enable_cancel_button(self, enable: bool):
        self._button_cancel.setEnabled(enable)
