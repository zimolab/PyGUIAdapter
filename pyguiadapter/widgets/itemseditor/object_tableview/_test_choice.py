if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
        ChoiceValue,
    )

    app = QApplication([])
    schema = {
        "A": ChoiceValue(
            default_value="apple",
            choices=["apple", "banana", "orange"],
        ),
        "B": ChoiceValue(
            default_value=1, choices=["apple", "banana", "orange"], editable=True
        ),
        "C": ChoiceValue(
            default_value=2,
            choices=["apple", "banana", "orange"],
        ),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
