from typing import Optional

import docstring_parser


class FnDocstring(object):

    def __init__(self, fn_docstring: str):
        self._fn_docstring: str = fn_docstring

        try:
            self._docstring = docstring_parser.parse(fn_docstring)
        except docstring_parser.ParseError:
            self._docstring = None

    def has_parameter(self, parameter_name: str) -> bool:
        if self._docstring is None:
            return False
        return self._find_parameter(parameter_name) is not None

    def get_short_description(self) -> Optional[str]:
        if self._docstring is None:
            return None
        return self._docstring.short_description

    def get_long_description(self) -> Optional[str]:
        if self._docstring is None:
            return None
        return self._docstring.long_description

    def get_parameter_description(self, parameter_name: str) -> Optional[str]:
        docstring_param = self._find_parameter(parameter_name)
        if docstring_param is None:
            return None
        return docstring_param.description.strip()

    def get_parameter_default_value(self, parameter_name: str) -> Optional[str]:
        docstring_param = self._find_parameter(parameter_name)
        if docstring_param is None:
            return None
        return docstring_param.default

    def get_parameter_typename(self, parameter_name: str) -> Optional[str]:
        docstring_param = self._find_parameter(parameter_name)
        if docstring_param is None:
            return None
        return docstring_param.type_name

    def _find_parameter(
        self, parameter_name: str
    ) -> Optional[docstring_parser.DocstringParam]:
        if self._docstring is None:
            return None
        for param in self._docstring.params:
            if param.arg_name == parameter_name:
                return param
        return None
