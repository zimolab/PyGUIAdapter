if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.valuetypes import (
        DateTimeValue,
    )

    app = QApplication([])
    schema = {
        "A": DateTimeValue(
            default_value="2022-01-06T18:13:11Z",
            str_format="%Y-%m-%dT%H:%M:%SZ",
            minimum="2022-01-01T00:00:00Z",
            maximum="2022-12-31T23:59:59Z",
            calendar_popup=False,
        ),
        "B": DateTimeValue(),
        "C": DateTimeValue(display_name="Label C"),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
