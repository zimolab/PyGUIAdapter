from __future__ import annotations

import dataclasses
import inspect
import warnings
from collections import OrderedDict
from typing import Callable, Literal, List, Tuple, Set, Dict, Any, Type

import tomli
from qtpy.QtGui import QIcon, QPixmap

from .typenames import get_typename, get_type_args
from .docstring import FnDocstring
from .. import utils
from ..fn import FnInfo, ParameterInfo


PARAM_WIDGET_METADATA_START = ("@widgets", "@parameters", "@params")
PARAM_WIDGET_METADATA_END = "@end"


class _Unset(object):
    pass


UNSET = _Unset


@dataclasses.dataclass
class WidgetMeta(object):
    widget_class: str | None | UNSET = UNSET
    default_value: Any | UNSET = UNSET
    label: str | None | UNSET = UNSET
    description: str | None | UNSET = UNSET
    default_value_description: str | None | UNSET = UNSET
    stylesheet: str | None | UNSET = UNSET
    custom_configs: Dict[str, Any] | UNSET = UNSET

    def to_config_dict(self) -> Dict[str, Any]:
        config_dict = dataclasses.asdict(self)
        custom_configs = config_dict.pop("custom_configs", None)
        if not isinstance(custom_configs, dict):
            custom_configs = OrderedDict()
        config_dict.update(**custom_configs)
        config_dict = {k: v for k, v in config_dict.items() if v is not UNSET}
        return config_dict


class FnParser(object):
    def __init__(
        self,
        widget_metadata_start: (
            str | List[str] | Tuple[str] | Set[str]
        ) = PARAM_WIDGET_METADATA_START,
        widget_metadata_end: (
            str | List[str] | Tuple[str] | Set[str]
        ) = PARAM_WIDGET_METADATA_END,
    ):
        self._widget_metadata_start: str | List[str] | Tuple[str] | Set[str] = (
            widget_metadata_start
        )
        self._widget_metadata_end: str | List[str] | Tuple[str] | Set[str] = (
            widget_metadata_end
        )

    def parse_fn_info(
        self,
        fn: Callable,
        display_name: str | None = None,
        document: str | None = None,
        document_format: Literal["markdown", "html", "plaintext"] = "markdown",
        icon: str | QIcon | QPixmap | None = None,
        group: str | None = None,
        ignore_self_param: bool = True,
    ) -> FnInfo:
        if not inspect.ismethod(fn) and not inspect.isfunction(fn):
            raise ValueError("fn must be a function or method")

        doc = fn.__doc__ or ""

        fn_docstring_text = utils.remove_text_block(
            doc, self._widget_metadata_start, self._widget_metadata_end
        )
        fn_docstring = FnDocstring(fn_docstring_text)

        if not display_name:
            display_name = fn.__name__

        if not document:
            document = (
                fn_docstring.get_long_description()
                or fn_docstring.get_short_description()
                or fn_docstring_text
            )

        return FnInfo(
            fn=fn,
            display_name=display_name,
            document=document,
            document_format=document_format,
            icon=icon,
            group=group,
            parameters=self._parse_fn_params(fn, fn_docstring, ignore_self_param),
        )

    def parse_widget_configs(
        self, fn_info: FnInfo
    ) -> Dict[str, Tuple[str | None, dict]]:
        configs = OrderedDict()
        metas = self._parse_widget_meta(fn_info)
        for param_name, param_info in fn_info.parameters.items():
            widget_config = OrderedDict(
                {
                    "default_value": param_info.default_value,
                    "label": param_name,
                    "description": param_info.description,
                    "default_value_description": None,
                    "stylesheet": None,
                }
            )
            widget_class = None
            meta = metas.get(param_name, None)
            if meta is not None:
                meta_config_dict = meta.to_config_dict()
                widget_class = meta_config_dict.pop("widget_class", None)
                widget_config.update(**meta_config_dict)
            configs[param_name] = (widget_class, widget_config)
        return configs

    def _parse_widget_meta(self, fn_info: FnInfo) -> Dict[str, WidgetMeta]:
        fn = fn_info.fn
        meta_text = utils.extract_text_block(
            fn.__doc__ or "", self._widget_metadata_start, self._widget_metadata_end
        )
        if meta_text is None:
            return OrderedDict()
        meta_text = meta_text.strip()

        try:
            metadata = tomli.loads(meta_text)
            if not isinstance(metadata, dict):
                raise ValueError("invalid widget configs text")
        except Exception as e:
            warnings.warn(f"failed to parse widget configs in docstring: {e}")
            return OrderedDict()

        meta = OrderedDict()
        for param_name, widget_configs in metadata.items():
            if not isinstance(widget_configs, dict):
                continue

            param_info: ParameterInfo | None = fn_info.parameters.get(param_name, None)
            widget_config_meta = WidgetMeta()

            key_widget_class = "widget_class"
            conf_widget_class = widget_configs.pop(key_widget_class, None)
            if conf_widget_class:
                widget_config_meta.widget_class = conf_widget_class
            else:
                widget_config_meta.widget_class = UNSET

            key_default_value = "default_value"
            conf_default_value = widget_configs.pop(key_default_value, None)
            if conf_default_value is not None:
                widget_config_meta.default_value = conf_default_value
            elif param_info is not None:
                widget_config_meta.default_value = param_info.default_value
            else:
                widget_config_meta.default_value = UNSET

            key_label = "label"
            conf_label = widget_configs.pop(key_label, None)
            if conf_label is not None:
                widget_config_meta.label = str(conf_label)
            elif param_info is not None:
                widget_config_meta.label = param_name
            else:
                widget_config_meta.label = UNSET

            key_description = "description"
            conf_description = widget_configs.pop(key_description, None)
            if conf_description is not None:
                widget_config_meta.description = str(conf_description)
            elif param_info is not None:
                widget_config_meta.description = str(param_info.description or "")
            else:
                widget_config_meta.description = UNSET

            key_default_value_description = "default_value_description"
            conf_default_value_description = widget_configs.pop(
                key_default_value_description, None
            )
            if conf_default_value_description is not None:
                widget_config_meta.default_value_description = str(
                    conf_default_value_description
                )
            else:
                widget_config_meta.default_value_description = UNSET

            key_stylesheet = "stylesheet"
            conf_stylesheet = widget_configs.pop(key_stylesheet, None)
            if conf_stylesheet is not None:
                widget_config_meta.stylesheet = str(conf_stylesheet)
            else:
                widget_config_meta.stylesheet = UNSET

            if len(widget_configs) > 0:
                widget_config_meta.custom_configs = {**widget_configs}

            meta[param_name] = widget_config_meta
        return meta

    def _parse_fn_params(
        self, fn: Callable, fn_docstring: FnDocstring, ignore_self_param: bool
    ) -> Dict[str, ParameterInfo]:
        params = OrderedDict()
        fn_signature = inspect.signature(fn)
        for param_name, param in fn_signature.parameters.items():
            if param_name in params:
                raise ValueError(f"duplicate parameter name: {param_name}")

            if ignore_self_param and param_name == "self":
                continue

            if param.default is not inspect.Parameter.empty:
                default_value = param.default
            else:
                default_value = fn_docstring.get_parameter_default_value(param.name)

            typename, type_args = self._get_param_type_info(
                param, default_value, fn_docstring
            )
            description = fn_docstring.get_parameter_description(param.name) or ""

            params[param_name] = ParameterInfo(
                typename=typename,
                type_args=type_args,
                default_value=default_value,
                description=description,
            )

        return params

    def _get_param_type_info(
        self, param: inspect.Parameter, default_value: Any, fn_docstring: FnDocstring
    ) -> (str, List[Any]):
        param_typename = None
        param_type_args = None

        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            raise RuntimeError(
                f"positional only parameters are not supported: {param.name}"
            )
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_type = list
            param_type_args = []
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            param_type = dict
            param_type_args = []
        elif self._has_type_annotation(param):
            param_type = param.annotation
        else:
            _param_type_in_docstring = fn_docstring.get_parameter_typename(param.name)
            if _param_type_in_docstring is not None:
                param_typename = _param_type_in_docstring
                param_type = None
            else:
                param_type = self._guess_param_type(default_value)
            param_type_args = []

        if param_typename is None:
            param_typename = get_typename(param_type)

        if param_type_args is None:
            param_type_args = get_type_args(param_type)

        return param_typename, param_type_args

    @staticmethod
    def _guess_param_type(default_value: Any) -> Type:
        if default_value is None:
            return Any
        if isinstance(default_value, type):
            return default_value
        return type(default_value)

    @staticmethod
    def _has_type_annotation(param: inspect.Parameter) -> bool:
        if (
            param.annotation is not None
            and param.annotation is not inspect.Parameter.empty
        ):
            return True
        return False
