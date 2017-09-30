# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Apps/Brontes/View/asset_widget.ui'
#
# Created: Sat Sep 30 22:14:53 2017
#      by: pyside-uic 0.2.13 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Asset_Widget(object):
    def setupUi(self, Asset_Widget):
        Asset_Widget.setObjectName("Asset_Widget")
        Asset_Widget.resize(576, 71)
        self.horizontalLayout = QtGui.QHBoxLayout(Asset_Widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = QtGui.QLabel(Asset_Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QtCore.QSize(50, 50))
        self.icon.setMaximumSize(QtCore.QSize(100, 150))
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap("../../../../../home/ggivry/Documents/icon.PNG"))
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)
        self.Main_gridLayout = QtGui.QGridLayout()
        self.Main_gridLayout.setHorizontalSpacing(6)
        self.Main_gridLayout.setObjectName("Main_gridLayout")
        self.userName = QtGui.QLabel(Asset_Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userName.sizePolicy().hasHeightForWidth())
        self.userName.setSizePolicy(sizePolicy)
        self.userName.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setItalic(True)
        self.userName.setFont(font)
        self.userName.setObjectName("userName")
        self.Main_gridLayout.addWidget(self.userName, 1, 1, 1, 1)
        self.name = QtGui.QLabel(Asset_Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.name.setFont(font)
        self.name.setStyleSheet("color: rgb(125, 125, 125)")
        self.name.setObjectName("name")
        self.Main_gridLayout.addWidget(self.name, 2, 2, 1, 1)
        self.task = QtGui.QLabel(Asset_Widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.task.setFont(font)
        self.task.setObjectName("task")
        self.Main_gridLayout.addWidget(self.task, 2, 1, 1, 1)
        self.frame_range_data = QtGui.QLabel(Asset_Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_range_data.sizePolicy().hasHeightForWidth())
        self.frame_range_data.setSizePolicy(sizePolicy)
        self.frame_range_data.setMinimumSize(QtCore.QSize(90, 0))
        self.frame_range_data.setObjectName("frame_range_data")
        self.Main_gridLayout.addWidget(self.frame_range_data, 2, 3, 1, 1)
        self.version_data = QtGui.QLabel(Asset_Widget)
        self.version_data.setObjectName("version_data")
        self.Main_gridLayout.addWidget(self.version_data, 2, 4, 1, 1)
        self.entity_name_label = QtGui.QLabel(Asset_Widget)
        self.entity_name_label.setObjectName("entity_name_label")
        self.Main_gridLayout.addWidget(self.entity_name_label, 1, 2, 1, 1)
        self.frame_range_label = QtGui.QLabel(Asset_Widget)
        self.frame_range_label.setObjectName("frame_range_label")
        self.Main_gridLayout.addWidget(self.frame_range_label, 1, 3, 1, 1)
        self.version_label = QtGui.QLabel(Asset_Widget)
        self.version_label.setObjectName("version_label")
        self.Main_gridLayout.addWidget(self.version_label, 1, 4, 1, 1)
        self.date = QtGui.QLabel(Asset_Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.date.sizePolicy().hasHeightForWidth())
        self.date.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setWeight(75)
        font.setBold(True)
        self.date.setFont(font)
        self.date.setStyleSheet("color: rgb(49, 131, 219)")
        self.date.setObjectName("date")
        self.Main_gridLayout.addWidget(self.date, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.Main_gridLayout)

        self.retranslateUi(Asset_Widget)
        QtCore.QMetaObject.connectSlotsByName(Asset_Widget)

    def retranslateUi(self, Asset_Widget):
        Asset_Widget.setWindowTitle(QtGui.QApplication.translate("Asset_Widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.userName.setText(QtGui.QApplication.translate("Asset_Widget", "Geoffroy", None, QtGui.QApplication.UnicodeUTF8))
        self.name.setText(QtGui.QApplication.translate("Asset_Widget", "lgt_ManorHouse", None, QtGui.QApplication.UnicodeUTF8))
        self.task.setText(QtGui.QApplication.translate("Asset_Widget", "LGT", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_range_data.setText(QtGui.QApplication.translate("Asset_Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1001-1076</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.version_data.setText(QtGui.QApplication.translate("Asset_Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">v01</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.entity_name_label.setText(QtGui.QApplication.translate("Asset_Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7pt; color:#646464;\">name:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_range_label.setText(QtGui.QApplication.translate("Asset_Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7pt; color:#646464;\">Frame range</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.version_label.setText(QtGui.QApplication.translate("Asset_Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7pt; color:#646464;\">version:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.date.setText(QtGui.QApplication.translate("Asset_Widget", "22/11/2017 at 11:30 by", None, QtGui.QApplication.UnicodeUTF8))

