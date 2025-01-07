if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.itemseditor.valuetypes import (
        TimeValue,
    )

    app = QApplication([])
    schema = {
        "A": TimeValue(
            default_value="18:13:11",
            str_format="%H:%M:%S",
            minimum="00:00:00",
            maximum="10:59:59",
        ),
        "B": TimeValue(
            default_value="18.13.11",
            str_format="%H.%M.%S",
            minimum="00.00.00",
            maximum="10.59.59",
        ),
        "C": TimeValue(display_name="Label C"),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
