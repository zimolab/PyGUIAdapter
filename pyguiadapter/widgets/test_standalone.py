from qtpy.QtWidgets import QApplication
from pyguiadapter.widgets.codeeditor import (
    CodeEditorConfig,
    CodeEditorWindow,
    PythonCodeFormatter,
)
from pyqcodeeditor.highlighters import QPythonHighlighter
from pyqcodeeditor.completers import QPythonCompleter


if __name__ == "__main__":
    app = QApplication([])
    completer = QPythonCompleter()
    formatter = PythonCodeFormatter()
    config = CodeEditorConfig(
        title="Code Editor",
        highlighter=QPythonHighlighter,
        completer=completer,
        code_formatter=formatter,
    )
    editor = CodeEditorWindow(None, config)
    editor.resize(800, 600)
    editor.show()
    app.exec_()
