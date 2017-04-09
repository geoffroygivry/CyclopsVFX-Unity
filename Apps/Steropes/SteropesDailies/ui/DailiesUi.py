#The MIT License (MIT)
#
#Copyright (c) 2015 Geoffroy Givry
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



  
import os
from PyQt4.QtGui import *
from Apps.Steropes.StyleSheet import MainStyleSheet




icon = os.path.join(os.getenv('CYC_ICON'), 'Cyclops.ico')

  
  
class DailiesPanel(QWidget):

  def __init__(self):

    super(DailiesPanel, self).__init__()


    #creation of the main Layout
    mainLayout = QVBoxLayout()
    #creation of the banner
    bannerLabel = QLabel("Dailies")
    bannerLabel.setProperty('labelClass', 'Main')
    SplitLayout = QVBoxLayout()
    ItemSubLayout = QHBoxLayout()
    self.subItemPic = QLabel()
    self.subItemPic.setProperty('labelClass', 'Pic')
    self.subItemInfo = QLabel()
    self.subItemInfo.setProperty('labelClass', 'itemInfo')
    self.forComments = QTextEdit()
    self.forComments.setProperty('labelClass', 'DailiesComment')
    self.frameIn = QLineEdit()
    self.frameIn.setProperty('labelClass', 'frameIO')
    self.frameOut = QLineEdit()
    self.frameOut.setProperty('labelClass', 'frameIO')
    self.save_push_button = QPushButton("Ok")
    self.save_push_button.setProperty('labelClass', 'pushB')
    self.close_push_button = QPushButton("Close")
    self.close_push_button.setProperty('labelClass', 'pushB')
    frameInLabel = QLabel('First Frame:')
    frameOutLabel = QLabel('Last Frame:')
    framesLayout = QHBoxLayout()
    framesLayout.addWidget(frameInLabel)
    framesLayout.addWidget(self.frameIn)
    framesLayout.addWidget(frameOutLabel)
    framesLayout.addWidget(self.frameOut)
    action_layout = QHBoxLayout()
    action_layout.addWidget(self.close_push_button)
    action_layout.addWidget(self.save_push_button)
    ItemSubLayout.addWidget(self.subItemPic)
    ItemSubLayout.addWidget(self.subItemInfo)
    SplitLayout.addWidget(self.forComments)
    mainLayout.addWidget(bannerLabel)
    mainLayout.addLayout(ItemSubLayout)
    mainLayout.addLayout(framesLayout)
    mainLayout.addLayout(SplitLayout)
    mainLayout.addLayout(action_layout)


    self.setLayout(mainLayout)
    self.setWindowTitle("Cyclops Dailies Submission")
    self.setWindowIcon(QIcon(icon))
    self.setFocus()
    MainStyleSheet.setStyleSheet(self)