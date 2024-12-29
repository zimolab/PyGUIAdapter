# from qtpy.QtWidgets import QApplication
#
# from pyguiadapter.widgets.itemseditor.object_editor import (
#     ObjectEditorConfig,
#     ObjectEditor,
# )
# from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
#     IntValue,
#     StringValue,
#     BoolValue,
# )
#
# app = QApplication([])
# schema = {
#     "Name": StringValue(),
#     "Age": IntValue(),
#     "Is Student": BoolValue(),
#     "Occupation": StringValue(),
# }
# config = ObjectEditorConfig()
# editor = ObjectEditor(None, schema, config)
# editor.set_object(
#     {
#         "Name": "John",
#         "Age": 25,
#         "Is Student": True,
#
#
#     }
# )
# editor.show()
# app.exec_()
# print(editor.get_object())
