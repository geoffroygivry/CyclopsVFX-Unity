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


def makeThumbnail():
  frameFirst = str('%0*d' % (4, int(nuke.Root()['first_frame'].value())))
  for node in nuke.allNodes('Write'):
    fileName = node['file'].value()
    FirstFramefileName = fileName.replace("%04d", frameFirst)
    NewFileName = fileName.rsplit('/', 1)[0] + '/.' + node['file'].value().split('/')[-1]
    FirstFrameNewFileName = NewFileName.replace("%04d", "thumbnail")
    ext = FirstFrameNewFileName.split('.')[-1]
    FirstFrameNewFileName = FirstFrameNewFileName.replace(ext, "jpg")
    ThePath = os.getenv("CYC_ENGINE_NUKE") + '/NukeTools_1.01'
    TheNukeVersion = os.getenv('NUKEVERSION')
    if platform.system() == 'Linux':
      IMCmd = (('nuke -t %s/Python/convert.py %s %s') % (ThePath, FirstFramefileName, FirstFrameNewFileName))
    else:
      IMCmd = (('nuke%s -t %s/Python/convert.py %s %s') % (TheNukeVersion, ThePath, FirstFramefileName, FirstFrameNewFileName))
    os.system(IMCmd)
    print "the file: ", FirstFrameNewFileName, "has been created!"


def justThumPath():
  node = nuke.toNode("Write1")
  fileName = node['file'].value()
  NewFileName = fileName.rsplit('/', 1)[0] + '/.' + node['file'].value().split('/')[-1]
  FirstFrameNewFileName = NewFileName.replace("%04d", "thumbnail")
  ext = FirstFrameNewFileName.split('.')[-1]
  FirstFrameNewFileName = FirstFrameNewFileName.replace(ext, "jpg")
  return FirstFrameNewFileName
