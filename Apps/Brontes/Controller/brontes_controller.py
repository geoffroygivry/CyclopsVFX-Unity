# The MIT License (MIT)
#
# Copyright (c) 2017 Geoffroy Givry
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os


try:
    # < Nuke 11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtWidgets
    import PySide.QtUiTools as QtUiTools
except ImportError:
    # >= Nuke 11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtUiTools as QtUiTools

from Apps.Brontes.Model import hydra_model as hm
from Apps.Brontes.View import brontes_main_ui as b_UI
from Apps.Brontes.View import type_widget_ui as type_widget
from Apps.Brontes.View import asset_widget_ui as asset_widget
from Apps.Brontes.View import MainStyleSheet


class Type_widget(QtWidgets.QWidget, type_widget.Ui_type_widget):
    # creation of our custom widget based on type_widget UI
    def __init__(self):
        super(Type_widget, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

    def set_text(self, text):
        self.type_label.setText(text)

    def set_icon(self, icon):
        self.type_icon.setPixmap(QtGui.QPixmap(icon))


class Asset_widget(QtWidgets.QWidget, asset_widget.Ui_Asset_Widget):
    # creation of our custom widget based on asset_widget UI
    def __init__(self):
        super(Asset_widget, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

    def set_username(self, text):
        self.userName.setText(text)

    def set_date(self, text):
        self.date.setText(text)

    def set_task(self, text):
        self.task.setText(text)

    def set_name(self, text):
        self.name.setText(text)

    def set_frameRange(self, first, last):
        self.frame_range_data.setText("{}-{}".format(first, last))

    def set_version(self, text):
        self.version_data("v{}".format(text))


class Brontes(QtWidgets.QWidget, b_UI.Ui_brontes_main):
    # main window UI
    def __init__(self):
        super(Brontes, self).__init__()
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.Model = hm.Model()
        self.populate_typeWidget()
        self.populate_entities()
        self.get_type_asset()

        self.populate_shows()  # populates list of actives shows in the show combobox
        self.populate_seqs()  # populates list of sequences in the seq combobox
        self.populate_shots()  # populates list of shots in the shot combobox

        self.asset_listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.cyc_icon.setPixmap(QtGui.QPixmap(
                                os.path.join(os.getenv("CYC_CORE_PATH"),
                                             "icons", "cyc_small.png")))
        self.search_button.setIcon(QtGui.QPixmap(
            os.path.join(os.getenv("CYC_CORE_PATH"),
                         "icons", "search.png")))

        MainStyleSheet.setStyleSheet(self)

        # Signals
        self.types_listWidget.currentItemChanged.connect(self.populate_entities)
        self.show_comboBox.currentIndexChanged.connect(self.populate_seqs)
        self.seq_comboBox.currentIndexChanged.connect(self.populate_shots)

    def populate_typeWidget(self):
        type_dict = {"All": "all_icon.png", "Cam": "cam_icon.png",
                     "Layout": "layout_icon.png", "CG": "lgt_icon.png",
                     "3D": "3D_icon.png", "Libs": "library_icon.png"}

        # populating The left widget list part with different types of assets.
        for n, v in type_dict.iteritems():
            icon_all = os.path.join(os.getenv("CYC_CORE_PATH"), "icons", v)
            type_wid = Type_widget()
            type_wid.set_text(n)
            type_wid.set_icon(icon_all)
            wid2 = QtWidgets.QListWidgetItem()
            wid2.setSizeHint(type_wid.sizeHint())
            self.types_listWidget.addItem(wid2)
            self.types_listWidget.setContentsMargins(100, 100, 100, 100)
            self.types_listWidget.setItemWidget(wid2, type_wid)

    def populate_entities(self):
        type_asset = self.get_type_asset()
        if type_asset == "All":
            if self.latest_checkBox.isChecked():
                assets = self.Model.get_all_latest_publish_shot()
                print assets
        # for n in range(3):
        #     asset_wid = Asset_widget()
        #     wid2 = QtWidgets.QListWidgetItem()
        #     asset_wid.setProperty("asset", True)
        #     wid2.setSizeHint(QtCore.QSize(110, 90))
        #     self.asset_listWidget.addItem(wid2)
        #     self.asset_listWidget.setItemWidget(wid2, asset_wid)
        #     self.asset_listWidget.setStyleSheet("QListWidget::item {margin-bottom: 4px; background-color: rgb(45,45,45);}")
        #     wid2.setBackground(QtGui.QColor(45, 45, 45))

    def get_type_asset(self):
        selected_type_widget = self.types_listWidget.itemWidget(self.types_listWidget.currentItem())
        if selected_type_widget is not None:
            return selected_type_widget.type_label.text()

    def populate_shows(self):
        shows = self.Model.get_active_shows()
        self.show_comboBox.addItems(shows)
        self.show_comboBox.setCurrentIndex(shows.index(os.getenv('SHOW')))

    def populate_seqs(self):
        seqs = self.Model.get_seqs(self.show_comboBox.currentText())
        self.seq_comboBox.addItems(seqs)
        self.seq_comboBox.setCurrentIndex(seqs.index(os.getenv('SEQ')))

    def populate_shots(self):
        shots = self.Model.get_shots(self.show_comboBox.currentText(), self.seq_comboBox.currentText())
        self.shot_comboBox.addItems(shots)
        self.shot_comboBox.setCurrentIndex(shots.index(os.getenv('SHOT')))


def float_in_nuke():
    float_in_nuke.panel = Brontes()
    float_in_nuke.panel.show()


def dock_in_nuke():
    import nuke
    from nukescripts import panels
    pane = nuke.getPaneFor("io.cyclopsvfx.Brontes")
    panels.registerWidgetAsPanel('brontes_controller.Brontes', 'Brontes',
                                 'io.cyclopsvfx.Brontes', True).addToPane(pane)


def runStandalone():
    app = QtWidgets.QApplication(sys.argv)
    panel = Brontes()
    panel.show()
    app.exec_()


if __name__ == "__main__":
    runStandalone()

# to run it within nuke:
# from Apps.Brontes.Controller import brontes_controller
# brontes_controller.dock_in_nuke()
