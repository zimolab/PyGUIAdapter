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
    FnExecuteWindowEventListener,
    DockWidgetArea,
    DockWidgetAreas,
)
from ._document_area import DocumentArea
from ._operation_area import OperationArea
from ._output_area import OutputArea, ProgressBarConfig
from ._parameter_area import ParameterArea
from ._progress_dialog import ProgressDialog
from ...adapter import ucontext
from ...adapter import uoutput
from ...bundle import FnBundle
from ...exceptions import (
    ParameterError,
    FunctionNotCancellableError,
    FunctionNotExecutingError,
)
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

        self._progress_dialog: Optional[ProgressDialog] = None

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
                self,
                exception=e,
                message="failed to create parameter widget: ",
                detail=True,
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

        self._document_area.on_parameter_anchor_clicked(self.scroll_to_parameter)
        self._document_area.on_group_anchor_clicked(self.activate_parameter_group)

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
        更新进度条配置

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
        显示进度条

        Returns:
            无返回值
        """
        self._output_area.show_progressbar()

    def hide_progressbar(self) -> None:
        """
        隐藏进度条

        Returns:
            无返回值
        """
        self._output_area.hide_progressbar()
        self._output_area.scroll_to_bottom()

    def update_progress(
        self, current_value: int, message: Optional[str] = None
    ) -> None:
        """
        更新进度条进度

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
        把文本追加到输出浏览器中

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
        清除输出浏览器内容

        Returns:
            无返回值
        """
        self._output_area.clear_output()

    def set_document(
        self, document: str, document_format: Literal["markdown", "html", "plaintext"]
    ) -> None:
        """
        设置函数说明文档

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
        添加一个新的函数参数

        Args:
            parameter_name: 要增加的函数参数名称
            config: 函数参数配置，格式为: (参数控件类, 参数控件配置类实例)

        Returns:
            无返回值

        Raises:
            ParameterError: 当参数为空、参数名称重复时将引发此异常
        """
        self._parameter_area.add_parameter(parameter_name, config)

    def add_parameters(
        self,
        configs: Dict[str, Tuple[Type[BaseParameterWidget], BaseParameterWidgetConfig]],
    ) -> None:
        """
        增加一组新的函数参数

        Args:
            configs: 要增加的函数参数名称及其配置

        Returns:
            无返回值

        Raises:
            ParameterError: 当参数为空、参数名称重复时将引发此异常
        """
        self._parameter_area.add_parameters(configs)

    def remove_parameter(
        self, parameter_name: str, ignore_unknown_parameter: bool = True
    ) -> None:
        """
        移除指定参数控件

        Args:
            parameter_name: 要移除的指定参数名称
            ignore_unknown_parameter: 是否忽略未知参数

        Returns:
            无返回值

        Raises:
            ParameterNotFoundError: 当参数`parameter_name`不存在且`ignore_unknown_parameter`为`False`时，将引发此异常
        """
        self._parameter_area.remove_parameter(
            parameter_name, ignore_unknown_parameter=ignore_unknown_parameter
        )

    def has_parameter(self, parameter_name: str) -> bool:
        """
        判断是否存在指定参数名称

        Args:
            parameter_name: 带判断的参数名称

        Returns:
            存在指定参数时返回`True`，否则返回`False`
        """
        return self._parameter_area.has_parameter(parameter_name)

    def clear_parameters(self) -> None:
        """
        清除所有参数

        Returns:
            无返回值
        """
        self._parameter_area.clear_parameters()

    def get_parameter_value(self, parameter_name: str) -> Any:
        """
        获取指定参数当前值

        Args:
            parameter_name: 参数名称

        Returns:
            返回当前值

        Raises:
            ParameterNotFoundError: 指定参数不存在时，将引发此异常
            ParameterError: 无法从对应控件获取当前值时，将引发此异常

        """
        return self._parameter_area.get_parameter_value(parameter_name)

    def get_parameter_values(self) -> Dict[str, Any]:
        """
        获取所有参数的当前值

        Returns:
            以字典形式返回当前所有参数的值

        Raises:
            ParameterError: 无法从对应控件获取某个参数的当前值时，将引发此异常
        """
        return self._parameter_area.get_parameter_values()

    def get_parameter_values_of(self, group_name: str) -> Dict[str, Any]:
        """
        获取指定分组下所有参数当前值

        Args:
            group_name: 指定分组的名称

        Returns:
            返回指定分组下所有参数的名称和值

        Raises:
            ParameterNotFoundError: 当指定分组不存在时，引发此异常
            ParameterError: 无法从对应控件获取某个参数的当前值时，将引发此异常
        """
        return self._parameter_area.get_parameter_values_of(group_name)

    def set_parameter_value(self, parameter_name: str, value: Any) -> None:
        """
        设置参数当前值

        Args:
            parameter_name: 参数名称
            value: 要设置的值

        Returns:
            无返回值

        Raises:
            ParameterNotFoundError: 若指定参数不存在，则引发此异常
            ParameterError: 若无法将值设置到对应的控件，那么将引发此异常
        """
        self._parameter_area.set_parameter_value(parameter_name, value)

    def set_parameter_values(self, values: Dict[str, Any]) -> None:
        """
        设置多个参数的当前值

        Args:
            values: 要设置的参数名称和值

        Returns:
            无返回值

        Raises:
            ParameterError: 若无法将值设置到对应的控件，那么将引发此异常
        """
        self._parameter_area.clear_parameter_error(None)
        if not values:
            return
        self._parameter_area.set_parameter_values(values)

    def get_parameter_names(self) -> List[str]:
        """
        获取所有参数名称

        Returns:
            返回当前所有参数名称
        """
        return self._parameter_area.get_parameter_names()

    def get_parameter_names_of(self, group_name: str) -> List[str]:
        """
        获取指定分组下的所有参数名称

        Args:
            group_name: 分组名称

        Returns:
            返回指定分组下的所有参数名称

        Raises:
            ParameterNotFoundError: 当指定分组不存在时，引发此异常

        """
        return self._parameter_area.get_parameter_names_of(group_name)

    def set_output_dock_property(
        self,
        *,
        title: Optional[str] = None,
        visible: Optional[bool] = None,
        floating: Optional[bool] = None,
        area: Optional[DockWidgetArea] = None,
    ) -> None:
        """
        设置Output Dock的属性

        Args:
            title: 标题
            visible: 是否显示
            floating: 是否悬浮
            area: 初始停靠区域

        Returns:
            无返回值
        """
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
    ) -> None:
        """
        设置Document Dock的属性

        Args:
            title: 标题
            visible: 是否显示
            floating: 是否悬浮
            area: 初始停靠区域

        Returns:
            无返回值
        """
        if title is not None:
            self.set_document_dock_title(title)
        if visible is not None:
            self.set_document_dock_visible(visible)
        if floating is not None:
            self.set_document_dock_floating(floating)
        if area is not None:
            self.set_document_dock_area(area)

    def set_allowed_dock_areas(self, areas: Optional[DockWidgetAreas]) -> None:
        """
        设置停靠窗口允许停靠的区域

        Args:
            areas: 允许停靠的区域

        Returns:
            无返回值

        """
        if areas is None:
            return
        self._document_dock.setAllowedAreas(areas)
        self._output_dock.setAllowedAreas(areas)

    def set_output_dock_visible(self, visible: bool) -> None:
        """
        设置Output Dock是否显示

        Args:
            visible: 目标状态

        Returns:
            无返回值
        """
        self._output_dock.setVisible(visible)

    def is_output_dock_visible(self) -> bool:
        """
        检查Output Dock是否显示

        Returns:
            返回当前显示状态
        """
        return self._output_dock.isVisible()

    def set_document_dock_visible(self, visible: bool) -> None:
        """
        设置Document Dock是否显示

        Args:
            visible: 目标状态

        Returns:
            无返回值
        """
        self._document_dock.setVisible(visible)

    def is_document_dock_visible(self) -> bool:
        """
        检查Document Dock是否显示

        Returns:
            返回当前显示状态
        """
        return self._document_dock.isVisible()

    def set_document_dock_floating(self, floating: bool) -> None:
        """
        设置Document Dock是否悬浮

        Args:
            floating: 目标状态

        Returns:
            无返回值
        """
        self._document_dock.setFloating(floating)

    def is_document_dock_floating(self) -> bool:
        """
        检查Document Dock是否悬浮

        Returns:
            返回当前悬浮状态
        """
        return self._document_dock.isFloating()

    def set_output_dock_floating(self, floating: bool) -> None:
        """
        设置Output Dock是否悬浮

        Args:
            floating: 目标状态

        Returns:
            无返回值
        """
        self._output_dock.setFloating(floating)

    def is_output_dock_floating(self) -> bool:
        """
        检查Output Dock是否悬浮

        Returns:
            返回当前悬浮状态
        """
        return self._output_dock.isFloating()

    def set_document_dock_title(self, title: str) -> None:
        """
        设置Document Dock标题

        Args:
            title: 标题

        Returns:
            无返回值
        """
        if title is None:
            return
        self._document_dock.setWindowTitle(title)

    def get_document_dock_title(self) -> str:
        """
        获取Document Dock标题

        Returns:
            返回当前标题
        """
        return self._document_dock.windowTitle()

    def get_document_dock_size(self) -> Tuple[int, int]:
        """
        获取Document Dock尺寸

        Returns:
            返回当前尺寸
        """
        size = self._document_dock.size()
        return size.width(), size.height()

    def set_output_dock_title(self, title: str) -> None:
        """
        设置Output Dock标题

        Args:
            title: 标题

        Returns:
            无返回值
        """
        if title is None:
            return
        self._output_dock.setWindowTitle(title)

    def get_output_dock_title(self) -> str:
        """
        获取Output Dock标题

        Returns:
            返回当前标题
        """
        return self._output_dock.windowTitle()

    def set_document_dock_area(self, area: DockWidgetArea) -> None:
        """
        设置Document Dock停靠区域

        Args:
            area: 目标停靠区域

        Returns:
            无返回值

        """
        if not self._document_dock.isAreaAllowed(area):
            messagebox.show_warning_message(self, f"Invalid dock area: {area}")
            return
        self.addDockWidget(area, self._document_dock)

    def get_document_dock_area(self) -> DockWidgetArea:
        """
        获取Document Dock停靠区域

        Returns:
            返回当前停靠区域
        """
        return self.dockWidgetArea(self._document_dock)

    def set_output_dock_area(self, area: DockWidgetArea) -> None:
        """
        设置Output Dock停靠区域

        Args:
            area: 目标停靠区域

        Returns:
            无返回值

        """
        if not self._output_dock.isAreaAllowed(area):
            messagebox.show_warning_message(self, f"Invalid dock area: {area}")
            return
        self.addDockWidget(area, self._output_dock)

    def get_output_dock_area(self) -> DockWidgetArea:
        """
        获取Output Dock停靠区域

        Returns:
            返回当前停靠区域
        """
        return self.dockWidgetArea(self._output_dock)

    def get_output_dock_size(self) -> Tuple[int, int]:
        """
        获取Output Dock尺寸

        Returns:
            返回当前尺寸
        """
        size = self._output_dock.size()
        return size.width(), size.height()

    def resize_document_dock(
        self, size: Tuple[Union[int, float, None], Union[int, float, None]]
    ) -> None:
        """
        调整Document Dock尺寸

        注意：停靠窗口的尺寸受到多种因素的影响，无法保证实际的尺寸与开发者设置的尺寸保持一致，尤其时多个停靠窗口停靠在同一区域时具体而言：

        - 尺寸的调整受最小和最大尺寸的约束；
        - 尺寸调整不会影响主窗口的大小；
        - 在空间有限的情况下，将根据各个停靠窗口的相对大小占比进行可以利用空间的调整

        Args:
            size: 目标尺寸。格式为`(width, height)`，可以只设置其中一个维度，另一个不需要设置的维度置为`None`即可。width和height可以为`int`或`float`, 为`int`时代表width或height的绝对值，为`float`时代表相对于窗口大小的百分比。

        Returns:
            无返回值
        """
        size = self._calc_dock_size(size)
        width, height = size
        if width:
            self.resizeDocks([self._document_dock], [width], Qt.Horizontal)
        if height:
            self.resizeDocks([self._document_dock], [height], Qt.Vertical)

    def resize_output_dock(
        self, size: Tuple[Union[int, float, None], Union[int, float, None]]
    ) -> None:
        """
        调整Output Dock尺寸

        注意：停靠窗口的尺寸受到多种因素的影响，无法保证实际的尺寸与开发者设置的尺寸保持一致，尤其时多个停靠窗口停靠在同一区域时具体而言：

        - 尺寸的调整受最小和最大尺寸的约束；
        - 尺寸调整不会影响主窗口的大小；
        - 在空间有限的情况下，将根据各个停靠窗口的相对大小占比进行可以利用空间的调整

        Args:
            size: 目标尺寸。格式为`(width, height)`，可以只设置其中一个维度，另一个不需要设置的维度置为`None`即可。width和height可以为`int`或`float`, 为`int`时代表width或height的绝对值，为`float`时代表相对于窗口大小的百分比。

        Returns:
            无返回值
        """
        size = self._calc_dock_size(size)
        width, height = size
        if width:
            self.resizeDocks([self._output_dock], [width], Qt.Horizontal)
        if height:
            self.resizeDocks([self._output_dock], [height], Qt.Vertical)

    def tabify_docks(self) -> None:
        """
        使所有Dock窗口选项卡化

        注意：当前已悬浮的窗口不受影响

        Returns:
            无返回值
        """
        self.tabifyDockWidget(self._document_dock, self._output_dock)

    def set_statusbar_visible(self, visible: bool) -> None:
        """
        设置窗口状态栏是否可见

        Args:
            visible: 目标状态

        Returns:
            无返回值
        """
        self.statusBar().setVisible(visible)

    def is_statusbar_visible(self) -> bool:
        """
        检查窗口状态栏是否可见

        Returns:
            返回状态栏当前状态
        """
        return self.statusBar().isVisible()

    def show_statusbar_message(self, message: str, timeout: int = 3000) -> None:
        """
        设置状态栏消息

        Args:
            message: 消息文本
            timeout: 显示的时长

        Returns:
            无返回值
        """
        self.statusBar().showMessage(message, timeout)

    def clear_statusbar_message(self) -> None:
        """
        清除状态栏消息

        Returns:
            无返回值
        """
        self.statusBar().clearMessage()

    def set_execute_button_text(self, text: str) -> None:
        """
        设置执行按钮文本

        Args:
            text: 目标文本

        Returns:
            无返回值
        """
        self._operation_area.set_execute_button_text(text)

    def set_cancel_button_text(self, text: str) -> None:
        """
        设置取消按钮文本

        Args:
            text: 目标文本

        Returns:
            无返回值
        """
        self._operation_area.set_cancel_button_text(text)

    def set_clear_button_text(self, text: str) -> None:
        """
        设置清除按钮文本

        Args:
            text: 目标文本

        Returns:
            无返回值
        """
        self._operation_area.set_clear_button_text(text)

    def set_clear_checkbox_text(self, text: str) -> None:
        """
        设置清除选项框文本

        Args:
            text: 目标文本

        Returns:
            无返回值
        """
        self._operation_area.set_clear_checkbox_text(text)

    def set_clear_button_visible(self, visible: bool) -> None:
        """
        设置清除按钮是否可见

        Args:
            visible: 目标状态

        Returns:
            无返回值
        """
        self._operation_area.set_clear_button_visible(visible)

    def set_clear_checkbox_visible(self, visible: bool) -> None:
        """
        设置清除选项框是否可见

        Args:
            visible: 目标状态

        Returns:
            无返回值
        """
        self._operation_area.set_clear_checkbox_visible(visible)

    def set_clear_checkbox_checked(self, checked: bool) -> None:
        """
        设置清除选项框是否选中

        Args:
            checked: 目标状态

        Returns:
            无返回值
        """
        self._operation_area.set_clear_checkbox_checked(checked)

    def is_clear_checkbox_checked(self) -> bool:
        """
        检查清除选项框是否选中

        Returns:
            返回当前状态
        """
        return self._operation_area.is_clear_checkbox_checked()

    def is_function_executing(self) -> bool:
        """
        检查函数是否正在运行

        Returns:
            返回函数运行状态
        """
        return self._executor.is_executing

    def is_function_cancelable(self) -> bool:
        """
        检查函数是否为可取消函数

        Returns:
            返回函数是否可取消
        """
        return self._executor.is_cancelled

    def process_parameter_error(self, e: ParameterError) -> None:
        """
        使用内置逻辑处理ParameterError类型的异常

        Args:
            e: 异常对象

        Returns:
            无返回值
        """
        self._parameter_area.process_parameter_error(e)

    def disable_parameter_widgets(self, disabled: bool) -> None:
        """
        设置参数控件禁用/启用状态

        Args:
            disabled: 是否禁用

        Returns:
            无返回值
        """
        self._parameter_area.disable_parameter_widgets(disabled)

    def try_cancel_execution(self) -> None:
        """
        尝试取消函数执行

        Returns:
            无返回值

        Raises:
            FunctionNotCancellableError: 函数未被设置为可取消函数时，将引发此异常
            FunctionNotExecutingError: 函数未处于正在执行中时，将引发此异常
        """
        self._config: FnExecuteWindowConfig
        if not self._bundle.fn_info.cancelable:
            raise FunctionNotCancellableError()
        if not self._executor.is_executing:
            raise FunctionNotExecutingError()
        else:
            self._executor.try_cancel()

    def activate_parameter_group(self, group_name: str) -> None:
        """
        激活展开指定参数分组。

        Args:
            group_name: 参数分组名称

        Returns:
            无返回值
        """
        if group_name == "":
            group_name = None
        self._parameter_area.activate_parameter_group(group_name)

    def show_progress_dialog(self, config: Dict[str, Any]) -> None:
        self._config: FnExecuteWindowConfig
        self.dismiss_progress_dialog()
        self._progress_dialog = ProgressDialog(
            self,
            cancellable=self._bundle.fn_info.cancelable,
            cancel_button_text=self._config.cancel_button_text,
            **config,
        )
        self._progress_dialog.sig_cancel_requested.connect(
            self._on_cancel_button_clicked
        )
        self._progress_dialog.show()

    def dismiss_progress_dialog(self) -> None:
        if self._progress_dialog is not None:
            self._progress_dialog.sig_cancel_requested.disconnect(
                self._on_cancel_button_clicked
            )
            self._progress_dialog.close()
            self._progress_dialog.deleteLater()
            self._progress_dialog = None

    def update_progress_dialog(self, progress: int, info: str) -> None:
        if self._progress_dialog is None:
            return
        self._progress_dialog.sig_update_progress.emit(progress, info)

    def scroll_to_parameter(
        self,
        parameter_name: str,
        x: int = 50,
        y: int = 50,
        highlight_effect: bool = True,
    ):
        """
        滚动到指定参数的位置。

        Args:
            parameter_name: 参数名称
            x: 滚动的X坐标偏移值
            y: 滚动的Y坐标偏移值
            highlight_effect: 是否对指定控件显示高亮效果

        Returns:
            无返回值
        """
        self._parameter_area.scroll_to_parameter(parameter_name, x, y, highlight_effect)

    def before_execute(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        self._config: FnExecuteWindowConfig
        super().before_execute(fn_info, arguments)
        if self._operation_area.is_clear_checkbox_checked():
            self.clear_output()
        self._operation_area.set_execute_button_enabled(False)
        if self._config.disable_widgets_on_execute:
            self._parameter_area.disable_parameter_widgets(True)
        self._operation_area.set_cancel_button_enabled(False)
        self._parameter_area.clear_parameter_error(None)
        self.dismiss_progress_dialog()

    def on_execute_start(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        super().on_execute_start(fn_info, arguments)
        self._operation_area.set_cancel_button_enabled(True)
        if isinstance(self._bundle.window_listener, FnExecuteWindowEventListener):
            self._bundle.window_listener.on_execute_start(self)

    def on_execute_finish(self, fn_info: FnInfo, arguments: Dict[str, Any]) -> None:
        self._config: FnExecuteWindowConfig
        super().on_execute_finish(fn_info, arguments)
        self._operation_area.set_execute_button_enabled(True)
        if self._config.disable_widgets_on_execute:
            self._parameter_area.disable_parameter_widgets(False)
        self._operation_area.set_cancel_button_enabled(False)

        self.dismiss_progress_dialog()

        if isinstance(self._bundle.window_listener, FnExecuteWindowEventListener):
            self._bundle.window_listener.on_execute_finish(self)

    def on_execute_result(
        self, fn_info: FnInfo, arguments: Dict[str, Any], result: Any
    ) -> None:
        self._config: FnExecuteWindowConfig
        # if callable(self._bundle.on_execute_result):
        #     self._bundle.on_execute_result(result, arguments.copy())
        #     return
        if isinstance(self._bundle.window_listener, FnExecuteWindowEventListener):
            should_continue = self._bundle.window_listener.on_execute_result(
                self, result
            )
            if not should_continue:
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

        if isinstance(self._bundle.window_listener, FnExecuteWindowEventListener):
            should_continue = self._bundle.window_listener.on_execute_error(self, error)
            if not should_continue:
                del error
                return

        if isinstance(error, ParameterError):
            self._parameter_area.process_parameter_error(error)
            del error
            return

        # if callable(self._bundle.on_execute_error):
        #     self._bundle.on_execute_error(error, arguments.copy())
        #     del error
        #     return

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
        self.dismiss_progress_dialog()

    def _on_destroy(self):
        super()._on_destroy()
        # noinspection PyProtectedMember
        ucontext._current_window_destroyed()

    def _on_cancel_button_clicked(self):
        self._config: FnExecuteWindowConfig
        try:
            self.try_cancel_execution()
        except FunctionNotCancellableError:
            messagebox.show_warning_message(
                self, self._config.uncancelable_function_message
            )
        except FunctionNotExecutingError:
            messagebox.show_warning_message(
                self, self._config.function_not_executing_message
            )

    def _on_execute_button_clicked(self):
        self._config: FnExecuteWindowConfig
        if self._executor.is_executing:
            messagebox.show_warning_message(
                self, self._config.function_executing_message
            )
            return
        try:
            arguments = self.get_parameter_values()
        except ParameterError as e:
            self._parameter_area.process_parameter_error(e)
        else:
            self._executor.execute(self._bundle.fn_info, arguments)

    # noinspection PyMethodMayBeStatic
    def _on_clear_button_clicked(self):
        uoutput.clear_output()

    def _calc_dock_size(
        self, size: Tuple[Union[int, float, None], Union[int, float, None]]
    ) -> Tuple[Optional[int], Optional[int]]:
        width, height = size
        win_width = self.width()
        win_height = self.height()

        calc = [None, None]

        if isinstance(width, int):
            calc[0] = min(width, win_width)
        elif isinstance(width, float):
            calc[0] = min(int(win_width * width), win_width)
        else:
            calc[0] = None

        if isinstance(height, int):
            calc[1] = min(height, win_height)
        elif isinstance(height, float):
            calc[1] = min(int(win_height * height), win_height)
        else:
            calc[1] = None

        return calc[0], calc[1]
