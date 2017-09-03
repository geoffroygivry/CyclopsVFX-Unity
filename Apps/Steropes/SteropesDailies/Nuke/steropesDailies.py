#!/usr/bin/env python2

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


import nuke
import os
from PyQt4.QtGui import *
import datetime
from PyQt4.QtCore import *
from Hydra.core import submissions
from Apps.Steropes.SteropesDailies.ui.DailiesUi import DailiesPanel


format = "%a %d %b %Y at %H:%M:%S "
today = datetime.datetime.today()
timeStamp = today.strftime(format)

artistName = os.getenv('USERNAME')


class nukeSteropesDailiesCore(DailiesPanel):
    '''The Nuke dailies submission panel'''

    def __init__(self):
        super(nukeSteropesDailiesCore, self).__init__()

        self.NukeSelNode = nuke.selectedNode()
        self.path = os.path.dirname(self.NukeSelNode['file'].value())
        self.thumbMeta = unicode(self.NukeSelNode.metadata()['exr/nuke/Thumbnail'])

        self.subItemPic.setPixmap(QPixmap(self.thumbMeta))
        self.setItemInfo()
        self.setMinFrame()
        self.setMaxFrame()

        self.close_push_button.clicked.connect(self.close)
        self.save_push_button.clicked.connect(self.goDb)

    def setItemInfo(self):
        pathToFile = self.NukeSelNode['file'].value()
        pathToFile = pathToFile.replace('%04d', '####')
        finalTextItemInfo = '%s\nBy %s\n%s' % (pathToFile, artistName, timeStamp)
        self.subItemInfo.setText(finalTextItemInfo)

    def setMinFrame(self):
        min_frame = min([x.split('.')[-2] for x in os.listdir(self.path) if x.split('.')[-1] == "exr"])
        self.frameIn.setText(min_frame)

    def setMaxFrame(self):
        max_frame = max([x.split('.')[-2] for x in os.listdir(self.path) if x.split('.')[-1] == "exr"])
        self.frameOut.setText(max_frame)

    def goDb(self):
        pathToFile = unicode(self.NukeSelNode['file'].value())
        pathToFile = unicode(pathToFile.replace('%04d', '####'))
        commentField = unicode(self.forComments.toPlainText())
        bckScript = unicode(self.NukeSelNode.metadata()['exr/nuke/NukeScript'])
        frameFirst = unicode(self.frameIn.text())
        frameLast = unicode(self.frameOut.text())
        submissions.sendToDailies(pathToFile, commentField, bckScript, frameFirst, frameLast, self.thumbMeta)
        self.close()


def start():

    try:
        start.panel = nukeSteropesDailiesCore()
        start.panel.show()
    except ValueError:
        nuke.message('Please select a read node')
        pass

# calling in nuke :
# from Apps.Steropes.Nuke import steropesDailies
# steropesDailies.start()
