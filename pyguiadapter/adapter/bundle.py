from typing import Any, Optional, Dict

from function2widgets.info import FunctionInfo

from pyguiadapter import commons
from pyguiadapter.commons import T, DocumentFormat

DEFAULT_ICON = "puzzle"


class FunctionBundle(object):

    def __init__(
        self,
        function: callable,
        bind: Optional[T] = None,
        display_name: Optional[str] = None,
        display_icon: Optional[str] = None,
        display_document: Optional[str] = None,
        document_format: Optional[DocumentFormat] = DocumentFormat.PLAIN,
        widgets_configs: Optional[Dict[str, dict]] = None,
    ):
        self._function = function
        self._bind = bind
        self._display_name = display_name
        self._display_icon = display_icon
        self._display_document = display_document
        self._document_format = document_format

        self._function_info = commons.get_function_parser().parse(
            func_obj=function,
            ignore_self_param=True,
        )

        if widgets_configs:
            self.apply_widget_configs(widgets_configs)

    @property
    def function(self) -> callable:
        return self._function

    @property
    def function_info(self) -> FunctionInfo:
        return self._function_info

    @property
    def bind(self) -> Optional[T]:
        return self._bind

    @property
    def display_name(self) -> str:
        return self._display_name or self._function_info.name

    @property
    def display_icon(self) -> str:
        return self._display_icon or DEFAULT_ICON

    @property
    def display_document(self) -> str:
        return self._display_document or self._function_info.description

    @property
    def document_format(self) -> DocumentFormat:
        return self._document_format

    def execute(self, *args, **kwargs) -> Any:
        if self._bind is None:
            return self._function(*args, **kwargs)
        return self._function(self._bind, *args, **kwargs)

    def apply_widget_configs(self, widget_configs: Dict[str, dict]):
        if not widget_configs:
            return
        for parameter_info in self.function_info.parameters:
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
        return f"<FunctionBundle function={self.function} bind={self.bind}>"
