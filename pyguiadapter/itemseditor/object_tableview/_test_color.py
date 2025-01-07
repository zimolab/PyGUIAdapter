if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.itemseditor.valuetypes import ColorValue

    app = QApplication([])
    schema = {
        "A": ColorValue(
            default_value=(255, 0, 0, 255), alpha_channel=True, display_color_name=True
        ),
        "B": ColorValue(
            default_value="#FF0000", alpha_channel=False, display_color_name=False
        ),
        "C": ColorValue(),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
