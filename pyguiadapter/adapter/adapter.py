"""
@Time    : 2024.10.20
@File    : adapter.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了GUI适配器类GUIAdapter，负责管理函数和启动GUI应用。
"""

import sys
import warnings
from collections import OrderedDict
from typing import (
    Literal,
    Dict,
    Type,
    Tuple,
    List,
    Union,
    Optional,
    Callable,
    Sequence,
)

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication

from . import ucontext
from ..action import Separator
from ..bundle import FnBundle
from ..exceptions import NotRegisteredError
from ..fn import ParameterInfo
from ..menu import Menu
from ..paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    is_parameter_widget_class,
)
from ..parser import FnParser
from ..toolbar import ToolBar
from ..utils import IconType
from ..widgets import ParameterWidgetFactory
from ..window import BaseWindowEventListener
from ..windows.fnexec import FnExecuteWindow, FnExecuteWindowConfig
from ..windows.fnselect import FnSelectWindow, FnSelectWindowConfig


class GUIAdapter(object):
    """
    GUI适配器类，负责管理函数和启动GUI应用。
    """

    def __init__(
        self,
        *,
        hdpi_mode: bool = True,
        global_stylesheet: Union[str, Callable[[], str], None] = None,
        on_app_start: Optional[Callable[[QApplication], None]] = None,
        on_app_shutdown: Optional[Callable] = None,
    ):
        """
        `GUIAdapter`构造函数。用于创建`GUIAdapter`实例。

        Args:
            hdpi_mode: 启用高DPI模式。某些Qt版本上，该参数不生效。
            global_stylesheet: 应用全局样式。可以为样式表字符串，也可以为一个返回全局样式表字符串的函数。
            on_app_start: 应用启动回调函数。在应用启动时调用。
            on_app_shutdown: 应用停止回调函数。在应用停止时调用。

        Examples:
            ```python
            from pyguiadapter.adapter import GUIAdapter

            def foo(a: int, b: int, c: str):
                pass

            adapter = GUIAdapter()
            adapter.add(foo)
            adapter.run()
            ```
        """
        self._hdpi_mode: bool = hdpi_mode
        self._global_stylesheet: Optional[str] = global_stylesheet
        self._on_app_start: Optional[Callable[[QApplication], None]] = on_app_start
        self._on_app_shutdown: Optional[Callable] = on_app_shutdown

        self._bundles: Dict[Callable, FnBundle] = OrderedDict()
        self._fn_parser = FnParser()

        self._application: Optional[QApplication] = None
        self._select_window: Optional[FnSelectWindow] = None
        self._execute_window: Optional[FnExecuteWindow] = None

    def add(
        self,
        fn: Callable,
        display_name: Optional[str] = None,
        group: Optional[str] = None,
        icon: IconType = None,
        document: Optional[str] = None,
        document_format: Literal["markdown", "html", "plaintext"] = "markdown",
        cancelable: bool = False,
        *,
        widget_configs: Optional[
            Dict[str, Union[BaseParameterWidgetConfig, dict]]
        ] = None,
        window_config: Optional[FnExecuteWindowConfig] = None,
        window_listener: Optional[BaseWindowEventListener] = None,
        window_toolbar: Optional[ToolBar] = None,
        window_menus: Optional[List[Union[Menu, Separator]]] = None,
    ) -> None:
        """
        添加一个函数。

        Args:
            fn: 待添加的函数。
            display_name: 函数的显示名称。如果不指定，则使用函数的名称。
            group: 函数所属的分组。如果不指定，则将函数添加到默认分组。
            icon: 函数的图标。可以为文件路径，也可使用QtAwesome支持的图标名称。
            document: 函数的说明文档。若不指定，则尝试提取函数的docstring作为文档。
            document_format: 函数说明文档的格式。可以为"markdown"、"html"或"plaintext"。
            cancelable: 函数是否可取消。
            widget_configs: 函数参数控件配置。键为参数名，值为参数控件配置。
            window_config: 窗口配置。
            window_listener: 窗口事件监听器。
            window_toolbar: 窗口的工具栏。
            window_menus: 窗口菜单列表。

        Returns:
            无返回值
        """
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
        widget_configs: Dict[
            str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]
        ] = self._merge_widget_configs(
            parameters=fn_info.parameters,
            parsed_configs=parsed_widget_configs,
            user_configs=user_widget_configs,
        )

        window_config = window_config or FnExecuteWindowConfig()
        bundle = FnBundle(
            fn_info,
            widget_configs=widget_configs,
            window_config=window_config,
            window_listener=window_listener,
            window_toolbar=window_toolbar,
            window_menus=window_menus,
        )
        self._bundles[fn] = bundle

    def remove(self, fn: Callable) -> None:
        """
        移除一个已添加的函数。

        Args:
            fn: 待移除的函数。

        Returns:
            无返回值
        """
        if fn in self._bundles:
            del self._bundles[fn]

    def exists(self, fn: Callable) -> bool:
        """
        判断函数是否已添加。

        Args:
            fn: 目标函数

        Returns:
            函数是否已添加
        """
        return fn in self._bundles

    # def get_bundle(self, fn: Callable) -> Optional[FnBundle]:
    #     return self._bundles.get(fn, None)
    #
    # def clear_bundles(self):
    #     self._bundles.clear()

    def run(
        self,
        argv: Optional[Sequence[str]] = None,
        *,
        show_select_window: bool = False,
        select_window_config: Optional[FnSelectWindowConfig] = None,
        select_window_listener: Optional[BaseWindowEventListener] = None,
        select_window_toolbar: Optional[ToolBar] = None,
        select_window_menus: Optional[List[Union[Menu, Separator]]] = None,
    ) -> None:
        """
        启动GUI应用。

        Args:
            argv: 传递给QApplication的命令行参数。
            show_select_window: 是否强制显示函数选择窗口，当添加的函数数量大于1时，默认显示。
            select_window_config: 函数选择窗口配置。
            select_window_listener: 函数选择窗口事件监听器。
            select_window_toolbar: 函数选择窗口的工具栏。
            select_window_menus: 函数选择窗口菜单列表。

        Returns:
            无返回值
        """
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
                self._show_select_window(
                    list(self._bundles.values()),
                    config=select_window_config or FnSelectWindowConfig(),
                    listener=select_window_listener,
                    toolbar=select_window_toolbar,
                    menus=select_window_menus,
                )

            self._application.exec()
        except Exception as e:
            raise e
        finally:
            self._shutdown_application()

    def is_application_started(self) -> bool:
        return self._application is not None

    @property
    def application(self) -> Optional[QApplication]:
        return self._application

    def _start_application(self, argv: Optional[Sequence[str]]):
        if argv is None:
            argv = sys.argv

        if self._application is not None:
            warnings.warn("application already started")
            return
        if self._hdpi_mode and hasattr(Qt, "AA_EnableHighDpiScaling"):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        self._application = QApplication(argv)
        if self._global_stylesheet:
            if isinstance(self._global_stylesheet, str):
                self._application.setStyleSheet(self._global_stylesheet)
            if callable(self._global_stylesheet):
                self._application.setStyleSheet(self._global_stylesheet())

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
        self,
        bundles: List[FnBundle],
        config: FnSelectWindowConfig,
        listener: Optional[BaseWindowEventListener],
        toolbar: Optional[ToolBar],
        menus: Optional[List[Union[Menu, Separator]]],
    ):
        if self._select_window is not None:
            return
        self._select_window = FnSelectWindow(
            parent=None,
            bundles=bundles,
            config=config,
            listener=listener,
            toolbar=toolbar,
            menus=menus,
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

    def _merge_widget_configs(
        self,
        parameters: Dict[str, ParameterInfo],
        parsed_configs: Dict[str, Tuple[Optional[str], dict]],
        user_configs: Dict[str, Union[BaseParameterWidgetConfig, dict]],
    ) -> Dict[str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]]:
        final_configs: Dict[
            str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]
        ] = OrderedDict()

        for param_name, (
            p_widget_class_name,
            p_widget_config,
        ) in parsed_configs.items():
            assert isinstance(p_widget_class_name, (str, type(None)))
            assert isinstance(p_widget_config, dict)

            param_info = parameters.get(param_name, None)
            assert param_info is not None

            p_widget_class = self._get_widget_class(p_widget_class_name, param_info)

            user_config = user_configs.get(param_name, None)
            if user_config is None:
                widget_class = p_widget_class
                if not is_parameter_widget_class(widget_class):
                    raise NotRegisteredError(
                        f"unknown widget class name for: {param_info.type}"
                    )
                widget_config = widget_class.ConfigClass.new(**p_widget_config)
                final_configs[param_name] = (widget_class, widget_config)
                continue

            assert isinstance(user_config, (dict, BaseParameterWidgetConfig))
            if isinstance(user_config, dict):
                widget_class = p_widget_class
                if not is_parameter_widget_class(widget_class):
                    raise NotRegisteredError(
                        f"unknown widget class name: {p_widget_class_name}"
                    )
                # override parsed config with user config
                tmp = {**p_widget_config, **user_config}
                widget_config = widget_class.ConfigClass.new(**tmp)
                final_configs[param_name] = (widget_class, widget_config)
                continue

            # when user_config is a BaseParameterWidgetConfig instance
            widget_class = user_config.target_widget_class()
            widget_config = user_config
            final_configs[param_name] = (widget_class, widget_config)
        return final_configs

    @staticmethod
    def _get_widget_class(
        widget_class_name: Optional[str], param_info: ParameterInfo
    ) -> Optional[Type[BaseParameterWidget]]:
        if widget_class_name is not None:
            widget_class_name = widget_class_name.strip()
        if widget_class_name:
            return ParameterWidgetFactory.find_by_widget_class_name(widget_class_name)
        widget_class = ParameterWidgetFactory.find_by_typename(param_info.typename)
        if is_parameter_widget_class(widget_class):
            return widget_class
        return ParameterWidgetFactory.find_by_rule(param_info)
