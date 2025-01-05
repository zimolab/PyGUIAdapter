if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication, QMessageBox

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.valuetypes import (
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
        VariantValue,
        ListValue,
        TupleValue,
        DictValue,
    )

    app = QApplication([])
    schema = {
        "Name": StringValue(display_name="姓名"),
        "Age": IntValue(display_name="年龄"),
        "Is Student": BoolValue(
            display_name="是否学生", true_text="是", false_text="否"
        ),
        "Occupation": ChoiceValue(
            0, ["Engineer", "Teacher", "Doctor"], display_name="职业"
        ),
        "Height": FloatValue(180.0, display_name="身高"),
        "Favorite Color": ColorValue(
            display_color_name=True, display_name="喜欢的颜色"
        ),
        "dir": DirectoryValue(display_name="目录"),
        "file": FileValue(display_name="文件", file_filters="*.py"),
        "birthday": DateTimeValue(),
        "date": DateValue(display_name="日期"),
        "time": TimeValue(),
        "generic": GenericPathValue(),
        "variant": VariantValue(
            [1, "hello", True, {"a": 1, "b": 2}], display_name="可变类型"
        ),
        "list": ListValue([1, 2, 3], display_name="列表"),
        "tuple": TupleValue((1, 2, 3), display_name="元组"),
        "dict": DictValue({"a": 1, "b": 2}, display_name="字典"),
    }

    def on_accept(s, obj) -> bool:
        if obj.get("Age") < 18:
            QMessageBox.warning(s, "警告", "年龄必须大于等于18")
            return False
        return True

    config = ObjectEditorConfig(resize_rows_to_contents=False)
    editor = ObjectEditor(None, schema, config, accept_hook=on_accept)
    editor.set_object(
        {
            "Name": "John",
            "Age": 25,
        }
    )
    editor.show()
    app.exec_()
    print(editor.get_object())
