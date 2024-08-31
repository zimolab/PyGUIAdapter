from qtpy.QtWidgets import QApplication
from pyguiadapter.widgets.editor.standalone import CodeEditorConfig, CodeEditor

if __name__ == "__main__":
    app = QApplication([])
    config = CodeEditorConfig(title="Code Editor")
    editor = CodeEditor(None, config)
    editor.resize(800, 600)
    editor.show()
    app.exec_()
