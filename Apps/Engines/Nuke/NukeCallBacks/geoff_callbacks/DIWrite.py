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


def CreateWriteTab():
    #### create knobs
    n = nuke.thisNode()
    if 'DI Job System' not in n.knobs():
        tabKnob = nuke.Tab_Knob('DI Job System')
        jobKnob = nuke.EvalString_Knob('job')
        shotKnob = nuke.EvalString_Knob('shot')
        folderKnob = nuke.Enumeration_Knob('folder', 'Folder', ['OUT', 'ELEMENTS', 'PLATES', 'TEST'])
        versionKnob = nuke.Int_Knob('version1', 'version')
        labelKnob = nuke.EvalString_Knob('usr_label', 'label')
        extKnob = nuke.EvalString_Knob('ext')
        buttonKnob = nuke.PyScript_Knob('createOut', 'Create Output', 'from geoff_callbacks import DIWrite; DIWrite.createOutFunction()')

        #### set some defaults for the knobs
        jobKnob.setValue(os.environ.get('JOB'))
        shotKnob.setValue(os.environ.get('SHOT'))
        versionKnob.setValue(1)
        labelKnob.setValue('comp')
        extKnob.setValue('exr')

        for k in [tabKnob, jobKnob, shotKnob, folderKnob, versionKnob, labelKnob, buttonKnob, extKnob]:
            n.addKnob(k)


def createOutFunction():
    n = nuke.thisNode()
    job = n['job'].value()
    shot = n['shot'].value()
    folder = n['folder'].value()
    version = n['version1'].value()
    label = n['usr_label'].value()
    ext = n['ext'].value()

    #### build up the shot name
    shotName = '%s/%s/%s/%s_v%03d_%s' % (job, shot, folder, shot, int(version), label)
    shotName02 = '%s_v%03d_%s' % (shot, int(version), label)

    #### grab base render directory from environment
    baseDir = os.environ.get('PIC')
    if baseDir == None:
        baseDir = os.environ['GEOFF_PATH']
    fullPath = baseDir + '/' + shotName

    try:
        os.makedirs(fullPath)
    except OSError:
        pass

    fileName = '%s.%s.%s' % (shotName02, '%04d', ext)
    fname = baseDir + '/' + shotName + '/' + fileName

    #### set the file knob to the new file name
    n['file'].setValue(fname)
    nuke.message('The Folder <font face="arial black" size="4">%s</font face="arial black" size="4"> has been created' % fullPath)