from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.complex.paths_editor import PathListEditor

app = QApplication([])
path_list_frame = PathListEditor()
path_list_frame.show()
app.exec_()
print(path_list_frame.get_path_list())
