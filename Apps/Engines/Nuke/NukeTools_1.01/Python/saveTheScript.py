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


import os
import nuke


nameLabel = "comp"
compFormat = '2K 5K'
compFolder = 'Comp Precomp'
VersionName = 1
geoffPath = os.environ['GEOFF_PATH']


def saveTheScript():

  show = os.getenv('SHOW')
  shot = os.getenv('SHOT')
  task = os.getenv('TASK')
  lastDir = 'TASKS/%s/Work/Nuke' % (task)
  finalPath = os.path.join(geoffPath, show, shot, lastDir)
  if not os.path.exists(finalPath):
    os.makedirs(finalPath)
  panelPath = 'Nuke script stored in : %s' % (finalPath)

  p = nuke.Panel('Auto Name script')
  p.addSingleLineInput("Type:", nameLabel)
  p.addSingleLineInput("Version:", VersionName)
  p.addEnumerationPulldown("Comp Type:", compFolder)
  p.addEnumerationPulldown("Comp format:", compFormat)
  p.addSingleLineInput("Path", panelPath)
  result = p.show()
  if result:
    nameType = p.value("Type:")
    enumVers = p.value("Version:")
    compF = p.value("Comp format:")
    compFold = p.value("Comp Type:")

    compType = nameType
    version = int(enumVers)
    Cformat = compF
    folderComp = compFold
    if folderComp == 'Precomp':
      if os.path.exists(finalPath + '/Precomps/'):
        newFinalPath = finalPath + '/Precomps'
        nkFile = '%s/%s_%s_comp%s_v%02d_01.nk' % (newFinalPath, shot, compType, Cformat, version)
      else:
        newFinalPath = finalPath + '/Precomps'
        os.makedirs(newFinalPath)
        nkFile = '%s/%s_%s_comp%s_v%02d_01.nk' % (newFinalPath, shot, compType, Cformat, version)
    else:
      nkFile = '%s/%s_%s_comp%s_v%02d_01.nk' % (finalPath, shot, compType, Cformat, version)
    if nameType == None:
      pass
    else:
      try:
        nuke.scriptSaveAs(nkFile, 0)
      except RuntimeError:
        nuke.message('this file already exists')
