import sys

from qtpy.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from pyguiadapter.widgets.complex.object_editor._frame import (
    ObjectTableViewFrame,
    ObjectTableViewFrameConfig,
)
from pyguiadapter.widgets.complex.objects_editor.valuetypes import StringValue, IntValue

schema = {
    "姓名": StringValue(),
    "年龄": IntValue(default_value=sys.maxsize),
    "地址": StringValue(),
    "电话": StringValue(),
}
app = QApplication([])
frame = ObjectTableViewFrame(None, schema, ObjectTableViewFrameConfig())
frame.show()
frame.resize(800, 600)
app.exec_()
