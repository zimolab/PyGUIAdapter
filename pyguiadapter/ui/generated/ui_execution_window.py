# Form implementation generated from reading ui file 'C:\Users\zyzz_\Projects\PyGUIAdapter\designer\execution_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupbox_params = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupbox_params.setEnabled(True)
        self.groupbox_params.setFlat(False)
        self.groupbox_params.setCheckable(False)
        self.groupbox_params.setObjectName("groupbox_params")
        self.vlayout_4 = QtWidgets.QVBoxLayout(self.groupbox_params)
        self.vlayout_4.setContentsMargins(2, 2, 2, 2)
        self.vlayout_4.setSpacing(0)
        self.vlayout_4.setObjectName("vlayout_4")
        self.scrollarea = QtWidgets.QScrollArea(parent=self.groupbox_params)
        self.scrollarea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setObjectName("scrollarea")
        self.scrollarea_content = QtWidgets.QWidget()
        self.scrollarea_content.setGeometry(QtCore.QRect(0, 0, 512, 452))
        self.scrollarea_content.setObjectName("scrollarea_content")
        self.scrollarea.setWidget(self.scrollarea_content)
        self.vlayout_4.addWidget(self.scrollarea)
        self.verticalLayout.addWidget(self.groupbox_params)
        self.checkbox_autoclear = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkbox_autoclear.setObjectName("checkbox_autoclear")
        self.verticalLayout.addWidget(self.checkbox_autoclear)
        self.hlayout_1 = QtWidgets.QHBoxLayout()
        self.hlayout_1.setObjectName("hlayout_1")
        self.button_execute = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_execute.setObjectName("button_execute")
        self.hlayout_1.addWidget(self.button_execute)
        self.button_cancel = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_cancel.setObjectName("button_cancel")
        self.hlayout_1.addWidget(self.button_cancel)
        self.button_clear = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_clear.setObjectName("button_clear")
        self.hlayout_1.addWidget(self.button_clear)
        self.verticalLayout.addLayout(self.hlayout_1)
        ExecutionWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=ExecutionWindow)
        self.statusbar.setObjectName("statusbar")
        ExecutionWindow.setStatusBar(self.statusbar)
        self.dockwidget_output = QtWidgets.QDockWidget(parent=ExecutionWindow)
        self.dockwidget_output.setObjectName("dockwidget_output")
        self.dockwidget_content = QtWidgets.QWidget()
        self.dockwidget_content.setObjectName("dockwidget_content")
        self.vlayout_3 = QtWidgets.QVBoxLayout(self.dockwidget_content)
        self.vlayout_3.setContentsMargins(2, 2, 2, 5)
        self.vlayout_3.setSpacing(2)
        self.vlayout_3.setObjectName("vlayout_3")
        self.textedit_output = QtWidgets.QTextBrowser(parent=self.dockwidget_content)
        self.textedit_output.setObjectName("textedit_output")
        self.vlayout_3.addWidget(self.textedit_output)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.progressbar_progress = QtWidgets.QProgressBar(parent=self.dockwidget_content)
        self.progressbar_progress.setProperty("value", 24)
        self.progressbar_progress.setObjectName("progressbar_progress")
        self.verticalLayout_2.addWidget(self.progressbar_progress)
        self.label_progress_text = QtWidgets.QLabel(parent=self.dockwidget_content)
        self.label_progress_text.setText("")
        self.label_progress_text.setScaledContents(False)
        self.label_progress_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_progress_text.setWordWrap(True)
        self.label_progress_text.setOpenExternalLinks(True)
        self.label_progress_text.setObjectName("label_progress_text")
        self.verticalLayout_2.addWidget(self.label_progress_text)
        self.vlayout_3.addLayout(self.verticalLayout_2)
        self.dockwidget_output.setWidget(self.dockwidget_content)
        ExecutionWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockwidget_output)
        self.dockwidget_document = QtWidgets.QDockWidget(parent=ExecutionWindow)
        self.dockwidget_document.setObjectName("dockwidget_document")
        self.dockwidget_content_2 = QtWidgets.QWidget()
        self.dockwidget_content_2.setObjectName("dockwidget_content_2")
        self.vlayout_2 = QtWidgets.QVBoxLayout(self.dockwidget_content_2)
        self.vlayout_2.setContentsMargins(2, 2, 2, 5)
        self.vlayout_2.setSpacing(2)
        self.vlayout_2.setObjectName("vlayout_2")
        self.textedit_document = QtWidgets.QTextBrowser(parent=self.dockwidget_content_2)
        self.textedit_document.setObjectName("textedit_document")
        self.vlayout_2.addWidget(self.textedit_document)
        self.dockwidget_document.setWidget(self.dockwidget_content_2)
        ExecutionWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockwidget_document)
        self.toolbar = QtWidgets.QToolBar(parent=ExecutionWindow)
        self.toolbar.setObjectName("toolbar")
        ExecutionWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.menubar = QtWidgets.QMenuBar(parent=ExecutionWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        ExecutionWindow.setMenuBar(self.menubar)
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
        self.groupbox_params.setTitle(_translate("ExecutionWindow", "Parameters"))
        self.checkbox_autoclear.setText(_translate("ExecutionWindow", "clear output before execution"))
        self.button_execute.setText(_translate("ExecutionWindow", "Execute"))
        self.button_cancel.setText(_translate("ExecutionWindow", "Cancel"))
        self.button_clear.setText(_translate("ExecutionWindow", "Clear Output"))
        self.dockwidget_output.setWindowTitle(_translate("ExecutionWindow", "Output"))
        self.dockwidget_document.setWindowTitle(_translate("ExecutionWindow", "Document"))
        self.toolbar.setWindowTitle(_translate("ExecutionWindow", "toolBar"))
        self.action_output_view.setText(_translate("ExecutionWindow", "Output View"))
        self.action_document_view.setText(_translate("ExecutionWindow", "Document View"))
        self.actionAbout.setText(_translate("ExecutionWindow", "About"))
        self.actionHelp.setText(_translate("ExecutionWindow", "Help"))
