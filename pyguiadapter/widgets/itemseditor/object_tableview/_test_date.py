if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.valuetypes import (
        DateValue,
    )

    app = QApplication([])
    schema = {
        "A": DateValue(
            default_value="2022-01-06",
            str_format="%Y-%m-%d",
            minimum="2022-01-01",
            maximum="2022-12-31",
            calendar_popup=False,
        ),
        "B": DateValue(display_format="dd/MM/yyyy", str_format="%m/%d/%Y"),
        "C": DateValue(display_name="Label C"),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
