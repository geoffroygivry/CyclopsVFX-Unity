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


nodeName = "k"
knobName = "flarePosition"


def getExprThis():
  
  

    
    p = nuke.Panel('rotate Center')
    p.addSingleLineInput("Node_Name:", nodeName)
    p.addSingleLineInput("Knob_Name:", knobName)
    result = p.show()
    nameType = p.value("Node_Name:")
    KnobName2 = p.value("Knob_Name:")
    nameType2 = nameType
    KnobName3 = KnobName2


    firstExpr = str('%s.%s' % (nameType2, KnobName3))
    getExprX = '(((%s) - width/4) * 2) + ((%s - (((%s) - width/4) * 2)) * intensity)' % (firstExpr, firstExpr, firstExpr)
    getExprY = '(((%s) - height/4) * 2) + ((%s - (((%s) - height/4) * 2)) * intensity)' % (firstExpr, firstExpr, firstExpr)


    newNoop = nuke.createNode('NoOp')
    newNoopTab = nuke.Tab_Knob('rotateCenter')
    newNoopXyKnob = nuke.XY_Knob('Expr')
    newNoopFloat = nuke.Double_Knob('intensity')
    newNoop.addKnob(newNoopTab)
    newNoop.addKnob(newNoopXyKnob)
    newNoop.addKnob(newNoopFloat)
    newNoopFloat.setValue(0)
    newNoopFloat.setRange(-1, 1)
    newNoopXyKnob.setExpression(getExprX, 0)
    newNoopXyKnob.setExpression(getExprY, 1)