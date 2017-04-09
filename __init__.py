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

import os
# main environment variables setup here. Note this is the version 0.01. might change a bit later.

os.environ['CYC_ROOT'] = os.path.dirname(os.path.abspath(__file__))
os.environ['CYC_HYDRA_PATH'] = os.path.join(os.environ['CYC_ROOT'], 'hydra')
os.environ['CYC_CORE_PATH'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config')
os.environ['CYC_NUKE_ENV'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config/NukeEnv')
os.environ['CYC_MAYA_ENV'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config/MayaEnv')
os.environ['CYC_RV_ENV'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config/RVEnv')
os.environ['CYC_MARI_ENV'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config/MariEnv')
os.environ['CYC_3DE_ENV'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config/3DeEnv')
os.environ['CYC_CLARISSE_ENV'] = os.path.join(os.environ['CYC_ROOT'], 'Core/config/ClarisseEnv')
os.environ['CYC_POLYPHEMUS_PATH'] = os.path.join(os.environ['CYC_ROOT'], 'Apps/Polyphemus')
os.environ['CYC_STEROPES_PATH'] = os.path.join(os.environ['CYC_ROOT'], 'Apps/Steropes')
os.environ['CYC_ENGINE_NUKE'] = os.path.join(os.environ['CYC_ROOT'], 'Apps/Engines/Nuke')