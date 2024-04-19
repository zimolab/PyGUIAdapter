import dataclasses
from typing import Type, Dict, List

from function2widgets import BaseParameterWidget, BaseWidgetArgs


@dataclasses.dataclass
class _Constants(object):
    func_name: str
    func_description: str
    param_labels: dict = dataclasses.field(default_factory=dict)
    param_descriptions: dict = dataclasses.field(default_factory=dict)
    param_default_value_descriptions: dict = dataclasses.field(default_factory=dict)
    param_default_values: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class _ParamWidgetInfo(object):
    widget_class: Type[BaseParameterWidget]
    widget_args_class: Type[BaseWidgetArgs]


@dataclasses.dataclass
class _FuncConfigs(object):
    param_widget_infos: Dict[str, _ParamWidgetInfo] = dataclasses.field(
        default_factory=dict
    )
    widget_imports: List[str] = dataclasses.field(default_factory=list)
    other_imports: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class _ParamWidgetConfig(object):
    parameter_name: str
    widget_class_name: str
    widget_args_class_name: str
    widget_args_fields: Dict[str, str] = dataclasses.field(default_factory=dict)
