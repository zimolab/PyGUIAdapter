from qtpy.QtWidgets import QApplication

from pyguiadapter.extend_types import file_t
from pyguiadapter.widgets.extend.pole.listeditor import (
    PlainObjectListEditor,
    PlainObjectListEditorConfig,
)
from pyguiadapter.widgets.extend.pole.valuetypes import DirPathValue, PathValue
from pyguiadapter.widgets.extend.pole.valuetypes.filevalue import FilePathValue

if __name__ == "__main__":
    app = QApplication([])
    schema = {
        "name": str,
        "age": int,
        "profile": file_t,
        "file": FilePathValue(),
        "directory": DirPathValue(),
        "path": PathValue(),
    }
    editor = PlainObjectListEditor(PlainObjectListEditorConfig(object_schema=schema))
    editor.set_objects(
        [
            {"name": "Alice", "age": 25, "profile": "alice.jpg"},
            {"name": "Bob", "age": 30, "profile": "bob.jpg"},
            {"name": "Charlie", "age": 35, "profile": "charlie.jpg"},
        ]
    )
    editor.show()
    app.exec()
    print(editor.get_objects())
