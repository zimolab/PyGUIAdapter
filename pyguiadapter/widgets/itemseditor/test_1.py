from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.itemseditor.object_tableview import (
    ObjectEditView,
    ObjectEditViewConfig,
)

app = QApplication([])

# listview = ListView(None, config=ListViewConfig())
# listview.resize(800, 600)
# listview.show()
#
# listview.append_row("Item 1")
# listview.append_row("Item 2")
# listview.append_row("Item 3")
# listview.remove_row(1)

# tableview = TableView(
#     None, config=TableViewConfig(), column_headers=["Name", "Age", "Gender"]
# )
# tableview.resize(800, 600)
# tableview.show()
#
# tableview.append_row(["John", 25, "Male"])
# tableview.append_row(["Jane", 30, "Female"])
# tableview.insert_row(1, ["Bob", 20, "Male"])
# tableview.insert_row(2, {"Name": "Mary", "Age": 28, "Gender": "Female"})
# tableview.remove_row(0)
# tableview.swap_rows(0, 1)

from pyguiadapter.widgets.itemseditor.object_tableview.valuetypes import (
    IntValue,
    StringValue,
    BoolValue,
)
from pyguiadapter.widgets.itemseditor.itemsview_container import (
    CommonItemsViewContainer,
)

schema = {
    "Name": StringValue(),
    "Age": IntValue(),
    "Is Student": BoolValue(),
    "Occupation": StringValue(),
}
#
# tableview = MultiObjectEditView(None, config=MultiObjectEditViewConfig(), schema=schema)
# tableview.resize(800, 600)
# tableview.show()
# tableview.add_object({"Name": "John", "Age": 25, "Is Student": True})
# tableview.add_object({"Name": "Jane", "Age": 30, "Is Student": False})
# tableview.insert_object(1, {"Name": "Bob", "Age": 20, "Is Student": False})
# tableview.insert_object(2, {"Name": "Mary", "Age": 28, "Is Student": False})
# tableview.move_row_down(0)
# # tableview.remove_row(0)
#
# app.exec_()
#
#
# print(tableview.get_all_objects())

tableview = ObjectEditView(None, config=ObjectEditViewConfig(), schema=schema)
container = CommonItemsViewContainer(
    parent=None, items_view=tableview, control_widgets_position="bottom"
)
container.resize(800, 600)
container.show()
# tableview.resize(800, 600)
# tableview.show()
# print(tableview.schema)
# tableview.remove_key("Occupation")
# print(tableview.schema)
# tableview.add_key("email", StringValue(), value="john@example.com")
# print(tableview.schema)
app.exec_()
print(tableview.get_all_row_data())
print(tableview.get_object())
