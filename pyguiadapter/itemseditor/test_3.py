if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.itemseditor.multiobject_editor import (
        MultiObjectEditor,
        MultiObjectEditorConfig,
    )
    from pyguiadapter.itemseditor.valuetypes import (
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
        VariantValue,
        TupleValue,
        ListValue,
        DictValue,
    )

    schema = {
        "Name": StringValue(display_name="姓名"),
        "Age": IntValue(display_name="年龄"),
        "Is Student": BoolValue(display_name="是否学生"),
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
        "variant": VariantValue(default_value=None),
        "tuple": TupleValue(default_value=("a", 1, True)),
        "list": ListValue(default_value=["a", 1, True]),
        "dict": DictValue(default_value={"a": 1, "b": 2}),
    }

    def on_accept(s, objects) -> bool:
        print("on_accept: ", s, objects)
        return True

    def on_reject(s) -> bool:
        print("on_reject: ", s)
        return True

    def on_item_editor_accept(s, obj) -> bool:
        print("on_item_editor_accept: ", s, obj)
        return True

    def on_item_editor_reject(s) -> bool:
        print("on_item_editor_reject: ", s)
        return True

    app = QApplication([])
    config = MultiObjectEditorConfig()
    editor = MultiObjectEditor(
        None,
        schema,
        config,
        accept_hook=on_accept,
        reject_hook=on_reject,
        item_editor_accept_hook=on_item_editor_accept,
        item_editor_reject_hook=on_item_editor_reject,
    )
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
