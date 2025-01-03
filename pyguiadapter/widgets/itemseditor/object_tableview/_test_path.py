if __name__ == "__main__":
    from os.path import expanduser
    from qtpy.QtWidgets import QApplication

    from pyguiadapter.widgets.itemseditor.object_editor import (
        ObjectEditorConfig,
        ObjectEditor,
    )
    from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
        DirectoryValue,
        FileValue,
        GenericPathValue,
    )

    app = QApplication([])
    schema = {
        "A": FileValue(as_posix=False),
        "B": FileValue(
            default_value="/path/to/file.txt",
            display_name="Label B",
            title="Choose File",
            file_filters="Text Files (*.txt);;Json Files (*.json);;All Files (*)",
            selected_filter="Json Files (*.json)",
            start_directory=expanduser("~"),
            as_posix=True,
        ),
        "C": DirectoryValue(
            default_value="/path/to/dir",
            display_name="Label C",
            title="Choose Directory",
            show_dirs_only=True,
            start_directory=expanduser("~"),
            as_posix=True,
        ),
        "D": DirectoryValue(show_dirs_only=False, as_posix=False),
        "E": GenericPathValue(
            default_value="/path/to/file.txt",
            display_name="Label E",
            window_title="Choose Path",
            file_button_text="Choose File",
            directory_button_text="Choose Directory",
            file_dialog_title="Choose File",
            directory_dialog_title="Choose Directory",
            any_file=True,
            show_dirs_only=False,
            start_directory=expanduser("~"),
            file_filters="Text Files (*.txt);;Json Files (*.json);;All Files (*)",
            selected_filter="Json Files (*.json)",
            as_posix=True,
        ),
    }

    config = ObjectEditorConfig()
    editor = ObjectEditor(None, schema, config)
    editor.show()
    app.exec_()
    print(editor.get_object())
