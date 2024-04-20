from typing import Optional, List, Tuple

from PyQt6.QtWidgets import QApplication

FUNC_RESULT_MSG = QApplication.tr("{}")
FUNC_RESULT_DIALOG_TITLE = QApplication.tr("Function Result")
FUNC_START_MSG = QApplication.tr("Execution Started")
FUNC_FINISH_MSG = QApplication.tr("Execution Finished")
FUNC_ERROR_MSG = QApplication.tr("Error: {}")
FUNC_ERROR_DIALOG_TITLE = QApplication.tr("Function Execution Error")
BUSY_MSG = QApplication.tr("A function is already executing!")
BUSY_DIALOG_TITLE = QApplication.tr("Busy")

DOCK_SIZES = (460, 460)

SOLE_WINDOW_SIZE = (460, 600)

# (typename, [...type_extras])
ParamInfoType = Tuple[str, Optional[List[str]]]
