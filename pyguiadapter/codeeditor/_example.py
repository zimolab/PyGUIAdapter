from pyqcodeeditor.highlighters import QPythonHighlighter
from qtpy.QtWidgets import QApplication

from pyguiadapter.codeeditor import (
    CodeEditorWindow,
    CodeEditorConfig,
    PythonFormatter,
)

app = QApplication([])
config = CodeEditorConfig(
    highlighter=QPythonHighlighter,
    formatter=PythonFormatter(),
    file_filters="python(*.py)",
    use_default_menus=True,
    # exclude_default_menus=["Edit", "File"],
    # exclude_default_menu_actions=(
    #     ("File", "Save"),
    #     ("File", "Save as"),
    #     ("Edit", "Select all"),
    # ),
    # exclude_default_toolbar_actions=("Save",),
)
window = CodeEditorWindow(None, config)
window.show()
app.exec_()
