from typing import Any, Optional, Dict, NoReturn

from function2widgets.info import FunctionInfo

from pyguiadapter import commons
from pyguiadapter.commons import T, DocumentFormat

DEFAULT_ICON = "puzzle"


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
    ):
        self._func_obj = func_obj
        self._bind = bind
        self._display_name = display_name
        self._display_icon = display_icon
        self._display_document = display_document
        self._document_format = document_format

        self._func_info = commons.get_function_parser().parse(
            func_obj=func_obj,
            ignore_self_param=True,
        )

        if widgets_configs:
            self.apply_widget_configs(widgets_configs)

    @property
    def func_obj(self) -> callable:
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

    def execute_function(self, *args, **kwargs) -> Any:
        if self._bind is None:
            return self._func_obj(*args, **kwargs)
        return self._func_obj(self._bind, *args, **kwargs)

    def apply_widget_configs(self, widget_configs: Dict[str, dict]) -> NoReturn:
        if not widget_configs:
            return
        for parameter_info in self.func_info.parameters:
            name = parameter_info.name
            if name not in widget_configs:
                continue

            widget_config = widget_configs[name]
            if not isinstance(widget_config, dict):
                continue

            widget_info = parameter_info.widget
            if widget_info is None:
                continue

            widget_info.update_with_flattened_dict(widget_config)

    def __repr__(self):
        return f"<FunctionBundle function={self.func_obj} bind={self.bind}>"
