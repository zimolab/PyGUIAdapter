from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
    StringValue,
    IntValue,
    BoolValue,
    FloatValue,
    ChoiceValue,
    ColorValue,
)
from pyguiadapter.widgets.itemseditor.multiobject_editor import (
    MultiObjectEditor,
    MultiObjectEditorConfig,
)
from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes._dir import PathValue

schema = {
    "Name": StringValue(),
    "Age": IntValue(),
    "Is Student": BoolValue(),
    "Occupation": ChoiceValue(0, ["Engineer", "Teacher", "Doctor"]),
    "Height": FloatValue(180.0),
    "Favorite Color": ColorValue(),
    "dir": PathValue(),
}

app = QApplication([])
config = MultiObjectEditorConfig()
editor = MultiObjectEditor(None, schema, config)
editor.set_objects(
    [
        {"Name": "John", "Age": 25, "Is Student": True, "Occupation": "Engineer"},
        {"Name": "Jane", "Age": 30, "Is Student": False, "Occupation": "Teacher"},
        {"Name": "Bob", "Age": 40, "Is Student": True, "Occupation": "Doctor"},
        {"Name": "Tom", "dir": "/home/user/Documents"},
    ]
)
editor.show()
app.exec_()
print(editor.get_objects())
