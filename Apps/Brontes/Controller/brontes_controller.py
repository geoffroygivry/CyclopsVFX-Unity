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

from Apps.Brontes.View import brontes_main_ui as b_UI
from Apps.Brontes.View import type_widget_ui as type_widget
from Apps.Brontes.View import asset_widget_ui as asset_widget


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



class Brontes(QtWidgets.QWidget, b_UI.Ui_brontes_main):
    # main window UI
    def __init__(self):
        super(Brontes, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.populate_typeWidget()
        self.populate_assets()

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
            wid2.setSizeHint(QtCore.QSize(120, 40))
            self.types_listWidget.addItem(wid2)
            self.types_listWidget.setItemWidget(wid2, type_wid)

    def populate_assets(self):
        asset_wid = Asset_widget()
        wid2 = QtWidgets.QListWidgetItem()
        wid2.setSizeHint(QtCore.QSize(150, 140))
        self.asset_listWidget.addItem(wid2)
        self.asset_listWidget.setItemWidget(wid2, asset_wid)


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
