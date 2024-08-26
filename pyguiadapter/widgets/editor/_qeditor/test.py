from qtpy.QtWidgets import QApplication
from pyguiadapter.widgets.editor._qeditor.QCodeEditor import QCodeEditor

app = QApplication([])

editor = QCodeEditor()
editor.setPlainText("{}")
editor.show()

app.exec_()
