camAnim = nuke.toNode("CYC_ALT_CAM")
theDot = nuke.toNode("FuckingDot")
frameCounter= 1045

def animListAtFrame(frame, mainCam, ts):
    frameShot = frame
    cam = mainCam
    CamAnim = cam[ts]
    animCuX = CamAnim.animation(0)
    animCuY = CamAnim.animation(1)
    animCuZ = CamAnim.animation(2)
    animList = []
    try:
        for key in animCuX.keys():
            if key.x == frameShot:
                animList.append(key.y)
        for key in animCuY.keys():
            if key.x == frameShot:
                animList.append(key.y)
        for key in animCuZ.keys():
            if key.x == frameShot:
                animList.append(key.y)
        return animList
    except AttributeError:
        k = CamAnim.value()
        animList.append(k)
        return animList[0]


def createCard(frameCount):
    rotateVal = animListAtFrame(frameCount, camAnim, 'rotate')
    translateVal = animListAtFrame(frameCount, camAnim, 'translate')
    focalVal = animListAtFrame(frameCount, camAnim, 'focal')
    hapertureVal = animListAtFrame(frameCount, camAnim, 'haperture')
    
    
    newCard = nuke.nodes.Card()
    newCard['translate'].setValue(translateVal)
    newCard['rotate'].setValue(rotateVal)
    newCard['lens_in_focal'].setValue(focalVal)
    newCard['lens_in_haperture'].setValue(hapertureVal)
    newCard['z'].setValue(3000)
    
    frameHoldNode = nuke.nodes.FrameHold()
    frameHoldNode['first_frame'].setValue(frameCount)
    
    newCard.setInput(0, frameHoldNode)
    frameHoldNode.setInput(0, theDot)

#createCard(frameCounter)

for n in range (1001, 1010):
    createCard(n)

    
sceneNode = nuke.nodes.Scene()
x = 0
for i in nuke.allNodes('Card'):
    sceneNode.setInput(x, i)
    x +=1
