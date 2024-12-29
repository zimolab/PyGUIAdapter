from qtpy.QtWidgets import QApplication

from pyguiadapter.widgets.complex.paths_editor import PathListEditor
from pyguiadapter.widgets.extend.pathlist2.editor import PathListEditorConfig

app = QApplication([])
path_list_frame = PathListEditor(None, PathListEditorConfig())
path_list_frame.show()
app.exec_()
print(path_list_frame.get_path_list())
