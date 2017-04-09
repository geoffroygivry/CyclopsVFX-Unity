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

nameLabel = ""
enumerationPulldown = " 20 35 42 55 "
enumerationColour = " Grey Blue Green Yellow"

def autoBackdrop():

  global nameLabel, enumerationPulldown, enumerationColour
  selNodes = nuke.selectedNodes()
  if not selNodes:
    return nuke.nodes.BackdropNode()


  
  p = nuke.Panel('Label')
  p.addSingleLineInput("Label Name", nameLabel)
  p.addEnumerationPulldown("Font Size:", enumerationPulldown)
  p.addEnumerationPulldown("Colour:", enumerationColour)
  result = p.show()
  nameLabel = p.value("Label Name")
  enumVal = p.value("Font Size:")
  enumCol = p.value("Colour:")
  if enumCol == "Grey":
    r = 0.267
    g = 0.267
    b = 0.267
  if enumCol == "Blue":
    r = 0.373
    g = 0.482
    b = 0.533
  if enumCol == "Green":
    r = 0.318
    g = 0.447
    b = 0.302
  if enumCol == "Yellow":
    r = 0.533
    g = 0.525
    b = 0.282
  if enumCol == None:
    r = 0.18
    g = 0.18
    b = 0.18
  hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)


  # Calculate bounds for the backdrop node.
  bdX = min([node.xpos() for node in selNodes])
  bdY = min([node.ypos() for node in selNodes])
  bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
  bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY
  
  # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
  left, top, right, bottom = (-100, -100, 100, 100)
  bdX += left
  bdY += top
  bdW += (right - left)
  bdH += (bottom - top)

  if enumCol == None:
    pass
  else:
   
    n = nuke.nodes.BackdropNode(xpos = bdX,
    bdwidth = bdW,
    ypos = bdY,
    bdheight = bdH,
    note_font = 'Arial Black',
    label = nameLabel,
    note_font_size=enumVal,
    name = nameLabel,
    tile_color = hexColour,
    gl_color = hexColour)

                    

  # revert to previous selection

    n['selected'].setValue(False)
    for node in selNodes:
      node['selected'].setValue(True)
 
    return n
