# Form implementation generated from reading ui file 'C:\Users\zyzz_\Projects\PyGUIAdapter\designer\selection_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SelectionWindow(object):
    def setupUi(self, SelectionWindow):
        SelectionWindow.setObjectName("SelectionWindow")
        SelectionWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=SelectionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_func_list = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_func_list.setObjectName("label_func_list")
        self.verticalLayout.addWidget(self.label_func_list)
        self.listwidget_functions = QtWidgets.QListWidget(parent=self.layoutWidget)
        self.listwidget_functions.setObjectName("listwidget_functions")
        self.verticalLayout.addWidget(self.listwidget_functions)
        self.hlayout_bottom = QtWidgets.QHBoxLayout()
        self.hlayout_bottom.setObjectName("hlayout_bottom")
        self.button_select = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.button_select.setObjectName("button_select")
        self.hlayout_bottom.addWidget(self.button_select)
        self.verticalLayout.addLayout(self.hlayout_bottom)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.vlayout_right = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.vlayout_right.setContentsMargins(0, 0, 0, 0)
        self.vlayout_right.setObjectName("vlayout_right")
        self.label_document = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.label_document.setObjectName("label_document")
        self.vlayout_right.addWidget(self.label_document)
        self.textedit_document = QtWidgets.QTextBrowser(parent=self.layoutWidget1)
        self.textedit_document.setObjectName("textedit_document")
        self.vlayout_right.addWidget(self.textedit_document)
        self.verticalLayout_2.addWidget(self.splitter)
        SelectionWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=SelectionWindow)
        self.statusbar.setObjectName("statusbar")
        SelectionWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SelectionWindow)
        QtCore.QMetaObject.connectSlotsByName(SelectionWindow)

    def retranslateUi(self, SelectionWindow):
        _translate = QtCore.QCoreApplication.translate
        SelectionWindow.setWindowTitle(_translate("SelectionWindow", "Select Function"))
        self.label_func_list.setText(_translate("SelectionWindow", "Functions"))
        self.button_select.setText(_translate("SelectionWindow", "Select"))
        self.label_document.setText(_translate("SelectionWindow", "Documentation"))
