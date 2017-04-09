# -*- coding: utf-8 -*-

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


import nuke
import os
import sys
from PyQt4.QtGui import *
import datetime
from PyQt4.QtCore import *
from Hydra.core import hQuery
from Apps.Steropes.SteropesDailies.ui.DailiesUi import DailiesPanel
import shutil


format = "%a %d %b %Y at %H:%M:%S "
today = datetime.datetime.today()
timeStamp = today.strftime(format)

artistName = os.getenv('USERNAME')


taskforDb = "Comp"


class nukeSteropesDailiesCore(DailiesPanel):
    '''The Nuke dailies submission panel'''
    def __init__(self):
        super(nukeSteropesDailiesCore, self).__init__()


        self.setThum()
        self.setItemInfo()
        self.setMinFrame()
        self.setMaxFrame()

        self.close_push_button.clicked.connect(self.close)
        self.save_push_button.clicked.connect(self.goDb)

    def setThum(self):

        NukeSelNode = nuke.selectedNode()
        path = NukeSelNode['file'].value().rsplit('/', 1)[0]
        newPath = []
        thumbList = []
        for I in os.listdir(path):
            if I[0] != '.':
                newPath.append(I)
            else:
                if I.split('.')[2] == 'thumbnail':
                    thumbList.append(I)
        thumbnailPic = os.path.join(path, thumbList[0])
        self.subItemPic.setPixmap(QPixmap(thumbnailPic))

    def setItemInfo(self):

        NukeSelNode = nuke.selectedNode()
        pathToFile = NukeSelNode['file'].value()
        pathToFile = pathToFile.replace('%04d', '####')
        finalTextItemInfo = '%s\nBy %s\n%s' % (pathToFile, artistName, timeStamp)
        self.subItemInfo.setText(finalTextItemInfo)


    def setMinFrame(self):

        NukeSelNode = nuke.selectedNode()
        path = NukeSelNode['file'].value().rsplit('/', 1)[0]
        newPath = []
        thumbList = []
        for I in os.listdir(path):
            if I[0] != '.':
                newPath.append(I)
            else:
                if I.split('.')[2] == 'thumbnail':
                    thumbList.append(I)
        minNum = min([r.split('.')[1] for r in newPath])
        self.frameIn.setText(minNum)

    def setMaxFrame(self):

        NukeSelNode = nuke.selectedNode()
        path = NukeSelNode['file'].value().rsplit('/', 1)[0]
        newPath = []
        thumbList = []
        for I in os.listdir(path):
            if I[0] != '.':
                newPath.append(I)
            else:
                if I.split('.')[2] == 'thumbnail':
                    thumbList.append(I)
        maxNum = max([r.split('.')[1] for r in newPath])
        self.frameOut.setText(maxNum)

    def copyThumb(self):
      NukeSelNode = nuke.selectedNode()
      thumbMeta = unicode(NukeSelNode.metadata()['exr/nuke/Thumbnail'])
      self.newName = unicode(thumbMeta.split('/')[-1])
      self.newName = unicode(self.newName.replace('.', '', 1))
      shutil.copy(thumbMeta, (os.getenv('CYC_METEOR_PATH') + '/public/' + self.newName))
      

    def goDb(self):

        NukeSelNode = nuke.selectedNode()
        pathToFile = unicode(NukeSelNode['file'].value())
        pathToFile = unicode(pathToFile.replace('%04d', '####'))
        commentField = unicode(self.forComments.toPlainText())
        bckScript = unicode(NukeSelNode.metadata()['exr/nuke/NukeScript'])
        frameFirst = unicode(self.frameIn.text())
        frameLast = unicode(self.frameOut.text())
        self.copyThumb()
        hQuery.sendToDailies(pathToFile, commentField, bckScript, frameFirst, frameLast, self.newName)
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