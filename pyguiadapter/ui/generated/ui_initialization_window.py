# Form implementation generated from reading ui file 'D:\Projects\PyGUIAdapter\designer\initialization_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InitializationWindow(object):
    def setupUi(self, InitializationWindow):
        InitializationWindow.setObjectName("InitializationWindow")
        InitializationWindow.resize(410, 619)
        self.verticalLayout = QtWidgets.QVBoxLayout(InitializationWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=InitializationWindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(parent=InitializationWindow)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.scrollarea = QtWidgets.QScrollArea(parent=InitializationWindow)
        self.scrollarea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollarea.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setObjectName("scrollarea")
        self.param_widgets_container = QtWidgets.QWidget()
        self.param_widgets_container.setGeometry(QtCore.QRect(0, 0, 388, 520))
        self.param_widgets_container.setObjectName("param_widgets_container")
        self.scrollarea.setWidget(self.param_widgets_container)
        self.verticalLayout.addWidget(self.scrollarea)
        self.line_2 = QtWidgets.QFrame(parent=InitializationWindow)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.button_initialize = QtWidgets.QPushButton(parent=InitializationWindow)
        self.button_initialize.setObjectName("button_initialize")
        self.verticalLayout.addWidget(self.button_initialize)

        self.retranslateUi(InitializationWindow)
        QtCore.QMetaObject.connectSlotsByName(InitializationWindow)

    def retranslateUi(self, InitializationWindow):
        _translate = QtCore.QCoreApplication.translate
        InitializationWindow.setWindowTitle(_translate("InitializationWindow", "Initialization"))
        self.label.setText(_translate("InitializationWindow", "Initialization Parameters"))
        self.button_initialize.setText(_translate("InitializationWindow", "Initialize"))
