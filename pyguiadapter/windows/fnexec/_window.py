from typing import Tuple, Literal, Dict, Union, Type, Any, List, Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from ._base import (
    BaseFnExecuteWindow,
    DEFAULT_EXECUTOR_CLASS,
    FnExecuteWindowConfig,
    DockWidgetArea,
    DockWidgetAreas,
)
from ._document_area import DocumentArea
from ._operation_area import OperationArea
from ._output_area import OutputArea, ProgressBarConfig
from ._parameter_area import ParameterArea
from ...adapter import ucontext
from ...bundle import FnBundle
from ...exceptions import ParameterError
from ...executor import BaseFunctionExecutor
from ...fn import FnInfo
from ...paramwidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
)
from ...utils import messagebox, get_traceback


class FnExecuteWindow(BaseFnExecuteWindow):
    def __init__(self, parent: Optional[QWidget], bundle: FnBundle):
        self._bundle: FnBundle = bundle

        self._center_widget: Optional[QWidget] = None

        self._operation_area: Optional[OperationArea] = None
        self._parameter_area: Optional[ParameterArea] = None
        self._document_area: Optional[DocumentArea] = None
        self._output_area: Optional[OutputArea] = None

        self._document_dock: Optional[QDockWidget] = None
        self._output_dock: Optional[QDockWidget] = None

        super().__init__(
            parent,
            bundle.window_config,
            bundle.window_listener,
            bundle.window_toolbar,
            bundle.window_menus,
        )
        executor_class = self._bundle.fn_info.executor or DEFAULT_EXECUTOR_CLASS
        # noinspection PyTypeChecker
        self._executor = executor_class(self, self)

        try:
            self.add_parameters(self._bundle.widget_configs)
        except Exception as e:
            messagebox.show_exception_messagebox(
                self, e, "Error when initializing parameters widgets", detail=True
            )
            exit(-1)
        # noinspection PyProtectedMember
        ucontext._current_window_created(self)

    @property
    def executor(self) -> BaseFunctionExecutor:
        return self._executor

    def _create_ui(self):
        self._config: FnExecuteWindowConfig

        super()._create_ui()

        self._center_widget = QWidget(self)
        # noinspection PyArgumentList
        layout_main = QVBoxLayout()
        self._center_widget.setLayout(layout_main)
        self.setCentralWidget(self._center_widget)

        parameter_area_layout = QVBoxLayout()
        layout_main.addLayout(parameter_area_layout)

        self._parameter_area = ParameterArea(
            self._center_widget, self._config, self._bundle
        )
        parameter_area_layout.addWidget(self._parameter_area)

        self._operation_area = OperationArea(self._center_widget, self._config)
        self._operation_area.set_cancel_button_visible(self._bundle.fn_info.cancelable)
        self._operation_area.sig_execute_requested.connect(
            self._on_execute_button_clicked
        )
        self._operation_area.sig_clear_requested.connect(self._on_clear_button_clicked)
        self._operation_area.sig_cancel_requested.connect(
            self._on_cancel_button_clicked
        )
        parameter_area_layout.addWidget(self._operation_area)

        self._document_dock = QDockWidget(self)
        self._document_area = DocumentArea(
            self._document_dock, self._config.document_browser_config
        )
        self._document_dock.setWidget(self._document_area)

        self._output_dock = QDockWidget(self)
        self._output_area = OutputArea(
            self._output_dock, self._config.output_browser_config
        )
        self._output_dock.setWidget(self._output_area)

    # noinspection PyUnresolvedReferences
    def apply_configs(self):
        super().apply_configs()

        self._config: FnExecuteWindowConfig

        if self._config.title is None:
            title = self._bundle.fn_info.display_name or ""
        else:
            title = self._config.title
        self.set_title(title)

        icon = self._config.icon or self._bundle.fn_info.icon
        self.set_icon(icon)

        self._operation_area.set_cancel_button_visible(self._bundle.fn_info.cancelable)
        self._operation_area.set_cancel_button_enabled(False)

        self.set_document_dock_property(
            title=self._config.document_dock_title,
            visible=self._config.document_dock_visible,
            floating=self._config.document_dock_floating,
            area=self._config.document_dock_initial_area,
        )
        self.set_document(
            self._bundle.fn_info.document, self._bundle.fn_info.document_format
        )

        self.set_output_dock_property(
            title=self._config.output_dock_title,
            visible=self._config.output_dock_visible,
            floating=self._config.output_dock_floating,
            area=self._config.output_dock_initial_area,
        )

        if self._config.initial_docks_state == "tabified":
            self.tabify_docks()

        self.resize_document_dock(self._config.document_dock_initial_size)
        self.resize_output_dock(self._config.output_dock_initial_size)

        self.set_statusbar_visible(self._config.statusbar_visible)

    def update_progressbar_config(
        self, config: Union[ProgressBarConfig, dict, None]
    ) -> None:
        """
        更新进度条配置。

        Args:
            config: 进度条配置

        Returns:
            无返回值
        """
        if isinstance(config, dict):
            config = ProgressBarConfig(**config)
        self._output_area.update_progressbar_config(config)

    def show_progressbar(self) -> None:
        """
        显示进度条。

        Returns:
            无返回值
        """
        self._output_area.show_progressbar()

    def hide_progressbar(self) -> None:
        """
        隐藏进度条。

        Returns:
            无返回值
        """
        self._output_area.hide_progressbar()
        self._output_area.scroll_to_bottom()

    def update_progress(
        self, current_value: int, message: Optional[str] = None
    ) -> None:
        """
        更新进度条进度。

        Args:
            current_value: 当前进度
            message: 额外信息

        Returns:

        """
        self._output_area.update_progress(current_value, message)

    def append_output(
        self, text: str, html: bool = False, scroll_to_bottom: bool = True
    ) -> None:
        """
        把文本追加到输出浏览器中。

        Args:
            text: 带输出的文本
            html: 是否为html格式
            scroll_to_bottom: 完成后是否将输出浏览器滚动到底部

        Returns:
            无返回值
        """
        self._output_area.append_output(text, html)
        if scroll_to_bottom:
            self._output_area.scroll_to_bottom()

    def clear_output(self) -> None:
        """
        清除输出浏览器内容。

        Returns:
            无返回值
        """
        self._output_area.clear_output()

    def set_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ) -> None:
        """
        设置函数说明文档。

        Args:
            document: 文档内容
            document_format: 文档格式

        Returns:
            无返回值
        """
        self._document_area.set_document(document, document_format)

    def add_parameter(
        self,
        parameter_name: str,
        config: Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig],
    ) -> None:
        """
        添加一个新的函数参数。

        Args:
            parameter_name: 要增加的函数参数名称
            config: 函数参数配置，格式为: (参数控件类, 参数控件配置类实例)

        Returns:
            无返回值

        Raises:
            ParameterError: 当参数为空、参数名称重复时将引发此异常。
        """
        self._parameter_area.add_parameter(parameter_name, config)

    def add_parameters(
        self,
        configs: Dict[str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]],
    ) -> None:
        """
        增加一组新的函数参数。

        Args:
            configs: 要增加的函数参数名称及其配置

        Returns:
            无返回值

        Raises:
            ParameterError: 当参数为空、参数名称重复时将引发此异常。
        """
        self._parameter_area.add_parameters(configs)

    def remove_parameter(
        self, parameter_name: str, ignore_unknown_parameter: bool = True
    ) -> None:
        """
        移除指定参数控件。

        Args:
            parameter_name: 要移除的指定参数名称
            ignore_unknown_parameter: 是否忽略未知参数

        Returns:
            无返回值

        Raises:
            ParameterNotFoundError: 当参数`parameter_name`不存在且`ignore_unknown_parameter`为`False`，将引发此异常。
        """
        self._parameter_area.remove_parameter(
            parameter_name, ignore_unknown_parameter=ignore_unknown_parameter
        )

    def has_parameter(self, parameter_name: str) -> bool:
        """
        判断是否存在指定参数名称。

        Args:
            parameter_name: 带判断的参数名称

        Returns:
            存在指定参数时返回`True`，否则返回`False`。
        """
        return self._parameter_area.has_parameter(parameter_name)

    def clear_parameters(self):
        """
        清除所有参数。

        Returns:
            无返回值
        """
        self._parameter_area.clear_parameters()

    def get_parameter_value(self, parameter_name: str) -> Any:
        """
        获取指定参数当前值。

        Args:
            parameter_name: 参数名称

        Returns:
            返回当前值。

        Raises:
            ParameterNotFoundError: 若指定参数不存在，则引发此异常。
            ParameterError: 若无法从对应控件获取值，那么将引发此异常。

        """
        return self._parameter_area.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        """
        获取所有参数的当前值。

        Returns:
            以字典形式返回当前所有参数的值。

        Raises:
            ParameterError: 若无法从对应控件获取值，那么将引发此异常。
        """
        return self._parameter_area.get_parameter_values()

    def set_parameter_value(self, parameter_name: str, value: Any) -> None:
        """
        设置参数当前值。

        Args:
            parameter_name: 参数名称
            value: 要设置的值。

        Returns:
            无返回值

        Raises:
            ParameterNotFoundError: 若指定参数不存在，则引发此异常。
            ParameterError: 若无法将值设置到对应的控件，那么将引发此异常。
        """
        self._parameter_area.set_parameter_value(parameter_name, value)

    def set_parameter_values(self, values: Dict[str, Any]) -> None:
        """
        设置多个参数的当前值。

        Args:
            values: 要设置的参数名称和值。

        Returns:
            无返回值。

        Raises:
            ParameterError: 若无法将值设置到对应的控件，那么将引发此异常。
        """
        self._parameter_area.clear_parameter_error(None)
        if not values:
            return
        self._parameter_area.set_parameter_values(values)

    def get_parameter_names(self) -> List[str]:
        return self._parameter_area.get_parameter_names()

    def get_parameter_names_of(self, group_name: str) -> List[str]:
        return self._parameter_area.get_parameter_names_of(group_name)

    def set_output_dock_property(
        self,
        *,
        title: Optional[str] = None,
        visible: Optional[bool] = None,
        floating: Optional[bool] = None,
        area: Optional[DockWidgetArea] = None,
    ):
        if title is not None:
            self.set_output_dock_title(title)
        if visible is not None:
            self.set_output_dock_visible(visible)
        if floating is not None:
            self.set_output_dock_floating(floating)
        if area is not None:
            self.set_output_dock_area(area)

    def set_document_dock_property(
        self,
        *,
        title: Optional[str] = None,
        visible: Optional[bool] = None,
        floating: Optional[bool] = None,
        area: Optional[DockWidgetArea] = None,
    ):
        if title is not None:
            self.set_document_dock_title(title)
        if visible is not None:
            self.set_document_dock_visible(visible)
        if floating is not None:
            self.set_document_dock_floating(floating)
        if area is not None:
            self.set_document_dock_area(area)

    def set_allowed_dock_areas(self, areas: Optional[DockWidgetAreas]):
        if areas is None:
            return
        self._document_dock.setAllowedAreas(areas)
        self._output_dock.setAllowedAreas(areas)

    def set_output_dock_visible(self, visible: bool):
        self._output_dock.setVisible(visible)

    def is_output_dock_visible(self) -> bool:
        return self._output_dock.isVisible()

    def set_document_dock_visible(self, visible: bool):
        self._document_dock.setVisible(visible)

    def is_document_dock_visible(self) -> bool:
        return self._document_dock.isVisible()

    def set_document_dock_floating(self, floating: bool):
        self._document_dock.setFloating(floating)

    def is_document_dock_floating(self) -> bool:
        return self._document_dock.isFloating()

    def set_output_dock_floating(self, floating: bool):
        self._output_dock.setFloating(floating)

    def is_output_dock_floating(self) -> bool:
        return self._output_dock.isFloating()

    def set_document_dock_title(self, title: str):
        if title is None:
            return
        self._document_dock.setWindowTitle(title)

    def get_document_dock_title(self) -> str:
        return self._document_dock.windowTitle()

    def get_document_dock_size(self) -> Tuple[int, int]:
        size = self._document_dock.size()
        return size.width(), size.height()

    def set_output_dock_title(self, title: str):
        if title is None:
            return
        self._output_dock.setWindowTitle(title)

    def get_output_dock_title(self) -> str:
        return self._output_dock.windowTitle()

    def set_document_dock_area(self, area: DockWidgetArea):
        if not self._document_dock.isAreaAllowed(area):
            messagebox.show_warning_message(self, f"Invalid dock area: {area}")
            return
        self.addDockWidget(area, self._document_dock)

    def get_document_dock_area(self) -> DockWidgetArea:
        return self.dockWidgetArea(self._document_dock)

    def set_output_dock_area(self, area: DockWidgetArea):
        if not self._output_dock.isAreaAllowed(area):
            messagebox.show_warning_message(self, f"Invalid dock area: {area}")
            return
        self.addDockWidget(area, self._output_dock)

    def get_output_dock_area(self) -> DockWidgetArea:
        return self.dockWidgetArea(self._output_dock)

    def get_output_dock_size(self) -> Tuple[int, int]:
        size = self._output_dock.size()
        return size.width(), size.height()

    def resize_document_dock(self, size: Tuple[Optional[int], Optional[int]]):
        width, height = size
        if width:
            self.resizeDocks([self._document_dock], [width], Qt.Horizontal)
        if height:
            self.resizeDocks([self._document_dock], [height], Qt.Vertical)

    def resize_output_dock(self, size: Tuple[Optional[int], Optional[int]]):
        width, height = size
        if width:
            self.resizeDocks([self._output_dock], [width], Qt.Horizontal)
        if height:
            self.resizeDocks([self._output_dock], [height], Qt.Vertical)

    def tabify_docks(self):
        self.tabifyDockWidget(self._document_dock, self._output_dock)

    def set_statusbar_visible(self, visible: bool):
        self.statusBar().setVisible(visible)

    def is_statusbar_visible(self) -> bool:
        return self.statusBar().isVisible()

    def show_statusbar_message(self, message: str, timeout: int = 3000):
        self.statusBar().showMessage(message, timeout)

    def clear_statusbar_message(self):
        self.statusBar().clearMessage()

    def set_execute_button_text(self, text: str):
        self._operation_area.set_execute_button_text(text)

    def set_cancel_button_text(self, text: str):
        self._operation_area.set_cancel_button_text(text)

    def set_clear_button_text(self, text: str):
        self._operation_area.set_clear_button_text(text)

    def set_clear_checkbox_text(self, text: str):
        self._operation_area.set_clear_checkbox_text(text)

    def set_clear_button_visible(self, visible: bool):
        self._operation_area.set_clear_button_visible(visible)

    def set_clear_checkbox_visible(self, visible: bool):
        self._operation_area.set_clear_checkbox_visible(visible)

    def set_clear_checkbox_checked(self, checked: bool):
        self._operation_area.set_clear_checkbox_checked(checked)

    def is_clear_checkbox_checked(self) -> bool:
        return self._operation_area.is_clear_checkbox_checked()

    def is_function_executing(self) -> bool:
        return self._executor.is_executing

    def is_function_cancelable(self) -> bool:
        return self._executor.is_cancelled

    def process_parameter_error(self, e: ParameterError):
        self._parameter_area.process_parameter_error(e)

    def disable_parameter_widgets(self, disabled):
        self._parameter_area.disable_parameter_widgets(disabled)

    def before_execute(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        self._config: FnExecuteWindowConfig
        super().before_execute(fn_info, arguments)
        if self._operation_area.is_clear_checkbox_checked():
            self.clear_output()
        self._operation_area.set_execute_button_enabled(False)
        if self._config.disable_widgets_on_execute:
            self._parameter_area.disable_parameter_widgets(True)
        # self._operation_area.set_clear_button_enabled(False)
        self._operation_area.set_cancel_button_enabled(False)
        self._parameter_area.clear_parameter_error(None)

    def on_execute_start(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_start(fn_info, arguments)
        self._operation_area.set_cancel_button_enabled(True)

    def on_execute_finish(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        self._config: FnExecuteWindowConfig
        super().on_execute_finish(fn_info, arguments)
        self._operation_area.set_execute_button_enabled(True)
        if self._config.disable_widgets_on_execute:
            self._parameter_area.disable_parameter_widgets(False)
        # self._operation_area.set_clear_button_enabled(True)
        self._operation_area.set_cancel_button_enabled(False)

    def on_execute_result(
        self, fn_info: FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        self._config: FnExecuteWindowConfig
        if callable(self._bundle.on_execute_result):
            self._bundle.on_execute_result(result, arguments.copy())
            return

        result_str = self._config.function_result_message.format(result)

        if self._config.print_function_result:
            self.append_output(result_str, scroll_to_bottom=True)

        if self._config.show_function_result:
            messagebox.show_info_message(
                self, result_str, title=self._config.result_dialog_title
            )

    def on_execute_error(
        self, fn_info: FnInfo, arguments: Dict[str, Any], error: Exception
    ):

        self._config: FnExecuteWindowConfig
        if isinstance(error, ParameterError):
            self._parameter_area.process_parameter_error(error)
            del error
            return

        if callable(self._bundle.on_execute_error):
            self._bundle.on_execute_error(error, arguments.copy())
            del error
            return

        error_type = type(error).__name__
        error_msg = self._config.function_error_message.format(error_type, str(error))
        if self._config.print_function_error:
            if not self._config.function_error_traceback:
                self.append_output(error_msg, scroll_to_bottom=True)
            else:
                self.append_output(get_traceback(error) + "\n", scroll_to_bottom=True)

        if self._config.show_function_error:
            if not self._config.function_error_traceback:
                messagebox.show_critical_message(
                    self, error_msg, title=self._config.error_dialog_title
                )
            else:
                messagebox.show_exception_messagebox(
                    self, exception=error, title=self._config.error_dialog_title
                )
        del error

    def _on_close(self) -> bool:
        self._config: FnExecuteWindowConfig
        if self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
            return False
        return super()._on_close()

    def _on_cleanup(self):
        super()._on_cleanup()
        self._parameter_area.clear_parameters()

    def _on_destroy(self):
        super()._on_destroy()
        # noinspection PyProtectedMember
        ucontext._current_window_destroyed()

    def _on_cancel_button_clicked(self):
        self._config: FnExecuteWindowConfig
        if not self._bundle.fn_info.cancelable:
            messagebox.show_warning_message(
                self, self._config.uncancelable_function_message
            )
            return
        if not self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_not_executing_message
            )
        else:
            self._executor.try_cancel()

    def _on_execute_button_clicked(self):
        self._config: FnExecuteWindowConfig
        if self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
            return
        try:
            arguments = self.get_parameter_values()
        # except FunctionExecutingError:
        #     messagebox.show_warning_message(
        #         self, self._config.function_executing_message
        #     )
        except ParameterError as e:
            self._parameter_area.process_parameter_error(e)
        else:
            self._executor.execute(self._bundle.fn_info, arguments)

    # noinspection PyMethodMayBeStatic
    def _on_clear_button_clicked(self):
        # self._config: FnExecuteWindowConfig
        # if self._executor.is_executing:
        #     messagebox.show_warning_message(
        #         self, self._config.function_executing_message
        #     )
        #     pass
        ucontext.clear_output()
