from __future__ import annotations

import sys
import warnings
from collections import OrderedDict
from collections.abc import Callable, Sequence
from typing import Literal, Dict, Any, Type, Tuple, List

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import QApplication, QStyleFactory

from . import ucontext
from ..bundle import FnBundle, WidgetConfigTypes
from ..fn import ParameterInfo
from ..paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    is_parameter_widget_class,
)
from ..parser import FnParser
from ..widgets import ParameterWidgetFactory
from ..windows import (
    FnExecuteWindowConfig,
    FnSelectWindow,
    FnSelectWindowConfig,
    FnExecuteWindow,
)


class GUIAdapter(object):

    def __init__(
        self,
        *,
        select_window_config: FnSelectWindowConfig | None = None,
        app_style: str | None = None,
        on_app_start: Callable[[QApplication], None] | None = None,
        on_app_shutdown: Callable | None = None,
    ):
        self._select_window_config = select_window_config or FnSelectWindowConfig()
        self._app_style: str | None = app_style
        self._on_app_start: Callable[[QApplication], None] | None = on_app_start
        self._on_app_shutdown: Callable | None = on_app_shutdown

        self._bundles: Dict[Callable, FnBundle] = OrderedDict()
        self._fn_parser = FnParser()

        self._application: QApplication | None = None
        self._select_window: FnSelectWindow | None = None
        self._execute_window: FnExecuteWindow | None = None

    def add(
        self,
        fn: Callable,
        display_name: str | None = None,
        group: str | None = None,
        icon: str | QIcon | QPixmap | None = None,
        document: str | None = None,
        document_format: Literal["markdown", "html", "plaintext"] = "markdown",
        cancelable: bool = False,
        on_execute_result: Callable[[Any], None] = None,
        on_execute_error: Callable[[Exception], None] = None,
        *,
        window_config: FnExecuteWindowConfig | None = None,
        widget_configs: Dict[str, WidgetConfigTypes] | None = None,
    ):
        # create the FnInfo from the function and given arguments
        fn_info = self._fn_parser.parse_fn_info(
            fn,
            display_name=display_name,
            group=group,
            icon=icon,
            document=document,
            document_format=document_format,
        )
        fn_info.cancelable = cancelable
        # configs for parameter widget can be from various sources
        # for example, from the function signature or function docstring, those are automatically parsed by FnParser
        # user can override those auto-parsed configs with 'widget_configs' of this method
        # That means the user's 'widget_configs' has a higher priority than the auto-parsed widget configs
        user_widget_configs = widget_configs or {}
        parsed_widget_configs = self._fn_parser.parse_widget_configs(fn_info)
        widget_configs = self._merge_widget_configs(
            parameters=fn_info.parameters,
            parsed_configs=parsed_widget_configs,
            user_configs=user_widget_configs,
        )

        window_config = window_config or FnExecuteWindowConfig()
        bundle = FnBundle(
            fn_info,
            window_config=window_config,
            param_widget_configs=widget_configs,
            on_execute_result=on_execute_result,
            on_execute_error=on_execute_error,
        )
        self._bundles[fn] = bundle

    def remove(self, fn: Callable):
        if fn in self._bundles:
            del self._bundles[fn]

    def exists(self, fn: Callable) -> bool:
        return fn in self._bundles

    def get_bundle(self, fn: Callable) -> FnBundle | None:
        return self._bundles.get(fn, None)

    def clear_bundles(self):
        self._bundles.clear()

    def run(
        self, argv: Sequence[str] | None = None, *, show_select_window: bool = False
    ):
        if self._application is None:
            self._start_application(argv)
        # noinspection PyProtectedMember
        ucontext._reset()
        count = len(self._bundles)
        if count == 0:
            self._shutdown_application()
            raise RuntimeError("no functions has been added")

        try:

            if count == 1 and not show_select_window:
                fn_bundle = next(iter(self._bundles.values()))
                self._show_execute_window(fn_bundle)
            else:
                window_config = self._select_window_config or FnExecuteWindowConfig()
                self._show_select_window(list(self._bundles.values()), window_config)

            self._application.exec()
        except Exception as e:
            raise e
        finally:
            self._shutdown_application()

    def is_application_started(self) -> bool:
        return self._application is not None

    @property
    def application(self) -> QApplication | None:
        return self._application

    def _start_application(self, argv: Sequence[str] | None):
        if argv is None:
            argv = sys.argv

        if self._application is not None:
            warnings.warn("application already started")
            return

        if self._app_style:
            QApplication.setStyle(QStyleFactory.create(self._app_style))

        self._application = QApplication(argv)

        if self._on_app_start:
            self._on_app_start(self._application)

    def _shutdown_application(self):
        if self._application is None:
            warnings.warn("application not started yet")
            return
        # noinspection PyProtectedMember
        ucontext._reset()

        self._application.closeAllWindows()
        self._application.quit()
        self._application = None

        if self._on_app_shutdown:
            self._on_app_shutdown()

    def _show_select_window(
        self, bundles: List[FnBundle], select_window_config: FnSelectWindowConfig
    ):
        if self._select_window is not None:
            return
        self._select_window = FnSelectWindow(
            parent=None,
            bundles=bundles,
            config=select_window_config,
        )
        self._select_window.setAttribute(Qt.WA_DeleteOnClose, True)
        # noinspection PyUnresolvedReferences
        self._select_window.destroyed.connect(self._on_select_window_destroyed)
        self._select_window.start()

    def _on_select_window_destroyed(self):
        self._select_window = None

    # noinspection PyUnresolvedReferences
    def _show_execute_window(self, bundle: FnBundle):
        if self._execute_window is not None:
            return
        self._execute_window = FnExecuteWindow(None, bundle=bundle)
        self._execute_window.setAttribute(Qt.WA_DeleteOnClose, True)
        self._execute_window.setWindowModality(Qt.ApplicationModal)
        self._execute_window.destroyed.connect(self._on_execute_window_destroyed)
        self._execute_window.show()

    def _on_execute_window_destroyed(self):
        self._execute_window = None

    # noinspection GrazieInspection
    def _merge_widget_configs(
        self,
        parameters: Dict[str, ParameterInfo],
        parsed_configs: Dict[str, Tuple[str | None, dict]],
        user_configs: Dict[str, WidgetConfigTypes],
    ) -> Dict[str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig | dict]]:
        user_configs = user_configs.copy()
        normalized_configs = OrderedDict()

        for param_name, parsed_config_item in parsed_configs.items():

            param_info = parameters.get(param_name, None)
            assert param_info is not None

            widget_class, widget_config = parsed_config_item
            user_config_item = user_configs.pop(param_name, None)

            # if user config not provided
            if not user_config_item:
                if widget_class is None:
                    widget_class = self._find_widget_class_by_type(param_info.typename)
                else:
                    widget_class = self._find_widget_class_by_name(widget_class)
                normalized_configs[param_name] = (widget_class, widget_config)
                continue

            if not self._check_user_widget_config(user_config_item):
                raise ValueError(
                    f"invalid widget configs for parameter '{param_name}': {user_config_item}"
                )

            user_widget_class: Type[BaseParameterWidget] | str | None = None
            user_widget_config: dict | BaseParameterWidgetConfig | None = None
            if is_parameter_widget_class(user_config_item):
                user_widget_class = user_config_item
            elif isinstance(user_config_item, str):
                user_widget_class = user_config_item
            elif isinstance(user_config_item, dict):
                user_widget_config = user_config_item
            elif isinstance(user_config_item, BaseParameterWidgetConfig):
                user_widget_class = user_config_item.target_widget_class()
                user_widget_config = user_config_item
            elif isinstance(user_config_item, tuple) and len(user_config_item) == 2:
                user_widget_class = user_config_item[0]
                user_widget_config = user_config_item[1]
            else:
                raise ValueError(
                    f"invalid widget configs for parameter '{param_name}': {user_config_item}"
                )

            _widget_class = user_widget_class or widget_class
            _widget_config = user_widget_config or widget_config

            if _widget_class is None:
                _widget_class = self._find_widget_class_by_type(param_info.typename)

            if isinstance(_widget_class, str):
                _widget_class = self._find_widget_class_by_name(_widget_class)

            normalized_configs[param_name] = (_widget_class, _widget_config)

        # process remaining user widget configs (if any)
        # if user_configs:
        #     for param_name, parsed_config_item in user_configs.items():
        #         if not isinstance(parsed_config_item, tuple) or len(parsed_config_item) != 2:
        #             raise ValueError(
        #                 f"widget class and widget configs must be provided as a tuple for parameter '{param_name}"
        #             )
        #         _widget_class_2, _widget_config_2 = parsed_config_item
        #         if not self._is_widget_class_type(_widget_class_2):
        #             raise ValueError(
        #                 f"invalid widget class for parameter '{param_name}': {_widget_class_2}"
        #             )
        #         if not self._is_widget_config_type(_widget_config_2):
        #             raise ValueError(
        #                 f"invalid widget configs for parameter '{param_name}': {_widget_config_2}"
        #             )
        #         if not is_parameter_widget_class(_widget_class_2):
        #             _widget_class_2 = self._find_widget_class_by_name(_widget_class_2)
        #
        #         normalized_configs[param_name] = (_widget_class_2, _widget_config_2)

        return normalized_configs

    @staticmethod
    def _find_widget_class_by_type(typ: str | Type) -> Type[BaseParameterWidget]:
        widget_class = ParameterWidgetFactory.get(typ)
        if not is_parameter_widget_class(widget_class):
            raise ValueError(f"no registered widget class found for type: {typ}")
        return widget_class

    @staticmethod
    def _find_widget_class_by_name(widget_class_name: str) -> Type[BaseParameterWidget]:
        widget_class = ParameterWidgetFactory.find_by_widget_class_name(
            widget_class_name
        )
        if not is_parameter_widget_class(widget_class):
            raise ValueError(f"no registered widget class found: {widget_class_name}")
        return widget_class

    @staticmethod
    def _is_widget_config_type(item: Any) -> bool:
        return isinstance(item, (BaseParameterWidgetConfig, dict))

    @staticmethod
    def _is_widget_class_type(item: Any) -> bool:
        if is_parameter_widget_class(item):
            return True
        if isinstance(item, str) and item.strip() != "":
            return True
        return False

    def _check_user_widget_config(self, item: Any) -> bool:
        if self._is_widget_class_type(item):
            return True
        if self._is_widget_config_type(item):
            return True
        if isinstance(item, tuple) and len(item) == 2:
            return self._is_widget_class_type(item[0]) and self._is_widget_config_type(
                item[1]
            )
        return False
