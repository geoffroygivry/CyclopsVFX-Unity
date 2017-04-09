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

LookAtName = "LookAt"

def panelLookAt():
    p = nuke.Panel("Look At Panel")
    p.addSingleLineInput("LookAt Name:", LookAtName)
    p.addButton("Cancel")
    p.addButton("OK")
    result = p.show()

    nameLookAt = p.value("LookAt Name:")
    EXpX = 'degrees(atan2(%s.translate.y-translate.y,sqrt(pow(%s.translate.x-translate.x,2)+pow(%s.translate.z-translate.z,2))))' % (nameLookAt, nameLookAt, nameLookAt)
    EXpY = '%s.translate.z-this.translate.z >= 0 ? 180+degrees(atan2(%s.translate.x-translate.x,%s.translate.z-translate.z)):180+degrees(atan2(%s.translate.x-translate.x,%s.translate.z-translate.z))' % (nameLookAt, nameLookAt, nameLookAt, nameLookAt, nameLookAt)
    nuke.nodes.Axis(name=nameLookAt)
    

    for n in nuke.selectedNodes():
        n['rotate'].setExpression(EXpX, 0)
        n['rotate'].setExpression(EXpY, 1)