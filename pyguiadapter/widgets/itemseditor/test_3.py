# from qtpy.QtWidgets import QApplication
#
# from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
#     StringValue,
#     IntValue,
#     BoolValue,
# )
# from pyguiadapter.widgets.itemseditor.multiobject_editor import (
#     MultiObjectEditor,
#     MultiObjectEditorConfig,
# )
#
# schema = {
#     "Name": StringValue(),
#     "Age": IntValue(),
#     "Is Student": BoolValue(),
#     "Occupation": StringValue(),
# }
#
# app = QApplication([])
# config = MultiObjectEditorConfig()
# editor = MultiObjectEditor(None, schema, config)
# editor.set_objects(
#     [
#         {"Name": "John", "Age": 25, "Is Student": True, "Occupation": "Engineer"},
#         {"Name": "Jane", "Age": 30, "Is Student": False, "Occupation": "Teacher"},
#         {"Name": "Bob", "Age": 40, "Is Student": True, "Occupation": "Doctor"},
#         {"Name": "Tom"},
#     ]
# )
# editor.show()
# app.exec_()
# print(editor.get_objects())
