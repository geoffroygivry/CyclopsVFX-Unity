# The MIT License (MIT)
#
# Copyright (c) 2015 Geoffroy Givry
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
import pyseq
from PySide.QtGui import *
from PySide.QtCore import *

from Apps.Steropes.StyleSheet import MainStyleSheet
from Hydra.core import submissions


icon = os.path.join(os.getenv('CYC_ICON'), 'Cyclops.ico')
show = os.getenv('JOB')
shot = os.getenv('SHOT')
task = os.getenv('TASK')
thumbnailPic = os.path.join(os.getenv("CYC_CORE_PATH"), "icons", "icon3d_2.png")


class QCustomQWidget (QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        # self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.iconQLabel.setProperty('labelClass', 'MiniIcon')
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addWidget(self.textUpQLabel, 1)

        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(255, 255, 255);
            font-size : 16px;
            font-weight : bold;
            font-family : Arial;
            background : grey;
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(125, 125, 125);
        ''')
        self.iconQLabel.setStyleSheet('''
            color: rgb(125, 125, 125);
        ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))


class PublishPanel(QWidget):

    """ Steropes Publish Panel """

    def __init__(self):
        super(PublishPanel, self).__init__()

        # creation of the main layout
        mainVertLayout = QVBoxLayout()
        HeaderLayout = QHBoxLayout()

        LabelShow = QLabel("Show:")
        messageShow = '''\
        <font face="Arial" color=grey size=7> {} </font>
        '''.format(show)
        labelShow01 = QLabel(messageShow)

        labelTask = QLabel("Task:")
        messageTask = '''\
        <font face="Arial" color=grey size=5> {} </font>
        '''.format(task)
        labelTask01 = QLabel(messageTask)
        labelLoc = QLabel('Location:')

        cboxLocation = QComboBox(self)
        cboxLocation.addItem(shot)
        self.CurrentShotLoc = unicode(cboxLocation.currentText())

        HeaderLayout.addWidget(LabelShow)
        HeaderLayout.addWidget(labelShow01)
        HeaderLayout.addWidget(labelTask)
        HeaderLayout.addWidget(labelTask01)
        HeaderLayout.addWidget(labelLoc)
        HeaderLayout.addWidget(cboxLocation)

        treeLayout = QHBoxLayout()
        self.treeLayout02 = QVBoxLayout()

        self.model = QFileSystemModel()
        rootPath = os.path.join(os.getenv("DI_ROOT"), 'jobs', show, self.CurrentShotLoc)

        # creation of the treeView
        self.model.setRootPath(unicode(QDir(rootPath)))
        tree = QTreeView()
        tree.setModel(self.model)
        # hiding header fileType and date, showing only the dirs
        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)
        tree.header().hide()

        setDir = QDir(rootPath)
        # setting up the model on the QTreeView
        self.model.setFilter(QDir.Drives | QDir.NoDotAndDotDot | QDir.AllDirs)  # showing Dirs only
        tree.setRootIndex(self.model.index(unicode(QDir.path(setDir))))  # starts at the rootPath variable
        tree.clicked.connect(self.on_treeView_clicked)

        # Layout for the QTreeView
        self.treeLayout02.addWidget(tree)
        treeLayout.addLayout(self.treeLayout02)

        # logo and name of the panel
        LogoLayout = QHBoxLayout()
        cycIcon = QLabel()
        cycIcon.setPixmap(QPixmap(thumbnailPic))
        nameFormat = '''\
        <font face="Arial" color=grey size=12> {} </font>
        '''.format(unicode("Steropes Publish"))
        StePubLabel = QLabel(nameFormat)
        LogoLayout.addWidget(cycIcon)
        LogoLayout.addWidget(StePubLabel)
        # end of logo and name of the panel

        labelSelectFile2Pub = QLabel('Select files to publish:')

        # creation of a model to show Files only on the QListView
        self.listModel = QFileSystemModel()
        self.listModel.setFilter(QDir.Files)  # showing files only

        # Creating the QListView
        self.myQListWidget = QListWidget(self)
        self.myQListWidget.setMinimumHeight(330)
        self.myQListWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.myQListWidget.setModel(self.listModel)

        self.pubPushButton = QPushButton('Publish!')
        self.pubPushButton.setProperty('labelClass', 'pushB')
        self.cancelPushButton = QPushButton('Cancel')
        self.cancelPushButton.setProperty('labelClass', 'pushB')

        labelcomment = QLabel('Comments:')

        self.commentsTextEdit = QTextEdit()
        self.commentsTextEdit.setProperty('labelClass', 'DailiesComment')

        # layout processes

        part2LayoutTree = QVBoxLayout()
        part2LayoutTree.addLayout(LogoLayout)
        part2LayoutTree.addWidget(labelSelectFile2Pub)
        part2LayoutTree.addWidget(self.myQListWidget)
        part2LayoutTree.addWidget(self.pubPushButton)
        part2LayoutTree.addWidget(self.cancelPushButton)
        part2LayoutTree.addWidget(labelcomment)
        part2LayoutTree.addWidget(self.commentsTextEdit)
        treeLayout.addLayout(part2LayoutTree)

        mainVertLayout.addLayout(HeaderLayout)
        mainVertLayout.addLayout(treeLayout)

        self.pubPushButton.clicked.connect(self.goPublish)
        self.cancelPushButton.clicked.connect(self.close)

        self.setLayout(mainVertLayout)
        self.setWindowTitle("Cyclops Publish Panel Submission")
        self.setWindowIcon(QIcon(icon))
        self.setFocus()
        self.setGeometry(100, 100, 1000, 950)
        MainStyleSheet.setStyleSheet(self)
        # text = open("C:/Dropbox/Cyclops/Apps/Steropes/StyleSheet/Style_v02.txt").read()
        # self.setStyleSheet(text)

    def goPublish(self):

        for item in self.myQListWidget.selectedItems():
            pubPath = self.infoWidget[str(item)]['fullPath']
            pubName = self.infoWidget[str(item)]['name']
            commentField = unicode(self.commentsTextEdit.toPlainText())
            submissions.PublishIt(pubName, pubPath, commentField)
        self.close()

    def on_treeView_clicked(self, index):

        # TODO : try to find the solution of being able to publish multi assets from differents locations

        self.clearListWidget()

        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        self.infoWidget = {}

        exrList = []
        nonExrList = []
        self.finalListItems = []

        listimg = os.listdir(filePath)

        for n in listimg:
            if n.split('.')[-1] == 'exr':
                exrList.append(n)
            else:
                nonExrList.append(n)

        if exrList:

            # Create QCustomQWidget
            self.myQCustomQWidget = QCustomQWidget()
            self.myQCustomQWidget.setIcon(os.path.join(os.getenv("CYC_CORE_PATH"), "icons", "rndrIcon2.png"))
            s = pyseq.Sequence(exrList)
            self.myQCustomQWidget.setTextUp(unicode(s))

            # debug:
            fullPathStr = str(filePath) + '/' + str(s)

            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setBackground(QColor('grey'))

            # Set size hint
            myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())

            # set the dictionary keys for the publishing process
            self.infoWidget[str(myQListWidgetItem)] = {'fullPath': fullPathStr, 'name': fullPathStr.split('/')[-1].split('.')[0]}

            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, self.myQCustomQWidget)

        elif nonExrList:
            # Create QCustomQWidget

            for n in nonExrList:
                fullPathStr = str(filePath) + '/' + str(n)
                self.myQCustomQWidget = QCustomQWidget()
                if n.split(".")[-1] == 'nk':
                    self.myQCustomQWidget.setIcon(os.path.join(os.getenv("CYC_CORE_PATH"), "icons", "nukeSmall.png"))
                elif n.split(".")[-1] == 'jpg':
                    self.myQCustomQWidget.setIcon(os.path.join(os.getenv("CYC_CORE_PATH"), "icons", "jpgIcons.png"))
                else:
                    self.myQCustomQWidget.setIcon(os.path.join(os.getenv("CYC_CORE_PATH"), "icons", "CYCIconSmall.png"))

                self.myQCustomQWidget.setTextUp(unicode(n))

                # Create QListWidgetItem
                myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                myQListWidgetItem.setBackground(QColor('grey'))

                # Set size hint
                myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())

                # set the dictionary keys for the publishing process
                self.infoWidget[str(myQListWidgetItem)] = {'fullPath': fullPathStr, 'name': fullPathStr.split('/')[-1].split('.')[0]}

                # Add QListWidgetItem into QListWidget
                self.myQListWidget.addItem(myQListWidgetItem)
                self.myQListWidget.setItemWidget(myQListWidgetItem, self.myQCustomQWidget)

    def clearListWidget(self):
        # Clear the contents of the previous folder
        self.myQListWidget.clear()


def runStandalone():

    app = QApplication(sys.argv)
    panel = PublishPanel()
    panel.show()
    app.exec_()


def runInNuke():

    runInNuke.panel = PublishPanel()
    runInNuke.panel.show()


if __name__ == "__main__":
    runStandalone()

# calling from nuke :
# from Apps.Steropes.SteropesPublish.ui import PublishUi

# PublishUi.runInNuke()
