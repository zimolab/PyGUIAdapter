from collections import OrderedDict

from typing import Dict, Any, List, Tuple, Type, Literal, Optional

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QSpacerItem,
    QSizePolicy,
)

from .base import BaseParameterPage, BaseParameterGroupBox
from .._base import FnExecuteWindowConfig
from ....exceptions import ParameterAlreadyExistError, ParameterNotFoundError
from ....paramwidget import BaseParameterWidget, BaseParameterWidgetConfig
from ....utils import get_icon


class ParameterGroupPage(BaseParameterPage):
    # noinspection SpellCheckingInspection
    def __init__(self, parent: "ParameterGroupBox", group_name: str):
        super().__init__(parent, group_name)

        self._parameters: Dict[str, BaseParameterWidget] = OrderedDict()

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout()
        self._layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout_main)

        self._param_scrollarea = QScrollArea(self)
        self._param_scrollarea.setWidgetResizable(True)
        self._scrollarea_content = QWidget(self._param_scrollarea)
        # noinspection PyArgumentList
        self._layout_scrollerea_content = QVBoxLayout()
        self._scrollarea_content.setLayout(self._layout_scrollerea_content)
        self._param_scrollarea.setWidget(self._scrollarea_content)
        self._layout_main.addWidget(self._param_scrollarea)

        self._bottom_spacer = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

    def scroll_to(self, parameter_name: str, x: int = 50, y: int = 50) -> None:
        widget = self.get_parameter_widget(parameter_name)
        if widget is None:
            return
        self._param_scrollarea.ensureWidgetVisible(widget, x, y)

    def upsert_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
        index: Optional[int] = None,
    ) -> BaseParameterWidget:
        if parameter_name.strip() == "":
            raise ValueError("parameter_name is an empty-string")
        # if there is an old widget for the parameter, remove it from the layout
        # and then release it
        if parameter_name in self._parameters:
            old_widget = self._parameters[parameter_name]
            old_index = self._layout_scrollerea_content.indexOf(old_widget)
            if old_index >= 0:
                self._layout_scrollerea_content.takeAt(index)
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
        # noinspection PyUnresolvedReferences
        self._parent.sig_validation_failed.connect(new_widget.on_validation_failed)
        # noinspection PyUnresolvedReferences
        self._parent.sig_validation_error_cleared.connect(
            new_widget.on_clear_validation_error
        )
        self._add_to_scrollarea(new_widget, index)
        self._parameters[parameter_name] = new_widget
        return new_widget

    def insert_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
        index: int = -1,
    ) -> BaseParameterWidget:
        if parameter_name.strip() == "":
            raise ValueError("invalid parameter_name: empty-string")

        if parameter_name in self._parameters:
            raise ParameterAlreadyExistError(parameter_name)

        return self.upsert_parameter_widget(
            parameter_name, widget_class, widget_config, index
        )

    def update_parameter_widget(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
    ) -> BaseParameterWidget:
        if parameter_name.strip() == "":
            raise ValueError("parameter_name is an empty-string")
        if parameter_name not in self._parameters:
            raise ParameterNotFoundError(parameter_name)
        return self.upsert_parameter_widget(
            parameter_name, widget_class, widget_config, None
        )

    def get_parameter_widget(
        self, parameter_name: str
    ) -> Optional[BaseParameterWidget]:
        return self._parameters.get(parameter_name, None)

    def has_parameter_widget(self, parameter_name: str) -> bool:
        if not self._parameters:
            return False
        return parameter_name in self._parameters

    def remove_parameter_widget(self, parameter_name: str):
        if parameter_name.strip() == "":
            raise ValueError("invalid parameter_name: empty parameter_name")
        if parameter_name not in self._parameters:
            return
        widget = self._parameters[parameter_name]
        index = self._layout_scrollerea_content.indexOf(widget)
        self._layout_scrollerea_content.takeAt(index)
        # noinspection PyUnresolvedReferences
        self._parent.sig_validation_failed.disconnect(widget.on_validation_failed)
        # noinspection PyUnresolvedReferences
        self._parent.sig_validation_error_cleared.disconnect(
            widget.on_clear_validation_error
        )
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

    def set_parameter_value(self, parameter_name: str, value: Any):
        widget = self.get_parameter_widget(parameter_name)
        if widget is None:
            raise ParameterNotFoundError(parameter_name)
        widget.set_value(value)

    def get_parameter_values(self) -> Dict[str, Any]:
        params = OrderedDict()
        for param_name, param_widget in self._parameters.items():
            if not param_widget:
                continue
            param_value = param_widget.get_value()
            params[param_name] = param_value
        return params

    def set_parameter_values(self, values: Dict[str, Any]):
        for param_name, param_value in values.items():
            widget = self.get_parameter_widget(param_name)
            if widget is None:
                continue
            widget.set_value(param_value)

    # noinspection SpellCheckingInspection
    def _add_to_scrollarea(self, widget: BaseParameterWidget, index: int):
        self._layout_scrollerea_content.removeItem(self._bottom_spacer)
        self._layout_scrollerea_content.insertWidget(index, widget)
        self._layout_scrollerea_content.addSpacerItem(self._bottom_spacer)


class ParameterGroupBox(BaseParameterGroupBox):
    def __init__(self, parent: QWidget, config: FnExecuteWindowConfig):
        self._config = config
        self._group_pages: Dict[str, BaseParameterPage] = OrderedDict()
        super().__init__(parent)

    def upsert_parameter_group(self, group_name: Optional[str]) -> BaseParameterPage:
        group_name = self._group_name(group_name)
        if group_name in self._group_pages:
            return self._group_pages[group_name]

        page = ParameterGroupPage(self, group_name=group_name)
        icon = self._group_icon(group_name)
        self.addItem(page, icon, group_name)
        self._group_pages[group_name] = page
        return page

    def add_default_group(self) -> BaseParameterPage:
        return self.upsert_parameter_group(None)

    def has_parameter_group(self, group_name: Optional[str]) -> bool:
        return self._group_name(group_name) in self._group_pages

    def _get_parameter_group(
        self, group_name: Optional[str]
    ) -> Optional[BaseParameterPage]:
        return self._group_pages.get(self._group_name(group_name), None)

    def remove_parameter_group(self, group_name: Optional[str]):
        group = self._group_pages.get(self._group_name(group_name), None)
        if group is None:
            return
        self._remove_group(group)

    def get_parameter_group_names(self) -> List[str]:
        return list(self._group_pages.keys())

    def _get_parameter_group_of(
        self, parameter_name: str
    ) -> Optional[BaseParameterPage]:
        for group_name, group in self._group_pages.items():
            if group.has_parameter_widget(parameter_name):
                return group
        return None

    def has_parameter(self, parameter_name: str) -> bool:
        if not self._group_pages:
            return False
        return any(
            group.has_parameter_widget(parameter_name)
            for group in self._group_pages.values()
        )

    def add_parameter(
        self,
        parameter_name: str,
        widget_class: Type[BaseParameterWidget],
        widget_config: BaseParameterWidgetConfig,
    ) -> BaseParameterWidget:
        if self.has_parameter(parameter_name):
            raise ParameterAlreadyExistError(parameter_name)
        group_page = self.upsert_parameter_group(widget_config.group)
        return group_page.insert_parameter_widget(
            parameter_name, widget_class, widget_config
        )

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
        for group in list(self._group_pages.values()):
            self._remove_group(group)
        self._group_pages.clear()

    def get_parameter_value(self, parameter_name: str) -> Any:
        _, widget = self._get_group_and_widget(parameter_name)
        if widget is None:
            raise ParameterNotFoundError(parameter_name)
        return widget.get_value()

    def get_parameter_values(self) -> Dict[str, Any]:
        params = OrderedDict()
        for group_page in self._group_pages.values():
            params.update(group_page.get_parameter_values())
        return params

    def get_parameter_values_of(self, group_name: Optional[str]) -> Dict[str, Any]:
        group_name = self._group_name(group_name)
        group = self._get_parameter_group(group_name)
        if group is None:
            raise ParameterNotFoundError(group_name)
        return group.get_parameter_values()

    def get_parameter_names(self) -> List[str]:
        return [
            parameter_name
            for group_page in self._group_pages.values()
            for parameter_name in group_page.get_parameter_names()
        ]

    def get_parameter_names_of(self, group_name: str) -> List[str]:
        group = self._get_parameter_group(group_name)
        if group is None:
            raise ParameterNotFoundError(group_name)
        return group.get_parameter_names()

    def set_parameter_value(self, parameter_name: str, value: Any):
        _, widget = self._get_group_and_widget(parameter_name)
        if widget is None:
            raise ParameterNotFoundError(parameter_name)
        widget.set_value(value)

    def set_parameter_values(self, params: Dict[str, Any]):
        for group_page in self._group_pages.values():
            group_page.set_parameter_values(params)

    def active_parameter_group(self, group_name: Optional[str]) -> bool:
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
    ) -> Tuple[Optional[BaseParameterPage], Optional[BaseParameterWidget]]:
        if not self._group_pages:
            return None, None
        for group_page in self._group_pages.values():
            widget = group_page.get_parameter_widget(parameter_name)
            if widget is not None:
                return group_page, widget
        return None, None

    def _remove_group(self, group: BaseParameterPage):
        if not group:
            return
        index = self.indexOf(group)
        if index >= 0:
            self.removeItem(index)
        group.clear_parameter_widgets()
        group.deleteLater()
        if group.group_name in self._group_pages:
            del self._group_pages[group.group_name]

    def _group_name(self, name: Optional[str]) -> str:
        if name is None:
            return self._config.default_parameter_group_name
        return name

    def _group_icon(self, group_name: Optional[str]) -> QIcon:
        group_name = self._group_name(group_name)
        if group_name == self._config.default_parameter_group_icon:
            icon = self._config.default_parameter_group_icon
        elif group_name in self._config.parameter_group_icons:
            icon = self._config.parameter_group_icons[group_name]
        else:
            return QIcon()
        return get_icon(icon) or QIcon()
