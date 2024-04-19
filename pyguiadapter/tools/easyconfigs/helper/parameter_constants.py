from typing import Any

from function2widgets import FunctionInfo

from pyguiadapter.tools.easyconfigs.helper.const_name_value import ConstNameValueHelper
from pyguiadapter.tools.easyconfigs.structures import _ParameterConstants


class ParameterConstantsHelper(object):

    def __init__(
        self, func_info: FunctionInfo, const_name_value_helper: ConstNameValueHelper
    ):
        self._const_name_value_helper = const_name_value_helper
        self._func_info = func_info

    def make_constants(self) -> _ParameterConstants:
        func_name_literal = self._const_name_value_helper.make_tr_str_literal(
            self._func_info.name
        )
        func_description_literal = self._const_name_value_helper.make_tr_str_literal(
            self._func_info.description
        )
        constants = _ParameterConstants(
            func_name=func_name_literal, func_description=func_description_literal
        )

        for param_info in self._func_info.parameters:
            param_name = param_info.name
            param_description = param_info.description.strip()
            param_default_value = param_info.default
            self._add_param_label(constants, param_name)
            self._add_param_description(constants, param_name, param_description)
            self._add_param_default_value(constants, param_name, param_default_value)
            self._add_param_default_value_description(constants, param_name)

        return constants

    def _add_param_label(self, constants: _ParameterConstants, param_name: str):
        constname = self._const_name_value_helper.constname_param_label(param_name)
        constvalue = self._const_name_value_helper.constvalue_param_label(param_name)
        constants.param_labels[constname] = constvalue

    def _add_param_description(
        self, constants: _ParameterConstants, param_name: str, param_desc: str
    ):
        constname = self._const_name_value_helper.constname_param_description(
            param_name
        )
        constvalue = self._const_name_value_helper.constvalue_param_description(
            param_desc
        )
        constants.param_descriptions[constname] = constvalue

    def _add_param_default_value_description(
        self, constants: _ParameterConstants, param_name: str
    ):
        constname = (
            self._const_name_value_helper.constname_param_default_value_description(
                param_name
            )
        )
        constants.param_default_value_descriptions[constname] = (
            self._const_name_value_helper.constvalue_param_default_value_description()
        )

    def _add_param_default_value(
        self, constants: _ParameterConstants, param_name: str, raw_value: Any
    ):
        constname = self._const_name_value_helper.constname_param_default_value(
            param_name
        )
        default_value_literal = self._const_name_value_helper.try_make_literal(
            raw_value
        )
        constants.param_default_values[constname] = default_value_literal
