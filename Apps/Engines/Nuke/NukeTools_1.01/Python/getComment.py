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
import time
import nukescripts
import sys


class getComment( nukescripts.PythonPanel ):
    
    def __init__(self):
        self.comment = ""
        self.compStart = int(nuke.root()['first_frame'].value())
        self.compEnd = int(nuke.root()['last_frame'].value())
        self.scriptPath = nuke.root()['name'].value()
        self.frameRange = str(self.compStart) + ' - ' + str(self.compEnd)
        self.shotName = nuke.root()['name'].value().split('/')[-1].split('_v')[0]
        self.date = str(time.localtime()[2]) + ('/') + str(time.localtime()[1]) + ('/') + str(time.localtime()[0])
        self.time = str(time.localtime()[3]) + ':' + str(time.localtime()[4])
        if nuke.root()['name'].value() == "":
           self.versionName = nuke.root()['name'].value().split('/')[-1].split('v')[-1].split('.')[0].split('_')[0]
        else:
           self.versionName = "v" + nuke.root()['name'].value().split('/')[-1].split('v')[-1].split('.')[0].split('_')[0]
          

        self.buildPanel()

    def buildPanel(self):
        self.p = nuke.Panel('Comments')
        self.p.addSingleLineInput("Shot Name", self.shotName)
        self.p.addSingleLineInput("Version", self.versionName)
        self.p.addSingleLineInput("Comp Range", self.frameRange)
        self.p.addSingleLineInput("Date", self.date)
        self.p.addMultilineTextInput("Comments:", self.comment)
        result = self.p.show()
        self.addComment = self.p.value("Comments:")
        if nuke.root()['name'].value() == "":
            self.totalComment = 'Untitled Document' + str(self.versionName) + '\nFrame Range: ' + str(self.frameRange) + '\n\nComments on the ' + str(self.date) + ' :\n\n' + str(self.addComment)
        else:
            self.totalComment = str(self.shotName) + '_' + str(self.versionName) + '\nFrame Range: ' + str(self.frameRange) + '\n\nComments on the ' + str(self.date) + ' :\n\n' + str(self.addComment)
        
        self.textCreation()
        
    def textCreation(self):

      if self.addComment == "":
         pass
      else:
	  r = 0.22745098
          g = 0.29803923
          b = 0.25490198
          hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
          r2 = 1
          g2 = 0.81176472
          b2 = 0.66274512
          hexColour02 = int('%02x%02x%02x%02x' % (r2*255,g2*255,b2*255,1),16)
          self.createText = nuke.nodes.Text(name = 'Comment',
          message = self.totalComment,
          label = self.date + '\nat ' + self.time,
          yjustify = 'bottom',
          box = 0,
          gl_color = hexColour,
          tile_color = hexColour,
          font = '/usr/share/fonts/dejavu/DejaVuSansMono.ttf',
	  note_font = 'Arial Black',
          note_font_color = hexColour02)
          tabComment = nuke.Tab_Knob('Comments')
          self.createText.addKnob(tabComment)
          self.textKnob = nuke.Text_Knob('')
          self.createText.addKnob(self.textKnob)
          commentBox1 = nuke.Boolean_Knob(self.addComment)
          commentBox1.setValue(False)
          self.createText.addKnob(commentBox1)
          self.createText.addKnob(self.textKnob)
          
        
          self.setData()


    def setData(self):
        compRange = self.p.value("Comp Range")
        firstFrame = compRange.split(' - ')[0]
        lastFrame = compRange.split(' - ')[1]
        nuke.root()['first_frame'].setValue(int(firstFrame))
        nuke.root()['last_frame'].setValue(int(lastFrame))
        nuke.root()['label'].setValue(str(self.totalComment))
