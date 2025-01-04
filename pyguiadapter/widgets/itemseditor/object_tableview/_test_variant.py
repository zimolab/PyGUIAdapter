if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
        VariantValue,
        ListValue,
        TupleValue,
        DictValue,
    )

    app = QApplication([])
    schema = {
        "A": VariantValue(default_value=1234),
        "B": VariantValue(default_value="Hello, world!"),
        "C": VariantValue(default_value=[1, 2, 3, 4]),
        "D": ListValue(default_value=[1, 2, 3, 4]),
        "E": TupleValue(default_value=(1, 2, 3, 4)),
        "F": DictValue(default_value={"a": 1, "b": 2, "c": 3}),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
