from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.itemseditor.multiobject_editor import (
    MultiObjectEditor,
    MultiObjectEditorConfig,
)
from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
    StringValue,
    IntValue,
    BoolValue,
    FloatValue,
    ChoiceValue,
    ColorValue,
    DateTimeValue,
    DateValue,
    TimeValue,
    DirectoryValue,
    FileValue,
    GenericPathValue,
)

schema = {
    "Name": StringValue(display_name="姓名"),
    "Age": IntValue(display_name="年龄"),
    "Is Student": BoolValue(display_name="是否学生"),
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
