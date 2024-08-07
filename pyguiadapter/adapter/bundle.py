import dataclasses
from typing import Any, Optional, Dict, NoReturn, Callable, List

from function2widgets import FunctionInfo, CommonParameterWidgetArgs

from pyguiadapter.commons import T, DocumentFormat, safe_del, get_function_parser
from pyguiadapter.progressbar_config import ProgressBarConfig
from pyguiadapter.ui.menus import ActionItem

from .constants import (
    DEFAULT_ICON,
    CANCEL_EVENT_PARAM_NAME,
    _KEY_WIDGET_ARGS,
    _KEY_PARAM_NAME,
)


class FunctionBundle(object):
    def __init__(
        self,
        func_obj: callable,
        bind: Optional[T] = None,
        display_name: Optional[str] = None,
        display_icon: Optional[str] = None,
        display_document: Optional[str] = None,
        document_format: Optional[DocumentFormat] = DocumentFormat.PLAIN,
        widgets_configs: Optional[Dict[str, dict]] = None,
        cancelable=False,
        cancel_event_param_name: Optional[str] = CANCEL_EVENT_PARAM_NAME,
        menus: Optional[Dict[str, dict]] = None,
        toolbar_actions: Optional[List[ActionItem]] = None,
        window_title: Optional[str] = None,
        window_icon: Optional[str] = None,
        goto_document_start: bool = False,
        enable_progressbar: bool = False,
        progressbar_config: Optional[ProgressBarConfig] = None,
    ):
        self._func_obj = func_obj
        self._bind = bind
        self._display_name = display_name
        self._display_icon = display_icon
        self._display_document = display_document
        self._document_format = document_format
        self._cancelable = cancelable
        self._cancel_event_param_name = (
            cancel_event_param_name or CANCEL_EVENT_PARAM_NAME
        )
        self._menus = menus
        self._toolbar_actions = toolbar_actions
        self._window_title = window_title
        self._window_icon = window_icon
        self._goto_document_start = goto_document_start is True
        self._enable_progressbar = enable_progressbar
        self._progressbar_config = progressbar_config

        func_info = get_function_parser().parse(
            func_obj=func_obj, ignore_self_param=True
        )

        if cancelable:
            func_info = self._handle_cancelable_func(func_info)

        self._func_info = func_info

        if widgets_configs:
            self.apply_widget_configs(widgets_configs)

    @property
    def func_obj(self) -> Callable:
        return self._func_obj

    @property
    def func_info(self) -> FunctionInfo:
        return self._func_info

    @property
    def bind(self) -> Optional[T]:
        return self._bind

    @property
    def display_name(self) -> str:
        return self._display_name or self._func_info.name

    @property
    def display_icon(self) -> str:
        return self._display_icon or DEFAULT_ICON

    @property
    def display_document(self) -> str:
        return self._display_document or self._func_info.description

    @property
    def document_format(self) -> DocumentFormat:
        return self._document_format

    @property
    def cancelable(self) -> bool:
        return self._cancelable

    @property
    def cancel_event_param_name(self) -> str:
        return self._cancel_event_param_name or CANCEL_EVENT_PARAM_NAME

    @property
    def menus(self) -> Optional[Dict[str, dict]]:
        return self._menus

    @property
    def toolbar_actions(self) -> Optional[List[ActionItem]]:
        return self._toolbar_actions

    @property
    def window_title(self) -> Optional[str]:
        return self._window_title

    @property
    def window_icon(self) -> Optional[str]:
        return self._window_icon

    @property
    def goto_document_start(self) -> bool:
        return self._goto_document_start

    @property
    def enable_progressbar(self) -> bool:
        return self._enable_progressbar

    @property
    def progressbar_config(self) -> ProgressBarConfig:
        return self._progressbar_config

    def execute_function(self, *args, **kwargs) -> Any:
        if self._bind is None:
            return self._func_obj(*args, **kwargs)
        return self._func_obj(self._bind, *args, **kwargs)

    def apply_widget_configs(self, widget_configs: Dict[str, dict]) -> NoReturn:
        if not widget_configs:
            return
        for parameter_info in self.func_info.parameters:
            param_name = parameter_info.name
            if param_name not in widget_configs:
                continue

            widget_config = widget_configs[param_name]
            if not isinstance(widget_config, dict):
                continue

            widget_info = parameter_info.widget
            if widget_info is None:
                continue

            if _KEY_WIDGET_ARGS in widget_config:
                widget_args = widget_config[_KEY_WIDGET_ARGS]
                safe_del(widget_config, _KEY_WIDGET_ARGS)
                # 'widget_args' in widget_configs must be an instance of CommonParameterWidgetArgs
                assert isinstance(widget_args, CommonParameterWidgetArgs)
                widget_args_dict = dataclasses.asdict(widget_args)
                safe_del(widget_args_dict, _KEY_PARAM_NAME)
                widget_config.update(widget_args_dict)
            widget_info.update_with_flattened_dict(widget_config)

    def _handle_cancelable_func(self, func_info: FunctionInfo) -> FunctionInfo:
        params = func_info.parameters
        cancel_event_param = None
        for param_info in params:
            if param_info.name == self.cancel_event_param_name:
                cancel_event_param = param_info
                break
        if cancel_event_param is None:
            raise RuntimeError(
                f"a cancelable function must provide a keyword parameter named '{self._cancel_event_param_name}'"
            )
        else:
            params.remove(cancel_event_param)
        return func_info

    def __repr__(self):
        return f"<FunctionBundle function={self.func_obj} bind={self.bind}>"
