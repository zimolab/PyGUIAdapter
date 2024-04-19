% for const_name in func_constants:
${const_name} = ${func_constants[const_name]}
% endfor

% for const_name in param_labels:
${const_name} = ${param_labels[const_name]}
% endfor

% for const_name in param_descs:
${const_name} = ${param_descs[const_name]}
% endfor

% for const_name in param_default_value_descs:
${const_name} = ${param_default_value_descs[const_name]}
% endfor

% for const_name in param_default_values:
${const_name} = ${param_default_values[const_name]}
% endfor