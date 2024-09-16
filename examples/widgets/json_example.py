from typing import Any

from pyguiadapter.adapter import GUIAdapter


def json_example(arg1: object, arg2: Any, arg3: list):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(json_example)
    adapter.run()

# from __future__ import annotations
#
# import dataclasses
# import inspect
# import os.path
#
# from markdown_table_generator import generate_markdown, table_from_string_list
# from typing import Type, Tuple, List, Literal
#
# from pyguiadapter import widgets, utils
# from pyguiadapter.adapter import GUIAdapter
# from pyguiadapter.adapter.ucontext import uprint
# from pyguiadapter.exceptions import ParameterError
# from pyguiadapter.paramwidget import BaseParameterWidgetConfig, BaseParameterWidget
# from pyguiadapter.widgets.common import CommonParameterWidgetConfig
#
# # warnings.filterwarnings("error")
#
# CONFIG_CLASS_TABLE_HEADER_CN = ("配置项名称", "类型", "默认值", "说明")
#
#
# def _all_widget_classes() -> List[str]:
#     all_imported = dir(widgets)
#     ret = []
#     for name in all_imported:
#         obj = getattr(widgets, name, None)
#         if not obj:
#             continue
#         if inspect.isclass(obj) and issubclass(obj, BaseParameterWidget):
#             ret.append(obj.__name__)
#     return ret
#
#
# def _get_default_value(field: dataclasses.Field) -> str:
#     if field.default is not dataclasses.MISSING:
#         return str(field.default)
#     if field.default_factory is not dataclasses.MISSING:
#         return str(field.default_factory)
#     return ""
#
#
# def _config2table(
#     config_class: Type[BaseParameterWidgetConfig],
#     header: Tuple[str, str, str, str] | None = None,
#     exclude_props: List[str] | None = None,
# ):
#     if exclude_props is None:
#         exclude_props = []
#
#     if not header:
#         header = CONFIG_CLASS_TABLE_HEADER_CN
#     header = header
#
#     assert isinstance(header, tuple) and len(header) >= 4
#
#     props = [list(header)]
#
#     fields = dataclasses.fields(config_class)
#     for field in fields:
#         if field.name in exclude_props:
#             continue
#         prop_name = f"`{field.name}`"
#         prop_type = "`{}`".format(str(field.type).replace("|", "\|"))
#         prop_default = _get_default_value(field)
#         prop_desc = ""
#         props.append([prop_name, prop_type, f"`{prop_default}`", prop_desc])
#     table = table_from_string_list(props)
#     return generate_markdown(table)
#
#
# def generate_config_doc(
#     widget_type: str,
#     widget_category: Literal["basic", "extend", "path"],
#     headers: Tuple[str, str, str, str],
#     exclude_props: List,
# ):
#     if not widget_type:
#         raise ParameterError("widget_type", "widget_type cannot be empty")
#
#     widget_class = getattr(widgets, widget_type, None)
#     if not (
#         inspect.isclass(widget_class) and issubclass(widget_class, BaseParameterWidget)
#     ):
#         raise ValueError(f"cannot find widget class for {widget_type}")
#
#     widget_class_filename = utils.get_object_filename(widget_class)
#     if widget_class_filename:
#         widget_class_filename = os.path.basename(widget_class_filename)
#     else:
#         widget_class_filename = "<unknown.py>"
#
#     widget_config_class = widget_class.ConfigClass
#     widget_config_class_filename = utils.get_object_filename(widget_config_class)
#     if widget_config_class_filename:
#         widget_config_class_filename = os.path.basename(widget_config_class_filename)
#     else:
#         widget_config_class_filename = "<unknown.py>"
#
#     widget_config_props_table = _config2table(
#         widget_config_class, headers, exclude_props
#     )
#
#     widget_config_class_source = utils.get_object_sourcecode(widget_config_class)
#     if widget_config_class_source:
#         widget_config_class_source = (
#             "@dataclasses.dataclass(frozen=True)\n" + widget_config_class_source
#         )
#     else:
#         widget_config_class_source = "UNKNOWN"
#
#
# if __name__ == "__main__":
#
#     sig = inspect.signature(generate_config_doc)
#     print(sig)
#     for p in sig.parameters.values():
#         print(p)
#
#     common_props = (
#         field.name for field in dataclasses.fields(CommonParameterWidgetConfig)
#     )
#
#     all_props = list(common_props)
#     default_exclude_props = [prop for prop in all_props if prop != "default_value"]
#
#     exclude_props_conf = widgets.MultiChoiceBoxConfig(
#         default_value=default_exclude_props, choices=all_props
#     )
#     headers_conf = widgets.TupleEditConfig(
#         default_value=CONFIG_CLASS_TABLE_HEADER_CN,
#     )
#     widget_type_conf = widgets.ComboBoxConfig(choices=_all_widget_classes())
#
#     adapter = GUIAdapter()
#     adapter.add(
#         generate_config_doc,
#         # widget_configs={
#         #     "widget_type": widget_type_conf,
#         #     "headers": headers_conf,
#         #     "exclude_props": exclude_props_conf,
#         # },
#     )
#     adapter.run()
