if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.itemseditor.valuetypes import BoolValue

    app = QApplication([])
    schema = {
        "A": BoolValue(default_value=True),
        "B": BoolValue(default_value=False, true_text="是", false_text="否"),
        "C": BoolValue(default_value=False, display_name="Label C", false_text="Off"),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
