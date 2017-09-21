# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'type_widget.ui'
#
# Created: Wed Sep 20 21:34:18 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_type_widget(object):
    def setupUi(self, type_widget):
        type_widget.setObjectName("type_widget")
        type_widget.resize(248, 78)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(type_widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.type_icon = QtWidgets.QLabel(type_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_icon.sizePolicy().hasHeightForWidth())
        self.type_icon.setSizePolicy(sizePolicy)
        self.type_icon.setObjectName("type_icon")
        self.horizontalLayout_2.addWidget(self.type_icon)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.line = QtWidgets.QFrame(type_widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.type_label = QtWidgets.QLabel(type_widget)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.type_label.setFont(font)
        self.type_label.setObjectName("type_label")
        self.horizontalLayout_2.addWidget(self.type_label)

        self.retranslateUi(type_widget)
        QtCore.QMetaObject.connectSlotsByName(type_widget)

    def retranslateUi(self, type_widget):
        type_widget.setWindowTitle(QtWidgets.QApplication.translate("type_widget", "Form", None, -1))
        self.type_icon.setText(QtWidgets.QApplication.translate("type_widget", "icon", None, -1))
        self.type_label.setText(QtWidgets.QApplication.translate("type_widget", "Type Label", None, -1))

