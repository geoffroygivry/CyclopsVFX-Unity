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
import sys

os.environ['NUKETOOLSVERSION'] = '1.01'
NukeMenuVersion = os.environ['NUKETOOLSVERSION']
os.environ['NUKEVERSION'] = "9.0"
os.environ['GEOFF_PATH'] = os.getenv("SHOW_PATH")


def NukePythonPath():

    sys.path.append('/Python27/Lib/site-packages')
    print "\n==========================="
    nukeIntitialPath = os.getenv('CYC_ENGINE_NUKE')
    nuke.pluginAddPath(os.path.join(nukeIntitialPath, 'NukeCallbacks'))
    print "%s/NukeCallbacks Path added" % (nukeIntitialPath)
    nuke.pluginAddPath('%s/NukeTools_%s' % (nukeIntitialPath, NukeMenuVersion))
    print "%s/NukeTools_%s Path added" % (nukeIntitialPath, NukeMenuVersion)
