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
    "Name": StringValue(display_name="姓名"),
    "Age": IntValue(display_name="年龄"),
    "Is Student": BoolValue(display_name="是否学生"),
    "Occupation": ChoiceValue(
        0, ["Engineer", "Teacher", "Doctor"], display_name="职业"
    ),
    "Height": FloatValue(180.0, display_name="身高"),
    "Favorite Color": ColorValue(display_color_name=True, display_name="喜欢的颜色"),
    "dir": PathValue(display_name="目录"),
    "birthday": DateTimeValue(),
    "date": DateValue(display_name="日期"),
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
