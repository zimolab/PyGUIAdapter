import dataclasses
from typing import Type, Dict, List

from function2widgets import BaseParameterWidget, BaseWidgetArgs


@dataclasses.dataclass
class _ParameterConstants(object):
    func_name: str
    func_description: str
    param_labels: dict = dataclasses.field(default_factory=dict)
    param_descriptions: dict = dataclasses.field(default_factory=dict)
    param_default_value_descriptions: dict = dataclasses.field(default_factory=dict)
    param_default_values: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class _ParamWidgetConfig(object):
    parameter_name: str
    widget_class: Type[BaseParameterWidget]
    widget_args_class: Type[BaseWidgetArgs]
    widget_args_fields: Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class _Imports(object):
    param_widget_imports: List[str] = dataclasses.field(default_factory=list)
    param_const_imports: List[str] = dataclasses.field(default_factory=list)
    other_imports: List[str] = dataclasses.field(default_factory=list)
