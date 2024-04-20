from PyQt6.QtWidgets import QApplication
from function2widgets.widgets.misc.coloredit import Color
from datetime import datetime
from datetime import date
from datetime import time
from PyQt6.QtCore import QDateTime
from PyQt6.QtCore import QDate
from PyQt6.QtCore import QTime

FUNC_NAME = QApplication.tr("foo")
FUNC_DESC = QApplication.tr("")

LABEL_A = QApplication.tr("a")
LABEL_B = QApplication.tr("b")
LABEL_C = QApplication.tr("c")
LABEL_D = QApplication.tr("d")
LABEL_E = QApplication.tr("e")
LABEL_F = QApplication.tr("f")
LABEL_G = QApplication.tr("g")
LABEL_COLOR2 = QApplication.tr("color2")
LABEL_H = QApplication.tr("h")
LABEL_COLOR = QApplication.tr("color")
LABEL_DATETIME1 = QApplication.tr("datetime1")
LABEL_DATE1 = QApplication.tr("date1")
LABEL_TIME1 = QApplication.tr("time1")
LABEL_DATETIME2 = QApplication.tr("datetime2")
LABEL_DATE2 = QApplication.tr("date2")
LABEL_TIME2 = QApplication.tr("time2")

DESCRIPTION_A = QApplication.tr("param a")
DESCRIPTION_B = QApplication.tr("param b")
DESCRIPTION_C = QApplication.tr("param c")
DESCRIPTION_D = QApplication.tr("param d")
DESCRIPTION_E = QApplication.tr("param e")
DESCRIPTION_F = QApplication.tr("param f")
DESCRIPTION_G = QApplication.tr("param g")
DESCRIPTION_COLOR2 = QApplication.tr("param color2")
DESCRIPTION_H = QApplication.tr("param h")
DESCRIPTION_COLOR = QApplication.tr("param color")
DESCRIPTION_DATETIME1 = QApplication.tr("")
DESCRIPTION_DATE1 = QApplication.tr("")
DESCRIPTION_TIME1 = QApplication.tr("")
DESCRIPTION_DATETIME2 = QApplication.tr("")
DESCRIPTION_DATE2 = QApplication.tr("")
DESCRIPTION_TIME2 = QApplication.tr("")

DEFAULT_VALUE_DESCRIPTION_A = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_B = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_C = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_D = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_E = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_F = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_G = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_COLOR2 = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_H = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_COLOR = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_DATETIME1 = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_DATE1 = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_TIME1 = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_DATETIME2 = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_DATE2 = QApplication.tr("use default value({})")
DEFAULT_VALUE_DESCRIPTION_TIME2 = QApplication.tr("use default value({})")

DEFAULT_VALUE_A = None
DEFAULT_VALUE_B = None
DEFAULT_VALUE_C = None
DEFAULT_VALUE_D = None
DEFAULT_VALUE_E = None
DEFAULT_VALUE_F = None
DEFAULT_VALUE_G = None
DEFAULT_VALUE_COLOR2 = None
DEFAULT_VALUE_H = "12345"
DEFAULT_VALUE_COLOR = Color.from_string("#000000ff")
DEFAULT_VALUE_DATETIME1 = datetime.now()
DEFAULT_VALUE_DATE1 = date.today()
DEFAULT_VALUE_TIME1 = time()
DEFAULT_VALUE_DATETIME2 = QDateTime.currentDateTime()
DEFAULT_VALUE_DATE2 = QDate.currentDate()
DEFAULT_VALUE_TIME2 = QTime.currentTime()
