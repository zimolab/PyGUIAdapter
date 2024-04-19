import os

from PyQt6.QtWidgets import QApplication

DEFAULT_TR_FUNCTION = "QApplication.tr"
DEFAULT_QUOTE = '"'

EXTRA_IMPORTS = (QApplication,)

PARAM_LABEL_PREFIX = "LABEL_"
PARAM_DESC_PREFIX = "DESCRIPTION_"
PARAM_DEFAULT_VALUE_DESC_PREFIX = "DEFAULT_VALUE_DESCRIPTION_"
PARAM_DEFAULT_VALUE_PREFIX = "DEFAULT_VALUE_"

DEFAULT_VALUE_DESC = "use default value({})"

SHORT_IMPORT = "from function2widgets import {}"

TPL_PKG = "pyguiadapter.tools.easyconfigs"
TPL_DIR = "tpl"

TPL_FILENAME_CONFIGS = "configs.tpl"
TPL_FILENAME_CONSTANTS = "constants.tpl"

DEFAULT_CONSTANTS_FILENAME = "_constants.py"
DEFAULT_CONFIGS_FILENAME = "_configs.py"
DEFAULT_DEST_DIR = os.getcwd()
DEFAULT_CONFIGS_VARNAME = "CONFIGS"
