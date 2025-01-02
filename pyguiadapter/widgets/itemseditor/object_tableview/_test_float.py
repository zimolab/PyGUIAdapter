if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import FloatValue

    app = QApplication([])
    schema = {
        "A": FloatValue(),
        "B": FloatValue(
            default_value=100,
            decimals=5,
            min_value=0,
            max_value=99,
            step=0.00005,
            prefix="$",
            suffix=" Dollars",
            display_affix=True,
        ),
        "C": FloatValue(
            default_value=50,
            display_name="Label C",
            decimals=3,
            display_as_decimals=True,
        ),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
