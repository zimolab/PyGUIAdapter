<p>${app_description}</p>
<div>
    %for name, value in app_fields.items():
    <p>${name}: ${value}</p>
    %endfor
</div>
%if app_license != "":
<p>${app_copyright}</p>
%endif
