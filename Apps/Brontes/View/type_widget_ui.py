# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Apps/Brontes/View/type_widget.ui'
#
# Created: Thu Sep 28 22:10:21 2017
#      by: pyside-uic 0.2.13 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_type_widget(object):
    def setupUi(self, type_widget):
        type_widget.setObjectName("type_widget")
        type_widget.resize(248, 78)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(type_widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.type_icon = QtGui.QLabel(type_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_icon.sizePolicy().hasHeightForWidth())
        self.type_icon.setSizePolicy(sizePolicy)
        self.type_icon.setObjectName("type_icon")
        self.horizontalLayout_2.addWidget(self.type_icon)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.line = QtGui.QFrame(type_widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.type_label = QtGui.QLabel(type_widget)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.type_label.setFont(font)
        self.type_label.setObjectName("type_label")
        self.horizontalLayout_2.addWidget(self.type_label)

        self.retranslateUi(type_widget)
        QtCore.QMetaObject.connectSlotsByName(type_widget)

    def retranslateUi(self, type_widget):
        type_widget.setWindowTitle(QtGui.QApplication.translate("type_widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.type_icon.setText(QtGui.QApplication.translate("type_widget", "icon", None, QtGui.QApplication.UnicodeUTF8))
        self.type_label.setText(QtGui.QApplication.translate("type_widget", "Type Label", None, QtGui.QApplication.UnicodeUTF8))

