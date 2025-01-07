if __name__ == "__main__":
    from qtpy.QtGui import QIntValidator
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.itemseditor.valuetypes import (
        StringValue,
        PasswordEchoOnEditMode,
        NormalEchoMode,
    )

    app = QApplication([])
    schema = {
        "A": StringValue(input_mask="999.999.999.999"),
        "B": StringValue(
            "Hello, World!",
            placeholder="Enter text here",
            clear_button=True,
            echo_mode=PasswordEchoOnEditMode,
        ),
        "C": StringValue(
            display_name="Label C",
            placeholder="Enter text here",
            clear_button=True,
            echo_mode=NormalEchoMode,
            # input_mask="999.999.999.999",
            validator=QIntValidator(),
        ),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
