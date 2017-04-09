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
import sys
import string
import shutil
import fnmatch
import nuke
import threading
import time



class archiveIt():
    
    def __init__(self):
        
        self.archiveName = ""
        self.path = '/user_data/Geoff/PERSONAL/Archive'
        self.buildPanel()
        
    def buildPanel(self):
        
        self.p = nuke.Panel('Dailies Submission')
        self.p.addSingleLineInput("Archive Name:", self.archiveName)
        self.p.show()
        self.finalName = self.p.value("Archive Name:")
        self.collectFootage()
        
    def collectFootage(self):
        
        self.name_ = os.path.join(self.path, self.finalName)
        os.mkdir(self.name_)
        self.nukeScriptName = self.name_ + '/' + self.finalName + '.nk'
        nuke.scriptSaveAs(self.nukeScriptName)
        
        #### Getting Filepaths, StartFrame and EndFrame from ReadNodes
        nuke.selectAll()
        self.tmpDir =[]
        self.rs = []
        self.stF = []
        self.edF = []
        for elm in nuke.selectedNodes('Read'):
            self.rs.append(elm.knob('name').value())
            self.stF.append(elm.knob('first').value())
            self.edF.append(elm.knob('last').value())
            self.tmpDir.append(elm.knob('file').value())
        self.tmpF = []
        self.tmpD = []
        for el in self.tmpDir:
            self.tp = os.path.dirname(el)
            self.tmpD.append(self.tp + '/')
            self.lp = len (self.tp)+1
            self.tmpF.append(el[self.lp:])
            
    #### Setting the Directory to save to 
        self.sc = nuke.Root().name()
        self.scPath = os.path.dirname(nuke.Root().name())
        self.pl = len(os.path.dirname(nuke.Root().name())) +1
        self.scName = self.sc[self.pl:-3]
        self.fdir = self.scName + '_Footage'
        self.fd = self.scPath +'/' + self.fdir
        os.mkdir(self.fd)
        self.ftdir = self.fd + '/' 
        self.rdir = []
        for n in self.rs:   
            os.mkdir(self.ftdir + n)
            self.rdir.append(self.ftdir+n+'/')
        self.CopyAndBag()
        
    def CopyAndBag(self):
        
    #### Checking the Footage and then Copy
        for i in range (0,len(self.rdir)):
            if ('%' in self.tmpF[i]):
                ind = string.find(self.tmpF[i],'%',0,len(self.tmpF[i]))
                fname = self.tmpF[i][0:ind]
                enum = self.tmpF[i][ind:-4]
                ext = self.tmpF[i][-4:]
                seq = []
                for file in os.listdir(self.tmpD[i]):
                    if fnmatch.fnmatch(file, fname + '*'):
                        for j in range (self.stF[i],self.edF[i]):
                            if fnmatch.fnmatch(file, '*'+str(j) + ext):
                                filelist = list(file)
                                filelist1 = string.join(filelist,"")
                                seq.append(filelist1)
                for elm in seq: shutil.copy(self.tmpD[i] + elm, self.rdir[i] +elm)
            else: shutil.copy(self.tmpDir[i], self.rdir[i]+ self.tmpF[i])
        self.zipArchive()
    
    def zipArchive(self):
        
        os.system('zip -r ' + self.name_ + '_Archived ' + self.name_ + ' ' + '& rm -r ' + self.name_)
        finalMsg ='the Archive <font face="arial black" size="4">%s_Archived.zip</font face="arial black" size="4"> is complete' % (self.name_.split('/')[-1])
        nuke.message(finalMsg)
	