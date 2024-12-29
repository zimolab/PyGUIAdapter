from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.complex.objects_editor._frame import (
    ObjectsTableViewFrame,
    ObjectsTableViewFrameConfig,
)
from pyguiadapter.widgets.complex.value_types import StringValue, IntValue, BoolValue

schema = {
    "name": StringValue(),
    "age": IntValue(min_value=18, max_value=100),
    "address": StringValue(),
    "is_married": BoolValue(),
}

app = QApplication([])

win = ObjectsTableViewFrame(None, config=ObjectsTableViewFrameConfig(), schema=schema)
win.add_object(
    {"name": "John", "age": 25, "address": "123 Main St", "is_married": True}
)
win.show()
win.resize(800, 600)

app.exec_()
print(win.get_objects())
