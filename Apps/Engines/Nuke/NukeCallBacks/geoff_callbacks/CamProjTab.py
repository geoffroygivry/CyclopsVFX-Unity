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


def CamProjTab01():
  n = nuke.thisNode()
  if 'Projector' not in n.knobs():
    projTabKnob = nuke.Tab_Knob('Projector')
    textMkProjKnob = nuke.Text_Knob('MakeProjText', 'Make Projector')
    LockButtonKnob = nuke.PyScript_Knob('Lock', 'Lock', 'from geoff_callbacks import CamProjTab; CamProjTab.doLock()')
    UnLockButtonKnob = nuke.PyScript_Knob('Unlock', 'Unlock', 'from geoff_callbacks import CamProjTab; CamProjTab.doUnLock()')
    LockStatusKnob = nuke.Text_Knob('LockStatus', ' ', ' --Unlocked--')
    setcurrentFrKnob = nuke.PyScript_Knob('setCurrentFrame', '      Set Current Frame    ', 'from geoff_callbacks import CamProjTab; CamProjTab.setFrame()')
    refFrameKnob = nuke.Int_Knob('refFrame', ' ')
    dividerKnob = nuke.Text_Knob('','','')
    for k in (projTabKnob, textMkProjKnob, LockButtonKnob, UnLockButtonKnob, LockStatusKnob, setcurrentFrKnob, refFrameKnob, dividerKnob):
      n.addKnob(k)
    UnLockButtonKnob.clearFlag(nuke.STARTLINE)
    LockStatusKnob.clearFlag(nuke.STARTLINE)
    refFrameKnob.clearFlag(nuke.STARTLINE)

def doLock():

  n = nuke.thisNode()
  referFrame = int(n['refFrame'].value())
  n['translate'].setExpression('curve(refFrame)')
  n['rotate'].setExpression('curve(refFrame)')
  n['scaling'].setExpression('curve(refFrame)')
  n['focal'].setExpression('curve(refFrame)')
  n['tile_color'].setValue(118197761)
  n['LockStatus'].setValue('<font color=Blue> --Locked--</font>')
  n['label'].setValue('Projector @ %s' % (referFrame))


def doUnLock():

  n = nuke.thisNode()
  n['translate'].setExpression('curve')
  n['rotate'].setExpression('curve')
  n['scaling'].setExpression('curve')
  n['focal'].setExpression('curve')
  n['tile_color'].setValue(2617245697)
  n['LockStatus'].setValue('<font color=Green> --Unlocked--</font>')
  n['label'].setValue(' ')

def setFrame():

  nuke.thisNode()['refFrame'].setValue(int(nuke.value('frame')))