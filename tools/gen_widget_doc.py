from __future__ import annotations

import dataclasses
import inspect
import os.path
from typing import Type, Tuple, List, Literal

import jinja2
from markdown_table_generator import generate_markdown, table_from_string_list

import pyguiadapter.utils.messagebox
from pyguiadapter import widgets, utils
from pyguiadapter.adapter import GUIAdapter, uoutput, udialog
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.extend_types import file_t
from pyguiadapter.paramwidget import BaseParameterWidget
from pyguiadapter.widgets.common import CommonParameterWidgetConfig
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig

# warnings.filterwarnings("error")

CONFIG_CLASS_TABLE_HEADER_CN = ("配置项名称", "类型", "默认值", "说明")


def _all_widget_classes() -> List[str]:
    all_imported = dir(widgets)
    ret = []
    for name in all_imported:
        obj = getattr(widgets, name, None)
        if not obj:
            continue
        if inspect.isclass(obj) and issubclass(obj, BaseParameterWidget):
            ret.append(obj.__name__)
    return ret


def _get_default_value(field: dataclasses.Field) -> str:
    if field.default is not dataclasses.MISSING:
        return str(field.default)
    if field.default_factory is not dataclasses.MISSING:
        return str(field.default_factory)
    return ""


def dataclass2table(
    clazz: Type,
    header: Tuple[str, str, str, str] | None = None,
    exclude_props: List[str] | None = None,
):
    assert dataclasses.is_dataclass(clazz)

    if exclude_props is None:
        exclude_props = []

    if not header:
        header = CONFIG_CLASS_TABLE_HEADER_CN
    header = header

    assert isinstance(header, tuple) and len(header) >= 4

    props = [list(header)]

    fields = dataclasses.fields(clazz)
    for field in fields:
        if field.name in exclude_props:
            continue
        prop_name = f"`{field.name}`"
        prop_type = "`{}`".format(str(field.type).replace("|", "\|"))
        prop_default = _get_default_value(field)
        prop_desc = ""
        props.append([prop_name, prop_type, f"`{prop_default}`", prop_desc])
    table = table_from_string_list(props)
    return generate_markdown(table)


def generate_widget_class_doc(
    widget_type: str,
    widget_category: Literal["basic", "extend"] = "basic",
    template_file: file_t = "",
    output_file: file_t = "",
    headers: Tuple[str, str, str, str] = CONFIG_CLASS_TABLE_HEADER_CN,
    exclude_props: List = None,
):
    """
    ## Document Generator

    This tool is mainly used for generating the document page of the selected widget class.

    User must provide a document template file of jinja2.
    """
    if exclude_props is None:
        exclude_props = []

    if not widget_type:
        raise ParameterError("widget_type", "widget_type cannot be empty")

    if not widget_category:
        raise ParameterError("widget_category", "widget_category cannot be empty")

    if not template_file:
        raise ParameterError("template_file", "template_file cannot be empty")

    if not output_file:
        raise ParameterError("output_file", "output_file cannot be empty")

    if os.path.isfile(output_file):
        uoutput.warning(f"Output file {output_file} already exists! Overwrite?")
        ret = udialog.show_question_dialog(
            f"Output file {output_file} already exists! Do you want to overwrite it?"
        )
        if ret != pyguiadapter.utils.messagebox.StandardButton.Yes:
            uoutput.warning(" |")
            uoutput.warning("  - User cancelled")
            uoutput.info("==Generating Finished!==")
            return
        uoutput.info(" |")
        uoutput.info("  - Overwrite Approved")

    widget_class = getattr(widgets, widget_type, None)
    if not (
        inspect.isclass(widget_class) and issubclass(widget_class, BaseParameterWidget)
    ):
        raise ValueError(f"cannot find widget class for {widget_type}")

    widget_class_name = widget_class.__name__
    uoutput.info(f"Generating config doc for {widget_class_name}...")
    uoutput.info(f"Widget Class: {widget_class_name}")

    widget_class_filename = utils.get_object_filename(widget_class)
    if widget_class_filename:
        widget_class_filename = os.path.basename(widget_class_filename)
        uoutput.info(" |")
        uoutput.info(f"  -Filename: {widget_class_filename}")
    else:
        widget_class_filename = "<unknown.py>"
        uoutput.warning(" |")
        uoutput.warning(f"  -Filename: {widget_class_filename}")

    widget_config_class = widget_class.ConfigClass
    widget_config_class_name = widget_config_class.__name__
    uoutput.info(f"Config Class: {widget_config_class_name}")
    widget_config_class_filename = utils.get_object_filename(widget_config_class)
    if widget_config_class_filename:
        widget_config_class_filename = os.path.basename(widget_config_class_filename)
        uoutput.info(" |")
        uoutput.info(f"  -Filename: {widget_config_class_filename}")
    else:
        widget_config_class_filename = "<unknown.py>"
        uoutput.warning(f" |")
        uoutput.warning(f"  -Filename: {widget_config_class_filename}")

    widget_config_props_table = dataclass2table(
        widget_config_class, headers, exclude_props
    )

    widget_config_class_source = utils.get_object_sourcecode(widget_config_class)
    if widget_config_class_source:
        widget_config_class_source = (
            "@dataclasses.dataclass(frozen=True)\n" + widget_config_class_source
        )
    else:
        widget_config_class_source = "UNKNOWN"

    try:
        template_content = utils.read_text_file(template_file)
    except Exception as e:
        uoutput.critical("Error:")
        uoutput.critical(f"  {e}")
        uoutput.info("==Generating Finished!==")
        raise e
    else:
        uoutput.info("Template File Loaded")
        uoutput.info(" |")
        uoutput.info(f"  - {os.path.normpath(template_file)}")
    template = jinja2.Template(template_content)
    try:
        output_content = template.render(
            widget_class_name=widget_class_name,
            widget_category=widget_category,
            widget_class_filename=widget_class_filename,
            widget_config_class_name=widget_config_class_name,
            widget_config_class_filename=widget_config_class_filename,
            widget_config_class_source=widget_config_class_source,
            widget_config_props_table=widget_config_props_table,
        )
        utils.write_text_file(output_file, output_content)
    except Exception as e:
        uoutput.critical("Error:")
        uoutput.critical(f"  {e}")
        uoutput.info("==Generating Finished!==")
        raise e
    else:
        uoutput.info("Document File Generated")
        uoutput.info(" |")
        uoutput.info(f"  - {os.path.normpath(output_file)}")
        uoutput.info("==Generating Finished!==")
        udialog.show_info_dialog(
            f"Document file for widget '{widget_class_name}' generated successfully!",
            "Success",
        )


if __name__ == "__main__":
    ########################## parameter configs ################################################
    common_props = (
        field.name for field in dataclasses.fields(CommonParameterWidgetConfig)
    )
    all_props = list(common_props)
    default_exclude_props = [prop for prop in all_props if prop != "default_value"]
    exclude_props_conf = widgets.MultiChoiceBoxConfig(
        default_value=default_exclude_props, choices=all_props
    )

    headers_conf = widgets.TupleEditConfig(
        default_value=CONFIG_CLASS_TABLE_HEADER_CN,
    )

    template_file_conf = widgets.FileSelectConfig(
        filters="Jinja2 files(*.j2);;Markdown files(*.md);;Text files(*.txt);;All files(*.*)",
    )

    output_file_conf = widgets.FileSelectConfig(
        filters="Markdown files(*.md);;Text files(*.txt);;All files(*.*)",
        save_file=True,
    )

    widget_type_conf = widgets.ChoiceBoxConfig(choices=_all_widget_classes())
    ########################## parameter configs ################################################

    ########################## window configs ################################################
    win_conf = FnExecuteWindowConfig(
        show_function_result=False, print_function_result=False
    )
    ########################## window configs ################################################

    adapter = GUIAdapter()
    adapter.add(
        generate_widget_class_doc,
        widget_configs={
            "widget_type": widget_type_conf,
            "template_file": template_file_conf,
            "output_file": output_file_conf,
            "headers": headers_conf,
            "exclude_props": exclude_props_conf,
        },
        window_config=win_conf,
    )
    adapter.run()
