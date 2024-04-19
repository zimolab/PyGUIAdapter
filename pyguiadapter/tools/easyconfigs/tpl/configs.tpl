<%def name="make_config_item(param_name, widget_class_name, widget_args_class_name, widget_args_fields)">
    "${param_name}": {
        "widget_class": ${widget_class_name},
        "widget_args": ${widget_args_class_name}(
            %for field_name, field_value in widget_args_fields.items():
            ${field_name}=${field_value},
            %endfor
        ),
    },
</%def>

${configs_varname} = {
    %for param_widget_config in param_widget_configs:
    <%
    param_name = param_widget_config.parameter_name
    widget_class_name = param_widget_config.widget_class_name
    widget_args_class_name = param_widget_config.widget_args_class_name
    widget_args_fields = param_widget_config.widget_args_fields
    %>
    ${make_config_item(param_name, widget_class_name, widget_args_class_name, widget_args_fields)}
    %endfor
}