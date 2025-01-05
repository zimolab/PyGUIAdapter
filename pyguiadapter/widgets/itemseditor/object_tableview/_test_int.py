if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.valuetypes import IntValue

    app = QApplication([])
    schema = {
        "A": IntValue(),
        "B": IntValue(
            default_value=100,
            min_value=0,
            max_value=99,
            step=2,
            prefix="$",
            suffix=" Dollars",
            display_affix=True,
        ),
        "C": IntValue(default_value=50, display_name="Label C"),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
