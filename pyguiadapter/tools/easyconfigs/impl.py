import os.path
from io import StringIO
from typing import Callable, Iterable

from function2widgets import (
    FunctionInfoParser,
    ParameterWidgetFactory,
)
from mako.template import Template

from pyguiadapter import get_function_parser, get_param_widget_factory
from .constants import *
from .helper.const_name_value import ConstNameValueHelper
from .helper.imports import ImportsHelper
from .helper.parameter_constants import ParameterConstantsHelper
from .helper.parameter_widget_configs import ParameterWidgetConfigsHelper
from .structures import _ParameterConstants, _ParamWidgetConfig, _Imports
from .utils import get_constants_tpl_file, get_configs_tpl_file


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
        param_widget_short_import: str = SHORT_IMPORT,
        extra_types_to_import: tuple = EXTRA_IMPORTS,
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

        self._param_widget_short_import = param_widget_short_import
        self._extra_types_to_import = extra_types_to_import

        self._configs_varname = configs_varname

        self._parser = func_info_parser or get_function_parser()
        self._factory = param_widget_factory or get_param_widget_factory()

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

        param_constants_helper = ParameterConstantsHelper(
            func_info, self._const_name_value_helper
        )
        param_constants = param_constants_helper.make_constants()

        param_widget_configs_helper = ParameterWidgetConfigsHelper(
            self._factory, self._const_name_value_helper
        )
        param_widget_configs = param_widget_configs_helper.make_configs(func_info)

        imports_helper = ImportsHelper(
            self._param_widget_short_import, self._extra_types_to_import
        )
        imports = imports_helper.make_imports(
            func_info=func_info, param_widget_configs=param_widget_configs
        )

        if constants_filepath is not None:
            self.generate_separated_files(
                constants_filepath,
                configs_filepath,
                imports,
                param_constants,
                param_widget_configs,
            )
        else:
            # write configs file
            self._generate_onefile(
                configs_filepath, imports, param_constants, param_widget_configs
            )

    def _generate_onefile(
        self,
        filepath: str,
        imports: _Imports,
        param_constants: _ParameterConstants,
        param_widget_configs: Iterable[_ParamWidgetConfig],
    ):
        with open(filepath, "w", encoding="utf-8") as output:
            all_imports = (
                *imports.other_imports,
                *imports.param_widget_imports,
                *imports.param_const_imports,
            )
            imports_code = self._generate_imports_code(*all_imports)
            output.write(imports_code)

            constants_code = self._generate_param_constants_code(param_constants)
            output.write(constants_code)

            configs_code = self._generate_param_widget_configs_code(
                param_widget_configs
            )
            output.write(configs_code)
            output.write("\n")
            output.flush()

    def generate_separated_files(
        self,
        constants_filepath: str,
        configs_filepath: str,
        imports: _Imports,
        param_constants: _ParameterConstants,
        param_widget_configs: Iterable[_ParamWidgetConfig],
    ):
        with open(constants_filepath, "w", encoding="utf-8") as output:
            constants_imports = (
                *imports.other_imports,
                *imports.param_const_imports,
            )
            imports_code = self._generate_imports_code(*constants_imports)
            output.write(imports_code)

            constants_code = self._generate_param_constants_code(param_constants)
            output.write(constants_code)
            output.flush()

        with open(configs_filepath, "w", encoding="utf-8") as output:
            constants_filename = os.path.basename(constants_filepath)
            constants_module = os.path.splitext(constants_filename)[0]

            configs_imports = (
                *imports.param_widget_imports,
                f"from .{constants_module} import *",
            )
            imports_code = self._generate_imports_code(*configs_imports)
            output.write(imports_code)

            configs_code = self._generate_param_widget_configs_code(
                param_widget_configs
            )
            configs_code = configs_code.lstrip()
            output.write(configs_code)
            output.flush()

    @staticmethod
    def _generate_imports_code(*imports: str) -> str:
        import_added = set()
        buffer = StringIO()
        for import_ in imports:
            if import_ in import_added:
                continue
            buffer.write(import_)
            buffer.write("\n")
            import_added.add(import_)
        buffer.write("\n")
        return buffer.getvalue()

    @staticmethod
    def _generate_param_constants_code(constants: _ParameterConstants) -> str:
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

    def _generate_param_widget_configs_code(
        self, param_widget_configs: Iterable[_ParamWidgetConfig]
    ) -> str:
        with open(get_configs_tpl_file(), "r", encoding="utf-8") as tpl_file:
            tpl_text = tpl_file.read()
            template = Template(tpl_text)
            return template.render(
                configs_varname=self._configs_varname,
                param_widget_configs=param_widget_configs,
            )
