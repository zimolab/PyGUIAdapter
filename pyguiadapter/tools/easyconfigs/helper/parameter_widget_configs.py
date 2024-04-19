from typing import List

from function2widgets import ParameterWidgetFactory, FunctionInfo

from pyguiadapter import AS_IS
from pyguiadapter.tools.easyconfigs.helper.const_name_value import ConstNameValueHelper
from pyguiadapter.tools.easyconfigs.structures import _ParamWidgetConfig


class ParameterWidgetConfigsHelper(object):

    def __init__(
        self,
        parameter_widget_factory: ParameterWidgetFactory,
        const_name_value_helper: ConstNameValueHelper,
    ):
        self._factory = parameter_widget_factory
        self._const_name_value_helper = const_name_value_helper

        self._common_widget_args_fields = {
            "parameter_name": self._const_name_value_helper.make_str_literal(AS_IS),
            "label": self._const_name_value_helper.constname_param_label,
            "description": self._const_name_value_helper.constname_param_description,
            "default": self._const_name_value_helper.constname_param_default_value,
            "default_value_description": self._const_name_value_helper.constname_param_default_value_description,
        }

    def make_configs(self, func_info: FunctionInfo) -> List[_ParamWidgetConfig]:
        param_widget_configs = []

        for param_info in func_info.parameters:
            param_widget_info = param_info.widget
            if param_widget_info is None:
                continue
            widget_class = self._factory.get_widget_class(
                param_widget_info.widget_class
            )
            widget_args_class = widget_class.widget_args_class()
            param_widget_config = _ParamWidgetConfig(
                parameter_name=param_info.name,
                widget_class=widget_class,
                widget_args_class=widget_args_class,
            )
            self._add_param_widget_args_fields(param_widget_config)

            param_widget_configs.append(param_widget_config)

        return param_widget_configs

    def _add_param_widget_args_fields(self, param_widget_config: _ParamWidgetConfig):
        self._add_common_widget_args_fields(param_widget_config)

    def _add_common_widget_args_fields(self, param_widget_config: _ParamWidgetConfig):
        for field_name, field_value in self._common_widget_args_fields.items():
            if callable(field_value):
                field_value = field_value(param_widget_config.parameter_name)
            param_widget_config.widget_args_fields[field_name] = field_value
