from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.complex.objects_editor._frame import ObjectsTableViewFrame
from pyguiadapter.widgets.complex.objects_editor.valuetypes import (
    StringValue,
    IntValue,
    FilePathValue,
)
from pyguiadapter.widgets.complex.schema import ObjectSchemaFactory


class file_path(str):
    pass


#
schema = {
    "name": "Tom",
    "age": 25,
    "gender": StringValue("unknown gender"),
    "address": StringValue("unknown address"),
    "file": FilePathValue("1234"),
    "file2": file_path("5678"),
}
factory = ObjectSchemaFactory()
factory.register(int, IntValue())
factory.register(str, StringValue())
factory.register(file_path, FilePathValue(""))


schema = factory.create_schema(schema_dict=schema)
print(schema["file2"].default_value)


app = QApplication([])
frame = ObjectsTableViewFrame(None, schema)
frame.add_object(
    {"name": "Alice", "age": 25, "gender": "female", "address": "123 Main St"}
)
frame.add_object({"name": "Bob", "gender": "male", "address": "456 Oak St"})
frame.show()
frame.resize(800, 600)
app.exec_()
