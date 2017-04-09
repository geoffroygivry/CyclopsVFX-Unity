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



def updateFrameRange():
    
    listTest = []
    finalList = []
    for n in nuke.selectedNodes():
        if n.Class() == "Read" or n.Class() == "DeepRead":
            filePath = n['file'].value().rsplit('/', 1)[0]
            try:
                for x in os.listdir(filePath):
                    if x.split('.')[-1] == 'sxr' or x.split('.')[-1] == 'exr' :
                        listTest.append(x)
                for h in listTest:
                        number = h.split('.')[-2]
                        finalList.append(int(number))
                maxFrame =  max(finalList)
                minFrame = min(finalList)
                n['first'].setValue(minFrame)
                n['last'].setValue(maxFrame)
                if n.Class() == "Read":
                    n['origfirst'].setValue(minFrame)
                    n['origlast'].setValue(maxFrame)
                
                print n['name'].value(), " : min Frame : ", minFrame, ", max frame : ", maxFrame, " frame Range updated!"
            except OSError:
                print "no file in here sorry Buddy!"
                pass