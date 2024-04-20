"""
this script make use of the easyconfigs tool (pyguiadapter.tools.easyconfigs) to generate the parameter widget configs
template file which helps user to customize their ui interface more easily and reduce the work of writing tedious code.

How to use:
1. get a ParameterWidgetConfigsCodeGenerator instance. Using get_configs_code_generator() to get a global instance or
use generator = ParameterWidgetConfigsCodeGenerator() to create a new instance.

2. import the function you want to generate parameter widget configs files for

3. call generator.generate_configs_file() to generate the configs file. You can specify the output directory,
the filename of the generated files and other arguments. To avoid accidental damage to existing files, if the specified
file already exists, the generation will fail. In this case, you can specify a new file name, or if you are sure,
delete the existing file

4. modify the generated configs code as needed.

5. import the CONFIGS variable in your main script and pass it to gui_adapter.add()

Note:
    Use easyconfigs tool only in dev phase. Generally speaking, the tool is part of the development tool rather than
    an integral part of the final product.

"""

import os.path

if __name__ == "__main__":
    from pyguiadapter.tools.easyconfigs import get_configs_code_generator
    from examples.easyconfigs_demo.main_script import foo

    DEST_DIR = os.path.dirname(os.path.abspath(__file__))

    generator = get_configs_code_generator()
    generator.generate_configs_file(
        func=foo,
        dest_dir=DEST_DIR,
        onefile=False,
        filename="_configs.py",
        constants_filename="_constants.py",
    )
