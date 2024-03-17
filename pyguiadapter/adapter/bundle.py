from typing import Any

from function2widgets.description import FunctionDescription

from pyguiadapter import commons
from pyguiadapter.commons import T, DocumentFormat

DEFAULT_ICON = "puzzle"


class FunctionBundle(object):

    def __init__(
        self,
        function: callable,
        bind: T | None = None,
        display_name: str | None = None,
        display_icon: str | None = None,
        display_document: str | None = None,
        document_format: DocumentFormat | None = DocumentFormat.PLAIN,
        widgets_configs: dict[str, dict] | None = None,
    ):
        self._function = function
        self._bind = bind
        self._display_name = display_name
        self._display_icon = display_icon
        self._display_document = display_document
        self._document_format = document_format

        self._function_description = commons.get_function_parser().parse(
            func=function, parse_class=False, ignore_self_param=True
        )

        if widgets_configs:
            self.apply_widgets_config(widgets_configs)

    @property
    def function(self) -> callable:
        return self._function

    @property
    def function_description(self) -> FunctionDescription:
        return self._function_description

    @property
    def bind(self) -> T | None:
        return self._bind

    @property
    def display_name(self) -> str:
        return self._display_name or self._function_description.name

    @property
    def display_icon(self) -> str:
        return self._display_icon or DEFAULT_ICON

    @property
    def display_document(self) -> str:
        return self._display_document or self._function_description.docstring

    @property
    def document_format(self) -> DocumentFormat:
        return self._document_format

    def execute(self, *args, **kwargs) -> Any:
        if self._bind is None:
            return self._function(*args, **kwargs)
        return self._function(self._bind, *args, **kwargs)

    def apply_widgets_config(self, widgets_config: dict[str, dict]):
        if not widgets_config:
            return
        for parameter_description in self.function_description.parameters:
            name = parameter_description.name
            if name not in widgets_config:
                continue

            widget_config = widgets_config[name]
            if not isinstance(widget_config, dict):
                continue

            widget_description = parameter_description.widget
            if widget_description is None:
                continue

            widget_description.update_with_flattened_dict(widget_config)

    def __repr__(self):
        return f"<FunctionBundle function={self.function} bind={self.bind}>"
