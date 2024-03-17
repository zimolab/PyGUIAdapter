# Form implementation generated from reading ui file 'D:\Projects\PyGUIAdapter\designer\execution_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ExecutionWindow(object):
    def setupUi(self, ExecutionWindow):
        ExecutionWindow.setObjectName("ExecutionWindow")
        ExecutionWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=ExecutionWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupbox_parameters = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupbox_parameters.setEnabled(True)
        self.groupbox_parameters.setFlat(False)
        self.groupbox_parameters.setCheckable(False)
        self.groupbox_parameters.setObjectName("groupbox_parameters")
        self.vlayout_4 = QtWidgets.QVBoxLayout(self.groupbox_parameters)
        self.vlayout_4.setContentsMargins(2, 2, 2, 2)
        self.vlayout_4.setSpacing(0)
        self.vlayout_4.setObjectName("vlayout_4")
        self.scrollarea = QtWidgets.QScrollArea(parent=self.groupbox_parameters)
        self.scrollarea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setObjectName("scrollarea")
        self.scrollarea_content = QtWidgets.QWidget()
        self.scrollarea_content.setGeometry(QtCore.QRect(0, 0, 507, 445))
        self.scrollarea_content.setObjectName("scrollarea_content")
        self.scrollarea.setWidget(self.scrollarea_content)
        self.vlayout_4.addWidget(self.scrollarea)
        self.verticalLayout_5.addWidget(self.groupbox_parameters)
        self.groupbox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupbox.setTitle("")
        self.groupbox.setObjectName("groupbox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupbox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkbox_auto_clear = QtWidgets.QCheckBox(parent=self.groupbox)
        self.checkbox_auto_clear.setObjectName("checkbox_auto_clear")
        self.verticalLayout.addWidget(self.checkbox_auto_clear)
        self.hlayout_1 = QtWidgets.QHBoxLayout()
        self.hlayout_1.setObjectName("hlayout_1")
        self.button_execute = QtWidgets.QPushButton(parent=self.groupbox)
        self.button_execute.setObjectName("button_execute")
        self.hlayout_1.addWidget(self.button_execute)
        self.button_clear = QtWidgets.QPushButton(parent=self.groupbox)
        self.button_clear.setObjectName("button_clear")
        self.hlayout_1.addWidget(self.button_clear)
        self.verticalLayout.addLayout(self.hlayout_1)
        self.verticalLayout_5.addWidget(self.groupbox)
        ExecutionWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=ExecutionWindow)
        self.statusbar.setObjectName("statusbar")
        ExecutionWindow.setStatusBar(self.statusbar)
        self.dockwidget_document = QtWidgets.QDockWidget(parent=ExecutionWindow)
        self.dockwidget_document.setObjectName("dockwidget_document")
        self.dockwidget_content_2 = QtWidgets.QWidget()
        self.dockwidget_content_2.setObjectName("dockwidget_content_2")
        self.vlayout_2 = QtWidgets.QVBoxLayout(self.dockwidget_content_2)
        self.vlayout_2.setContentsMargins(2, 2, 2, 5)
        self.vlayout_2.setSpacing(2)
        self.vlayout_2.setObjectName("vlayout_2")
        self.textedit_document = QtWidgets.QTextEdit(parent=self.dockwidget_content_2)
        self.textedit_document.setReadOnly(True)
        self.textedit_document.setObjectName("textedit_document")
        self.vlayout_2.addWidget(self.textedit_document)
        self.dockwidget_document.setWidget(self.dockwidget_content_2)
        ExecutionWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockwidget_document)
        self.dockwidget_output = QtWidgets.QDockWidget(parent=ExecutionWindow)
        self.dockwidget_output.setObjectName("dockwidget_output")
        self.dockwidget_content = QtWidgets.QWidget()
        self.dockwidget_content.setObjectName("dockwidget_content")
        self.vlayout_3 = QtWidgets.QVBoxLayout(self.dockwidget_content)
        self.vlayout_3.setContentsMargins(2, 2, 2, 5)
        self.vlayout_3.setSpacing(2)
        self.vlayout_3.setObjectName("vlayout_3")
        self.textedit_output = QtWidgets.QTextEdit(parent=self.dockwidget_content)
        self.textedit_output.setObjectName("textedit_output")
        self.vlayout_3.addWidget(self.textedit_output)
        self.dockwidget_output.setWidget(self.dockwidget_content)
        ExecutionWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockwidget_output)
        self.action_output_view = QtGui.QAction(parent=ExecutionWindow)
        self.action_output_view.setCheckable(True)
        self.action_output_view.setChecked(True)
        self.action_output_view.setObjectName("action_output_view")
        self.action_document_view = QtGui.QAction(parent=ExecutionWindow)
        self.action_document_view.setCheckable(True)
        self.action_document_view.setChecked(True)
        self.action_document_view.setObjectName("action_document_view")
        self.actionAbout = QtGui.QAction(parent=ExecutionWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtGui.QAction(parent=ExecutionWindow)
        self.actionHelp.setObjectName("actionHelp")

        self.retranslateUi(ExecutionWindow)
        QtCore.QMetaObject.connectSlotsByName(ExecutionWindow)

    def retranslateUi(self, ExecutionWindow):
        _translate = QtCore.QCoreApplication.translate
        ExecutionWindow.setWindowTitle(_translate("ExecutionWindow", "Function Execution"))
        self.groupbox_parameters.setTitle(_translate("ExecutionWindow", "Parameters"))
        self.checkbox_auto_clear.setText(_translate("ExecutionWindow", "clear output before execution"))
        self.button_execute.setText(_translate("ExecutionWindow", "Execute"))
        self.button_clear.setText(_translate("ExecutionWindow", "Clear Output"))
        self.dockwidget_document.setWindowTitle(_translate("ExecutionWindow", "Document"))
        self.dockwidget_output.setWindowTitle(_translate("ExecutionWindow", "Output"))
        self.action_output_view.setText(_translate("ExecutionWindow", "Output View"))
        self.action_document_view.setText(_translate("ExecutionWindow", "Document View"))
        self.actionAbout.setText(_translate("ExecutionWindow", "About"))
        self.actionHelp.setText(_translate("ExecutionWindow", "Help"))
