# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Brontes_main_v02.ui'
#
# Created: Thu Nov 16 19:08:20 2017
#      by: pyside-uic 0.2.13 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_brontes_main(object):
    def setupUi(self, brontes_main):
        brontes_main.setObjectName("brontes_main")
        brontes_main.resize(996, 698)
        self.verticalLayout_2 = QtGui.QVBoxLayout(brontes_main)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.top_vertical_layout = QtGui.QVBoxLayout()
        self.top_vertical_layout.setObjectName("top_vertical_layout")
        self.top_horizontal_layout = QtGui.QHBoxLayout()
        self.top_horizontal_layout.setObjectName("top_horizontal_layout")
        self.cyc_icon = QtGui.QLabel(brontes_main)
        self.cyc_icon.setMaximumSize(QtCore.QSize(150, 16777215))
        self.cyc_icon.setText("")
        self.cyc_icon.setPixmap(QtGui.QPixmap("../../../../../../../../../../../../../../../../../../../../../../../../Core/config/icons/cyc_small.png"))
        self.cyc_icon.setObjectName("cyc_icon")
        self.top_horizontal_layout.addWidget(self.cyc_icon)
        self.vertical_divider = QtGui.QFrame(brontes_main)
        self.vertical_divider.setFrameShape(QtGui.QFrame.VLine)
        self.vertical_divider.setFrameShadow(QtGui.QFrame.Sunken)
        self.vertical_divider.setObjectName("vertical_divider")
        self.top_horizontal_layout.addWidget(self.vertical_divider)
        self.show_shot_layout = QtGui.QFormLayout()
        self.show_shot_layout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.show_shot_layout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.show_shot_layout.setHorizontalSpacing(10)
        self.show_shot_layout.setObjectName("show_shot_layout")
        self.show_label = QtGui.QLabel(brontes_main)
        self.show_label.setObjectName("show_label")
        self.show_shot_layout.setWidget(0, QtGui.QFormLayout.LabelRole, self.show_label)
        self.show_comboBox = QtGui.QComboBox(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_comboBox.sizePolicy().hasHeightForWidth())
        self.show_comboBox.setSizePolicy(sizePolicy)
        self.show_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.show_comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.show_comboBox.setObjectName("show_comboBox")
        self.show_shot_layout.setWidget(0, QtGui.QFormLayout.FieldRole, self.show_comboBox)
        self.seq_label = QtGui.QLabel(brontes_main)
        self.seq_label.setObjectName("seq_label")
        self.show_shot_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.seq_label)
        self.seq_comboBox = QtGui.QComboBox(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seq_comboBox.sizePolicy().hasHeightForWidth())
        self.seq_comboBox.setSizePolicy(sizePolicy)
        self.seq_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.seq_comboBox.setObjectName("seq_comboBox")
        self.show_shot_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.seq_comboBox)
        self.shot_label = QtGui.QLabel(brontes_main)
        self.shot_label.setObjectName("shot_label")
        self.show_shot_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.shot_label)
        self.shot_comboBox = QtGui.QComboBox(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shot_comboBox.sizePolicy().hasHeightForWidth())
        self.shot_comboBox.setSizePolicy(sizePolicy)
        self.shot_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.shot_comboBox.setObjectName("shot_comboBox")
        self.show_shot_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.shot_comboBox)
        self.top_horizontal_layout.addLayout(self.show_shot_layout)
        spacerItem = QtGui.QSpacerItem(250, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.top_horizontal_layout.addItem(spacerItem)
        self.top_vertical_layout.addLayout(self.top_horizontal_layout)
        self.verticalLayout_2.addLayout(self.top_vertical_layout)
        self.divider_top = QtGui.QFrame(brontes_main)
        self.divider_top.setFrameShape(QtGui.QFrame.HLine)
        self.divider_top.setFrameShadow(QtGui.QFrame.Sunken)
        self.divider_top.setObjectName("divider_top")
        self.verticalLayout_2.addWidget(self.divider_top)
        self.mid_horizontal_layout = QtGui.QHBoxLayout()
        self.mid_horizontal_layout.setObjectName("mid_horizontal_layout")
        self.poly_label = QtGui.QLabel(brontes_main)
        self.poly_label.setObjectName("poly_label")
        self.mid_horizontal_layout.addWidget(self.poly_label)
        self.poly_lineEdit = QtGui.QLineEdit(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poly_lineEdit.sizePolicy().hasHeightForWidth())
        self.poly_lineEdit.setSizePolicy(sizePolicy)
        self.poly_lineEdit.setMinimumSize(QtCore.QSize(500, 0))
        self.poly_lineEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.poly_lineEdit.setSizeIncrement(QtCore.QSize(0, 35))
        self.poly_lineEdit.setBaseSize(QtCore.QSize(0, 12))
        self.poly_lineEdit.setObjectName("poly_lineEdit")
        self.mid_horizontal_layout.addWidget(self.poly_lineEdit)
        self.latest_checkBox = QtGui.QCheckBox(brontes_main)
        self.latest_checkBox.setChecked(True)
        self.latest_checkBox.setObjectName("latest_checkBox")
        self.mid_horizontal_layout.addWidget(self.latest_checkBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mid_horizontal_layout.addItem(spacerItem1)
        self.search_lineEdit = QtGui.QLineEdit(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_lineEdit.setSizePolicy(sizePolicy)
        self.search_lineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.search_lineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.search_lineEdit.setObjectName("search_lineEdit")
        self.mid_horizontal_layout.addWidget(self.search_lineEdit)
        self.search_button = QtGui.QToolButton(brontes_main)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../../../../../../../../../../../../../../../../../../Core/config/icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon)
        self.search_button.setObjectName("search_button")
        self.mid_horizontal_layout.addWidget(self.search_button)
        self.verticalLayout_2.addLayout(self.mid_horizontal_layout)
        self.divider = QtGui.QFrame(brontes_main)
        self.divider.setFrameShape(QtGui.QFrame.HLine)
        self.divider.setFrameShadow(QtGui.QFrame.Sunken)
        self.divider.setObjectName("divider")
        self.verticalLayout_2.addWidget(self.divider)
        self.bottom_verticalLayout = QtGui.QVBoxLayout()
        self.bottom_verticalLayout.setObjectName("bottom_verticalLayout")
        self.bottom_horizontalLayout = QtGui.QHBoxLayout()
        self.bottom_horizontalLayout.setObjectName("bottom_horizontalLayout")
        self.types_tabWidget = QtGui.QTabWidget(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.types_tabWidget.sizePolicy().hasHeightForWidth())
        self.types_tabWidget.setSizePolicy(sizePolicy)
        self.types_tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.types_tabWidget.setObjectName("types_tabWidget")
        self.assets_tab = QtGui.QWidget()
        self.assets_tab.setObjectName("assets_tab")
        self.horizontalLayout = QtGui.QHBoxLayout(self.assets_tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.assets_type_listWidget = QtGui.QListWidget(self.assets_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assets_type_listWidget.sizePolicy().hasHeightForWidth())
        self.assets_type_listWidget.setSizePolicy(sizePolicy)
        self.assets_type_listWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.assets_type_listWidget.setSizeIncrement(QtCore.QSize(10, 0))
        self.assets_type_listWidget.setBaseSize(QtCore.QSize(10, 0))
        self.assets_type_listWidget.setObjectName("assets_type_listWidget")
        self.horizontalLayout.addWidget(self.assets_type_listWidget)
        self.types_tabWidget.addTab(self.assets_tab, "")
        self.shot_tab = QtGui.QWidget()
        self.shot_tab.setObjectName("shot_tab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.shot_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.shot_type_listWidget = QtGui.QListWidget(self.shot_tab)
        self.shot_type_listWidget.setObjectName("shot_type_listWidget")
        self.verticalLayout_3.addWidget(self.shot_type_listWidget)
        self.types_tabWidget.addTab(self.shot_tab, "")
        self.libs_tab = QtGui.QWidget()
        self.libs_tab.setObjectName("libs_tab")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.libs_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.libs_listWidget = QtGui.QListWidget(self.libs_tab)
        self.libs_listWidget.setObjectName("libs_listWidget")
        self.verticalLayout_5.addWidget(self.libs_listWidget)
        self.types_tabWidget.addTab(self.libs_tab, "")
        self.bottom_horizontalLayout.addWidget(self.types_tabWidget)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.asset_listWidget = QtGui.QListWidget(brontes_main)
        self.asset_listWidget.setDragEnabled(True)
        self.asset_listWidget.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.asset_listWidget.setObjectName("asset_listWidget")
        self.verticalLayout_4.addWidget(self.asset_listWidget)
        self.central_icon_verticalLayout = QtGui.QVBoxLayout()
        self.central_icon_verticalLayout.setObjectName("central_icon_verticalLayout")
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.central_icon_verticalLayout.addItem(spacerItem2)
        self.central_icon_label = QtGui.QLabel(brontes_main)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans Mono")
        font.setPointSize(50)
        font.setWeight(75)
        font.setBold(True)
        self.central_icon_label.setFont(font)
        self.central_icon_label.setStyleSheet("color:grey")
        self.central_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.central_icon_label.setObjectName("central_icon_label")
        self.central_icon_verticalLayout.addWidget(self.central_icon_label)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.central_icon_verticalLayout.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.central_icon_verticalLayout)
        self.bottom_textBrowser = QtGui.QTextBrowser(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_textBrowser.sizePolicy().hasHeightForWidth())
        self.bottom_textBrowser.setSizePolicy(sizePolicy)
        self.bottom_textBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
        self.bottom_textBrowser.setObjectName("bottom_textBrowser")
        self.verticalLayout_4.addWidget(self.bottom_textBrowser)
        self.bottom_horizontalLayout.addLayout(self.verticalLayout_4)
        self.Detail_GroupBox = QtGui.QGroupBox(brontes_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Detail_GroupBox.sizePolicy().hasHeightForWidth())
        self.Detail_GroupBox.setSizePolicy(sizePolicy)
        self.Detail_GroupBox.setMaximumSize(QtCore.QSize(500, 16777215))
        self.Detail_GroupBox.setFlat(False)
        self.Detail_GroupBox.setObjectName("Detail_GroupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.Detail_GroupBox)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Version_detail_listWidget = QtGui.QListWidget(self.Detail_GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Version_detail_listWidget.sizePolicy().hasHeightForWidth())
        self.Version_detail_listWidget.setSizePolicy(sizePolicy)
        self.Version_detail_listWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.Version_detail_listWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.Version_detail_listWidget.setObjectName("Version_detail_listWidget")
        self.verticalLayout.addWidget(self.Version_detail_listWidget)
        self.bottom_horizontalLayout.addWidget(self.Detail_GroupBox)
        self.bottom_verticalLayout.addLayout(self.bottom_horizontalLayout)
        self.verticalLayout_2.addLayout(self.bottom_verticalLayout)

        self.retranslateUi(brontes_main)
        self.types_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(brontes_main)

    def retranslateUi(self, brontes_main):
        brontes_main.setWindowTitle(QtGui.QApplication.translate("brontes_main", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.show_label.setText(QtGui.QApplication.translate("brontes_main", "Show", None, QtGui.QApplication.UnicodeUTF8))
        self.seq_label.setText(QtGui.QApplication.translate("brontes_main", "Seq", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_label.setText(QtGui.QApplication.translate("brontes_main", "Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.poly_label.setText(QtGui.QApplication.translate("brontes_main", "Polyphemus ", None, QtGui.QApplication.UnicodeUTF8))
        self.latest_checkBox.setText(QtGui.QApplication.translate("brontes_main", "latest", None, QtGui.QApplication.UnicodeUTF8))
        self.search_button.setText(QtGui.QApplication.translate("brontes_main", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.types_tabWidget.setTabText(self.types_tabWidget.indexOf(self.assets_tab), QtGui.QApplication.translate("brontes_main", "Assets", None, QtGui.QApplication.UnicodeUTF8))
        self.types_tabWidget.setTabText(self.types_tabWidget.indexOf(self.shot_tab), QtGui.QApplication.translate("brontes_main", "Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.types_tabWidget.setTabText(self.types_tabWidget.indexOf(self.libs_tab), QtGui.QApplication.translate("brontes_main", "Libraries", None, QtGui.QApplication.UnicodeUTF8))
        self.central_icon_label.setText(QtGui.QApplication.translate("brontes_main", "CYC", None, QtGui.QApplication.UnicodeUTF8))

