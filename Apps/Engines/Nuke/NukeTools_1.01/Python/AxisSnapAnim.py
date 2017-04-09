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
import nukescripts.snap3d

def snapToPointsAnim( node=None, mode='t'):
    '''
    Animated versions of the three default snapping funtions in the axis menu
    args:
       node  -  node to snap
       mode  -  which mode. Available modes are: 't' to match translation, 'tr', to match translation ans rotation, 'trs' to match translation, rotation and scale. default: 't'
    '''

    node = node or nuke.thisNode()
    if mode not in ( 't', 'tr', 'trs' ):
        raise ValueError, 'mode must be "t", "tr" or "trs"'
    
    # KNOB MAP
    knobs = dict( t=['translate'], tr=['translate', 'rotate'], trs=['translate', 'rotate','scaling'] )
    # SNAP FUNCTION MAP
    snapFn = dict( t=nukescripts.snap3d.translateToPoints,
                   tr=nukescripts.snap3d.translateRotateToPoints,
                   trs=nukescripts.snap3d.translateRotateScaleToPoints )

    # SET REQUIRED KNOBS TO BE ANIMATED
    for k in knobs[ mode ]:
        node[ k ].clearAnimated()
        node[ k ].setAnimated()
    
    # GET FRAME RANGE
    fRange = nuke.getInput( 'Frame Range', '%s-%s' % ( nuke.root().firstFrame(), nuke.root().lastFrame() ))
    if not fRange:
        return
    
    # DO THE WORK
    tmp = nuke.nodes.CurveTool() # HACK TO FORCE PROPER UPDATE. THIS SHOULD BE FIXED
    for f in nuke.FrameRange( fRange ):
        nuke.execute( tmp, f, f )
        snapFn[ mode ](node)
    nuke.delete( tmp ) # CLEAN UP THE HACKY BIT