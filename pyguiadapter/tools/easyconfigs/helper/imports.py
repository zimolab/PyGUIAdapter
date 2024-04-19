import inspect
from typing import Tuple, Type, List
from function2widgets import FunctionInfo
from pyguiadapter.tools.easyconfigs.structures import _ParamWidgetConfig, _Imports


class ImportsHelper(object):
    def __init__(
        self, param_widget_short_import: str, extra_types_to_import: Tuple[Type]
    ):
        self._param_widget_short_import = param_widget_short_import
        self._extra_types_to_import = extra_types_to_import

        self._ignored_types = (
            int,
            float,
            str,
            bool,
            list,
            tuple,
            dict,
            set,
            frozenset,
            bytes,
            bytearray,
            type(None),
        )

    def make_imports(
        self, func_info: FunctionInfo, param_widget_configs: List[_ParamWidgetConfig]
    ) -> _Imports:
        imports = _Imports()
        self._add_param_const_imports(imports, func_info)
        self._add_param_widget_imports(imports, param_widget_configs)
        self._add_extra_types_imports(imports)
        return imports

    def _add_param_const_imports(self, target: _Imports, func_info: FunctionInfo):
        for param_info in func_info.parameters:
            default_value = param_info.default
            if default_value is inspect.Parameter.empty:
                default_value = None
            default_value_type = type(default_value)
            if default_value_type in self._ignored_types:
                continue
            import_statement = self._get_import_statement(default_value_type, False)
            if import_statement not in target.param_const_imports:
                target.param_const_imports.append(import_statement)

    def _add_param_widget_imports(
        self, target: _Imports, param_widget_configs: List[_ParamWidgetConfig]
    ):
        for param_widget_config in param_widget_configs:
            widget_class = param_widget_config.widget_class
            widget_args_class = param_widget_config.widget_args_class
            widget_class_import_statement = self._get_import_statement(
                widget_class, True
            )
            widget_args_class_import_statement = self._get_import_statement(
                widget_args_class, True
            )
            if widget_class_import_statement not in target.param_widget_imports:
                target.param_widget_imports.append(widget_class_import_statement)
            if widget_args_class_import_statement not in target.param_widget_imports:
                target.param_widget_imports.append(widget_args_class_import_statement)

    def _add_extra_types_imports(self, target: _Imports):
        for extra_type in self._extra_types_to_import:
            import_statement = self._get_import_statement(extra_type, False)
            if import_statement not in target.other_imports:
                target.other_imports.append(import_statement)

    def _get_import_statement(self, clazz: type, try_short_import: bool = True) -> str:
        if try_short_import and self._param_widget_short_import:
            return self._param_widget_short_import.format(clazz.__name__)
        return f"from {clazz.__module__} import {clazz.__name__}"
