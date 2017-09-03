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
import platform
import shutil
import time
import ImageMagick


def writeMeta():
    localtime = time.localtime()
    timeString = time.strftime("%d%m%Y%H%M%S", localtime)
    writeNode = nuke.thisNode()
    extension = writeNode['file'].value().split('.')[-1]
    if extension == 'exr':
        nuke.tprint("Write node = %s" % writeNode)
        writeNode['metadata'].setValue("all metadata")
        try:
            operator = os.environ['USERNAME']
            origNukeScript = nuke.root().name()
            thumbnail = ImageMagick.justThumPath()
            origNukeScriptName = origNukeScript.split('/')[-1]
            backupScript = '.' + origNukeScriptName.split('.')[0] + "_bkp_%s.nk" % (timeString)
            finalBackupScrip = writeNode['file'].value().rsplit('/', 1)[0] + '/' + backupScript

            try:
                shutil.copy(origNukeScript, finalBackupScrip)
            except IOError:
                nuke.message('Please save the script first')
                pass

            mdn = nuke.nodes.ModifyMetaData()
            fullData = "{set Operator %s}\n{set NukeScript %s}\n{set BackupScript %s}\n{set Thumbnail %s}" % (operator, origNukeScript, finalBackupScrip, thumbnail)
            mdn['metadata'].fromScript(fullData)
            oldInput = writeNode.dependencies()[0]
            writeNode.setInput(0, mdn)
            mdn.setInput(0, oldInput)
        except RuntimeError:
            nuke.message('Please save the script first')
            pass
    else:
        pass


def delMetaNode():

    for n in nuke.allNodes():
        if n.Class() == 'ModifyMetaData':
            nuke.delete(n)
