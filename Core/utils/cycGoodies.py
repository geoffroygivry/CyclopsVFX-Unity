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
import re
import pyseq

root = os.getenv('CYC_ROOT')


class listMyDir(object):

    """simple module to quickly print the content of a directory or creating a list from it. Here is the method :

    from Core.utils.cycGoodies import listMyDir
    emptyList = []
    listit = listMyDir('/Dropbox/jobs/Babiru3D/OUT_001/OUT/OUT_001_v001_comp')
    listit.ListThisDir(emptyList)

    to print the __doc__:
    print listD.listMyDir.__doc__

    """

    def __init__(self, path):

        self.__doc__ = "there are 2 methods one to print the folder in a nice way and the other to append into a list what's in the folder"

        self.path = path

    def printThisDir(self):
        for i in os.listdir(self.path):
            print i

    def ListThisDir(self, dirList):
        for r in os.listdir(self.path):
            dirList.append(r)


def getVersion(filename):
    """ This function will search for the int version number if there is a v or V in the string"""

    match = re.findall('[vV]([0-9]+)', filename)
    return int(match[-1]) if match else 0


def setSequence(path):
    empty = []
    listimg = os.listdir(path)
    for n in listimg:
        try:
            if n[0] != '.':
                empty.append(n)
        except IndexError:
            pass
    for j in empty:
        if j.split(".")[-1] == 'exr' or j.split(".")[-1] == 'jpg' or j.split(".")[-1] == 'tif' or j.split(".")[-1] == 'tga':
            s = pyseq.Sequence(empty)
            return s
        else:
            None
