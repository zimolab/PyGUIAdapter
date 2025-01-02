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
    DirectoryValue,
    FileValue,
    GenericPathValue,
)

app = QApplication([])
schema = {
    "Name": StringValue(display_name="姓名"),
    "Age": IntValue(display_name="年龄"),
    "Is Student": BoolValue(display_name="是否学生", true_text="是", false_text="否"),
    "Occupation": ChoiceValue(
        0, ["Engineer", "Teacher", "Doctor"], display_name="职业"
    ),
    "Height": FloatValue(180.0, display_name="身高"),
    "Favorite Color": ColorValue(display_color_name=True, display_name="喜欢的颜色"),
    "dir": DirectoryValue(display_name="目录"),
    "file": FileValue(display_name="文件", file_filters="*.py"),
    "birthday": DateTimeValue(),
    "date": DateValue(display_name="日期"),
    "time": TimeValue(),
    "generic": GenericPathValue(),
}

config = ObjectEditorConfig()
editor = ObjectEditor(None, schema, config)
editor.set_object(
    {
        "Name": "John",
        "Age": 25,
    }
)
editor.show()
app.exec_()
print(editor.get_object())
