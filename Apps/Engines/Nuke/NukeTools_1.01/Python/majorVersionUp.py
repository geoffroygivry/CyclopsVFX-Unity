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

geoffPath = os.getenv("SHOW_PATH")
shot = os.environ['SHOT']
job = os.environ['JOB']
task = os.getenv('TASK')

def majorVersionUp():

    if not nuke.root()['name'].value() == "":
	version = int(nuke.root()['name'].value().split('/')[-1].split('v')[1].split('_')[0])
	baseFile = nuke.root()['name'].value().split('/')[-1].split('v')[0]
	baseFile0 = '%s/%s/%s/TASKS/%s/Work/Nuke/' % (geoffPath, job, shot, task)
	versionUp = version + 1
	newFile = baseFile0  + '%sv%03d_01.nk' % (baseFile, versionUp)
	nuke.scriptSaveAs(newFile,0)
    else:
	nuke.message('please choose a script to save first')
	pass
