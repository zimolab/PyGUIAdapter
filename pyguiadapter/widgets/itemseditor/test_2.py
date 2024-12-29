from qtpy.QtWidgets import QApplication


from pyguiadapter.widgets.itemseditor.paths_editor import PathsEditor, PathsEditorConfig


app = QApplication([])
config = PathsEditorConfig()
editor = PathsEditor(None, config)
editor.resize(800, 600)
editor.show()
app.exec_()
print(editor.get_paths())
