import os.path
from datetime import datetime, date, time
from typing import Callable, Iterable

from PyQt6.QtCore import QDateTime, QDate, QTime
from PyQt6.QtGui import QColor
from function2widgets import (
    FunctionInfoParser,
    ParameterWidgetFactory,
    FunctionInfo,
    Color,
    ParameterInfo,
)
from mako.template import Template

from pyguiadapter import get_function_parser, get_param_widget_factory, AS_IS
from .constants import *
from .helpers import ConstNameValueHelper, ConstantsHelper
from .structures import _Constants, _ParamWidgetInfo, _FuncConfigs, _ParamWidgetConfig
from .utils import get_constants_tpl_file, write_text_blocks, get_configs_tpl_file


class FuncConfigsGenerator(object):
    def __init__(
        self,
        func_info_parser: FunctionInfoParser = None,
        param_widget_factory: ParameterWidgetFactory = None,
        str_quote: str = DEFAULT_QUOTE,
        param_label_prefix: str = PARAM_LABEL_PREFIX,
        param_description_prefix: str = PARAM_DESC_PREFIX,
        param_default_value_description_prefix: str = PARAM_DEFAULT_VALUE_DESC_PREFIX,
        param_default_value_prefix: str = PARAM_DEFAULT_VALUE_PREFIX,
        default_value_description_text: str = DEFAULT_VALUE_DESC,
        tr_function: str = DEFAULT_TR_FUNCTION,
        short_import: str = SHORT_IMPORT,
        extra_imports: tuple = EXTRA_IMPORTS,
        configs_varname: str = DEFAULT_CONFIGS_VARNAME,
    ):
        if str_quote != '"' and str_quote != "'":
            raise ValueError("str_quote must be ' or \"")

        self._const_name_value_helper = ConstNameValueHelper(
            str_quote=str_quote,
            param_label_prefix=param_label_prefix,
            param_description_prefix=param_description_prefix,
            param_default_value_description_prefix=param_default_value_description_prefix,
            param_default_value_prefix=param_default_value_prefix,
            default_value_description_text=default_value_description_text,
            tr_function=tr_function,
        )

        self._short_import = short_import
        self._extra_imports = extra_imports

        self._configs_varname = configs_varname

        self._parser = func_info_parser or get_function_parser()
        self._factory = param_widget_factory or get_param_widget_factory()

        self._common_widget_args_fields = {
            "parameter_name": self._const_name_value_helper.make_str_literal(AS_IS),
            "label": self._const_name_value_helper.constname_param_label,
            "description": self._const_name_value_helper.constname_param_description,
            "default": self._const_name_value_helper.constname_param_default_value,
            "default_value_description": self._const_name_value_helper.constname_param_default_value_description,
        }

    def generate_configs_file(
        self,
        func: Callable,
        dest_dir: str = DEFAULT_DEST_DIR,
        filename: str = DEFAULT_CONFIGS_FILENAME,
        onefile: bool = False,
        constants_filename: str = DEFAULT_CONSTANTS_FILENAME,
    ):
        if not onefile and not constants_filename:
            raise ValueError(
                "constants_filename must be specified when onefile is False"
            )

        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        configs_filepath = os.path.join(dest_dir, filename)
        if os.path.isfile(configs_filepath):
            raise ValueError(f"configs file '{configs_filepath}' already exists")

        if not onefile:
            constants_filepath = os.path.join(dest_dir, constants_filename)
            if os.path.isfile(constants_filepath):
                raise ValueError(
                    f"constants file '{constants_filepath}' already exists"
                )
        else:
            constants_filepath = None

        func_info = self._parser.parse(func, ignore_self_param=True)

        constants_helper = ConstantsHelper(func_info, self._const_name_value_helper)
        constants = constants_helper.make_constants()

        func_configs = self._generate_func_configs(func_info)

        for extra_import in self._extra_imports:
            self._add_other_import(func_configs, extra_import)

        widget_imports_code = self._generate_imports_code(func_configs.widget_imports)
        other_imports_code = self._generate_imports_code(func_configs.other_imports)
        constants_code = self._generate_constants_code(constants)
        configs_code = self._generate_configs_code(
            configs_varname=self._configs_varname, configs=func_configs
        )

        if constants_filepath is not None:
            # write constants file
            constants_blocks = (other_imports_code, "\n", constants_code)
            write_text_blocks(constants_filepath, *constants_blocks)

            # write configs file
            constants_module_name = os.path.splitext(constants_filename)[0]
            constants_import = f"from .{constants_module_name} import *"
            configs_blocks = (
                widget_imports_code,
                "\n",
                constants_import,
                configs_code,
            )
            write_text_blocks(configs_filepath, *configs_blocks)
        else:
            # write configs file
            configs_blocks = (
                widget_imports_code,
                "\n",
                other_imports_code,
                "\n",
                constants_code,
                configs_code,
            )
            write_text_blocks(configs_filepath, *configs_blocks)

    def _generate_func_configs(self, func_info: FunctionInfo) -> _FuncConfigs:

        func_configs = _FuncConfigs()

        for param_info in func_info.parameters:
            self._add_param_widget_config(func_configs, param_info)
            param_default_value = param_info.default
            if isinstance(
                param_default_value,
                (Color, QColor, date, time, datetime, QDate, QTime, QDateTime),
            ):
                self._add_other_import(func_configs, param_default_value.__class__)

        return func_configs

    def _add_param_widget_config(
        self, func_configs: _FuncConfigs, param_info: ParameterInfo
    ):
        param_widget_info = param_info.widget
        widget_class = self._factory.get_widget_class(param_widget_info.widget_class)
        widget_args_class = widget_class.widget_args_class()
        param_widget_config = _ParamWidgetInfo(
            widget_class=widget_class, widget_args_class=widget_args_class
        )
        func_configs.param_widget_infos[param_info.name] = param_widget_config
        self._add_widget_import(func_configs, widget_class, try_short_import=True)
        self._add_widget_import(func_configs, widget_args_class, try_short_import=True)

    def _add_widget_import(
        self, func_configs: _FuncConfigs, clazz: type, try_short_import: bool = False
    ):
        clazz_import = self._get_import(clazz, try_short_import)
        if clazz_import not in func_configs.widget_imports:
            func_configs.widget_imports.append(clazz_import)

    def _add_other_import(self, func_configs: _FuncConfigs, clazz: type):
        clazz_import = self._get_import(clazz, False)
        if clazz_import not in func_configs.other_imports:
            func_configs.other_imports.append(clazz_import)

    def _get_import(self, clazz: type, try_short_import: bool = True) -> str:
        if try_short_import and self._short_import:
            return self._short_import.format(clazz.__name__)
        return f"from {clazz.__module__} import {clazz.__name__}"

    @staticmethod
    def _generate_imports_code(imports: Iterable[str]) -> str:
        return "\n".join(imports)

    @staticmethod
    def _generate_constants_code(constants: _Constants) -> str:
        with open(get_constants_tpl_file(), "r", encoding="utf-8") as tpl_file:
            tpl_text = tpl_file.read()
            template = Template(tpl_text)
            func_constants = {
                "FUNC_NAME": constants.func_name,
                "FUNC_DESC": constants.func_description,
            }
            constants_code = template.render(
                func_constants=func_constants,
                param_labels=constants.param_labels,
                param_descs=constants.param_descriptions,
                param_default_value_descs=constants.param_default_value_descriptions,
                param_default_values=constants.param_default_values,
            )
            return constants_code

    def _generate_configs_code(
        self, configs_varname: str, configs: _FuncConfigs
    ) -> str:
        with open(get_configs_tpl_file(), "r", encoding="utf-8") as tpl_file:
            tpl_text = tpl_file.read()
            template = Template(tpl_text)
            param_widget_configs = []
            for param_name, param_widget_info in configs.param_widget_infos.items():
                param_widget_config = self._make_param_widget_config(
                    param_name, param_widget_info
                )
                param_widget_configs.append(param_widget_config)

            return template.render(
                configs_varname=configs_varname,
                param_widget_configs=param_widget_configs,
            )

    def _make_param_widget_config(
        self, param_name: str, param_widget_info: _ParamWidgetInfo
    ) -> _ParamWidgetConfig:
        param_widget_config = _ParamWidgetConfig(
            parameter_name=param_name,
            widget_class_name=param_widget_info.widget_class.__name__,
            widget_args_class_name=param_widget_info.widget_args_class.__name__,
        )
        self._add_common_widget_args_fields(param_name, param_widget_config)
        # add common field of widget args obj
        return param_widget_config

    def _add_common_widget_args_fields(
        self, param_name: str, param_widget_config: _ParamWidgetConfig
    ):
        for field_name, field_value in self._common_widget_args_fields.items():
            if callable(field_value):
                field_value = field_value(param_name)
            param_widget_config.widget_args_fields[field_name] = field_value
