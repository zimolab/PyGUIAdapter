from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.itemseditor.object_editor import (
    ObjectEditorConfig,
    ObjectEditor,
)
from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
    IntValue,
    StringValue,
    BoolValue,
    ChoiceValue,
    FloatValue,
    ColorValue,
    DateTimeValue,
    DateValue,
    TimeValue,
)
from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes._dir import PathValue

app = QApplication([])
schema = {
    "Name": StringValue(),
    "Age": IntValue(),
    "Is Student": BoolValue(),
    "Occupation": ChoiceValue(0, ["Engineer", "Teacher", "Doctor"]),
    "Height": FloatValue(180.0),
    "Favorite Color": ColorValue(display_color_name=True),
    "dir": PathValue(),
    "birthday": DateTimeValue(),
    "date": DateValue(),
    "time": TimeValue(),
}

config = ObjectEditorConfig()
editor = ObjectEditor(None, schema, config)
editor.set_object(
    {
        "Name": "John",
        "Age": 25,
        "Is Student": True,
    }
)
editor.show()
app.exec_()
print(editor.get_object())
