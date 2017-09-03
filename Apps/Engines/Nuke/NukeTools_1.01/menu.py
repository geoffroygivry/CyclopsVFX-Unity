#!/usr/bin/env python2

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
import json
import autobackdrop
import stores
import NukeCollect
import explorer
import AxisSnapAnim
import reloadReadNodes
import openNukeScriptMetadata
import mari_bridge
import rotateCenter
import ToDoList
import makeIcons
import LookAt
import ImageMagick
import readCompRange
import missingFrames
import RandomSelection
import updateFrameRange
import saveTheScript
import load_frame_range
from Apps.Steropes.SteropesDailies.Nuke import steropesDailies
from Apps.Steropes.SteropesPublish.ui import PublishUi


import geoffroy_callbacks
geoffroy_callbacks.register_callbacks()

# nuke.Root() callback
nuke.addOnUserCreate(load_frame_range.in_nuke)


ToDoList.registerNukePanel()
nuke.addAfterRender(ImageMagick.makeThumbnail)
stores.addStoresMenu()

os.environ['GENEPATH'] = '/usr/home/ggivry/Geoff/NUKE/'
genePath = os.environ['GENEPATH']

fullHD = '2048 1152 0 0 2048 1152 1 2K_178'
nuke.addFormat(fullHD)

fullHD1K = '1024 576 0 0 1024 576 1 1K_178'
nuke.addFormat(fullHD1K)

CGOverscan = '2150 1209 0 0 2150 1209 1 CG_Overscan'
nuke.addFormat(CGOverscan)

ms = nuke.menu('Axis')
ms.addCommand('Snap/Match selected position (animated)',
              lambda: AxisSnapAnim.snapToPointsAnim(mode='t'))
ms.addCommand('Snap/Match selected position, orientation (animated)',
              lambda: AxisSnapAnim.snapToPointsAnim(mode='tr'))
ms.addCommand('Snap/Match selected position, orientation, size (animated)',
              lambda: AxisSnapAnim.snapToPointsAnim(mode='trs'))

ma = nuke.menu('Animation')
ma.addCommand('Snap Keyframe 0 => 1 => 0', "snapIt()")
ma.addCommand('Snap Keyframe 0 => 1', "snapZeroToOne()")
ma.addCommand('Snap Keyframe 1 => 0', "snapOneToZero()")
ma.addCommand('Snap Keyframe LensFlare', "snapItFlare()")
ma.addCommand('$Gui this', "DolGui()")
ma.addCommand('!$Gui this', "DolGuiInv()")


def view_depth():
    for x in nuke.root().nodes():
        if(x.Class() == "Viewer"):
            x["channels"].setValue("red green blue depth.Z")


nuke.menu("Nodes").menu("Image").addCommand("LookAtDepth", view_depth, "Meta+Z")


def DolGui():

    k = nuke.thisKnob()
    k.setExpression('$gui')


def DolGuiInv():

    k = nuke.thisKnob()
    k.setExpression('!$gui')


def snapItFlare():

    k = nuke.thisKnob()
    t = nuke.frame()
    tMinus = t - 4
    tPlus = t + 7
    try:
        k.setAnimated()
        k.setValueAt(0, tMinus)
        k.setValueAt(1, t)
        k.setValueAt(0, tPlus)
    except AttributeError:
        pass


def snapIt():

    k = nuke.thisKnob()
    t = nuke.frame()
    tMinus = t - 1
    tPlus = t + 1
    try:
        k.setAnimated()
        k.setValueAt(0, tMinus)
        k.setValueAt(1, t)
        k.setValueAt(0, tPlus)
    except AttributeError:
        pass


def snapZeroToOne():

    k = nuke.thisKnob()
    t = nuke.frame()
    tPlus = t + 1
    try:
        k.setAnimated()
        k.setValueAt(0, t)
        k.setValueAt(1, tPlus)
    except AttributeError:
        pass


def snapOneToZero():

    k = nuke.thisKnob()
    t = nuke.frame()
    tPlus = t + 1
    try:
        k.setAnimated()
        k.setValueAt(1, t)
        k.setValueAt(0, tPlus)
    except AttributeError:
        pass


def importFromMeta():
    n = nuke.selectedNode()
    nuke.nodePaste(n.metadata()['exr/nuke/BackupScript'])


def reloadSandboxModule():
    p = nuke.Panel('reload python module')
    p.addSingleLineInput('Module Name:', "")
    p.addSingleLineInput('Function Name:', "")
    result = p.show()
    if result:
        modStr = p.value('Module Name:')
        funcStr = p.value('Function Name:')

        noopNode = nuke.createNode('NoOp')
        noopNode['name'].setValue('reload %s.py' % (modStr))
        reloadTab = nuke.Tab_Knob('reload_module', 'reload module')
        pyscriptStr = "sys.path.append('/Dropbox/sandbox/nuke') \nimport %s\nreload(%s)\n%s.%s()" % (
            modStr, modStr, modStr, funcStr)
        pyButton = nuke.PyScript_Knob('reloadRun', 'run run run!', pyscriptStr)
        for k in (reloadTab, pyButton):
            noopNode.addKnob(k)


try:
    if os.getenv("JOB") != None:
        menu2 = nuke.menu('Nuke').addMenu('%s | %s' % (os.getenv("JOB"), (os.getenv('SHOT'))))
        import majorVersionUp
        import minorVersionUp
        #.addCommand( '%s | %s'% (os.getenv("JOB"), (os.getenv('SHOT'))), '').setEnabled(False)
        menu2.addSeparator()
        menu2.addCommand('Save The Script ', 'saveTheScript.saveTheScript()')
        menu2.addCommand('Major Version Up ', 'majorVersionUp.majorVersionUp()')
        menu2.addCommand('Minor Version Up ', 'minorVersionUp.minorVersionUp()')
        menu2.addSeparator()
        menu2.addCommand('Steropes/Dailies Submission', 'steropesDailies.start()')
        menu2.addCommand('Steropes/Publish Submission', 'PublishUi.runInNuke()')
    else:
        menu2 = nuke.menu('Nuke').addMenu('No Env Mode').setEnabled(False)

except KeyError:
    menu2 = nuke.menu('Nuke').addMenu('No Env Mode').setEnabled(False)


Geoff = nuke.menu('Nuke').addMenu('CyclopsVFX')
# Geoff.addCommand('Auto Name Script', 'autoNameScript_RND.saveTheScript()')
# Geoff.addCommand('Save major version up ', 'majorVersionUp.majorVersionUp()', "^+Up")
# Geoff.addCommand('Save minor version up ', 'minorVersionUp.minorVersionUp()', "^Up")


Geoff.addSeparator()


Geoff.addCommand('Reload Sanbox module', 'reloadSandboxModule()')

Geoff.addSeparator()

Geoff.addCommand('Reload All Read Nodes', 'reloadReadNodes.reloadAll()', icon='reloadRead.png')
Geoff.addCommand('Reload Selected Read Nodes',
                 'reloadReadNodes.reloadSelected()', icon='reloadRead.png')

Geoff.addSeparator()

Geoff.addCommand('Import Nuke script from selected read nodes', 'importFromMeta()', "^+r")
Geoff.addCommand('create read node from selected Write', 'read_from_write()', "alt+r")
Geoff.addCommand('Open Selected nodes in Explorer', 'explorer.openInExplorer()')

Geoff.addSeparator()

Geoff.addCommand('Display Reads Path', "displayReadFile()")
Geoff.addCommand('Display Reads Path Selected', "displayReadFileSelected()")

Geoff.addSeparator()

Geoff.addCommand('Reads and Deep Reads Script Frame Range (All)', "readCompRange.readCompRange()")
Geoff.addCommand('Reads and Deep Reads Script Frame Range (Selected)',
                 "readCompRange.readCompRangeSelected()")
Geoff.addCommand('Reads and Deep Reads Rendered Frame Range (Selected)',
                 "updateFrameRange.updateFrameRange()")

Geoff.addSeparator()

Geoff.addCommand('Display channels', "showChannelsDisplay()")
Geoff.addCommand('Check Missing Frames', 'missingFrames.missingFrames()')

Geoff.addSeparator()

#Geoff.addCommand('Create Template Node(s)', "templateNode.TemplateNode()")
#Geoff.addCommand('update all Template Nodes', "templateNode.excuteAllTempNode()")

# Geoff.addSeparator()

Geoff.addCommand("Rotate Center Expression", "rotateCenter.getExprThis()")
Geoff.addCommand('Nuke Collect', 'NukeCollect.collectThisComp()')

Geoff.addSeparator()

Geoff.addCommand('ExponBlur', 'nuke.createNode("L_ExponBlur_v03")')
Geoff.addCommand('LookAt', 'LookAt.panelLookAt()')
Geoff.addCommand('Random Selection in Selected Nodes', 'RandomSelection.selectRandom()')

Geoff.addSeparator()

Geoff.addCommand('Icons/Mono Icon', 'makeIcons.makeIcon()')
Geoff.addCommand('Icons/Check!', 'makeIcons.checkIcon()')
Geoff.addCommand('Icons/Uncheck!', 'makeIcons.uncheckIcon()')
Geoff.addCommand('Icons/select check Icons', 'makeIcons.selCheck()')
Geoff.addCommand('Icons/select Uncheck Icons', 'makeIcons.selUncheck()')
Geoff.addCommand('Icons/Clear Icon', 'makeIcons.clearIcon()')


toolbar = nuke.menu('Nodes')
toolbar.addCommand('Merge/KeyMix', 'nuke.createNode("Keymix")', 'Ctrl+d')
toolbar.addCommand('Transform/Reformat', 'nuke.createNode("Reformat")', 'Ctrl+r')
toolbar.addCommand("Merge/Merges/Stencil",
                   "nuke.createNode('Merge2', 'operation stencil')", "Alt+z", icon="MergeOut.png")
toolbar.addCommand("Merge/Merges/Plus",
                   "nuke.createNode('Merge2', 'operation plus Achannels rgb', False)", "^+a")
toolbar.addCommand("Merge/Merges/Divide", "nuke.createNode('Merge2', 'operation divide')")
toolbar.addCommand("Merge/Merges/Mask",
                   "nuke.createNode('Merge2', 'operation mask')", "^+z", icon="MergeIn.png")
toolbar.addCommand('Color/Math/Multiply', 'nuke.createNode("Multiply")', '^m')
toolbar.addCommand('Color/Exposure', 'nuke.createNode("EXPTool")', 'e', icon='Exposure.png')
toolbar.addCommand('Draw/Bezier', 'nuke.createNode("Bezier")', 'Alt+b', icon='wizardFX_icon.png')
toolbar.addCommand('Other/AutoBackdrop', 'autobackdrop.autoBackdrop()',
                   'Alt+m', icon='wizardFX_icon.png')


nuke.knobDefault('CurveTool.ROI', 'autocropdata autocropdata autocropdata autocropdata')
nuke.knobDefault('Bezier.cliptype', 'no clip')
nuke.knobDefault('RotoPaint.label', '[value lifetime_type]')
nuke.knobDefault('RotoPaint.outputMask', 'rotopaint_mask.a')
nuke.knobDefault('RotoPaint.cliptype', 'no clip')
nuke.knobDefault("RotoPaint.toolbar_source_translate_round", "true")
nuke.knobDefault("Roto.toolbar_autokey", "true")
nuke.knobDefault("Roto.output", "rgba")
nuke.knobDefault("Read.before", 'hold')
nuke.knobDefault("Card.rows", "1")
nuke.knobDefault("Card.columns", "1")
nuke.knobDefault("Write.extension", "sxr")
nuke.knobDefault("Read.postage_stamp", "false")


def showPath():
    list1 = []
    for n in nuke.allNodes('Read'):
        nameFile = n['file'].value().rsplit('/', 1)[-1].split('.')[0]
        pathFile = n['file'].value()
        finalpath = '\n' + nameFile + ':\n' + pathFile
        list1.append(finalpath)
        NumRead = str(len([n.name() for n in nuke.allNodes('Read')]))
    return NumRead + ' Read Node(s):\n\n' + '\n\n==================================\n'.join(list1)


def displayReadFile():
    nuke.display("showPath()", nuke.root(), 'Display Reads Path')


def showPathSelected():
    list1 = []
    for n in nuke.selectedNodes('Read'):
        nameFile = n['file'].value().rsplit('/', 1)[-1].split('.')[0]
        pathFile = n['file'].value()
        finalpath = '\n' + nameFile + ':\n' + pathFile
        list1.append(finalpath)
        NumRead = str(len([n.name() for n in nuke.selectedNodes('Read')]))
    try:
        return NumRead + ' Read Node(s):\n\n' + '\n\n==================================\n'.join(list1)
    except:
        UnboundLocalError
        nuke.message('please select reads nodes')
        pass


def displayReadFileSelected():
    nuke.display("showPathSelected()", nuke.root(), 'Display Reads Path Selected')


def showChannels():
    return '\n'.join(nuke.thisNode().channels())


def showChannelsDisplay():
    node = nuke.selectedNode()
    nuke.display('showChannels()', node, 'show channels for %s' % node.name())


def read_from_write():
    write = nuke.selectedNode()
    file_path = write['file'].value()
    min_frame = int(min([x.split('.')[-2] for x in os.listdir(os.path.dirname(file_path)) if x.split('.')[-1] == 'exr']))
    max_frame = int(max([x.split('.')[-2] for x in os.listdir(os.path.dirname(file_path)) if x.split('.')[-1] == 'exr']))
    nuke.nodes.Read(file=file_path, first=min_frame, last=max_frame)
