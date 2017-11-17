# The MIT License (MIT)
#
# Copyright (c) 2017 Geoffroy Givry
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
import nukescripts
from Core.config import extensions as ext
from Apps.Brontes.Controller import brontes_controller
from Core.utils import cyc_utils as utils


class Brontes_nuke(brontes_controller.Brontes):
    def __init__(self):
        super(Brontes_nuke, self).__init__()


def float_in_nuke():
    float_in_nuke.panel = Brontes_nuke()
    float_in_nuke.panel.show()


def dock_in_nuke():
    import nuke
    from nukescripts import panels
    pane = nuke.getPaneFor("io.cyclopsvfx.Brontes_nuke")
    panels.registerWidgetAsPanel('nuke_brontes.Brontes_nuke', 'Brontes_nuke',
                                 'io.cyclopsvfx.Brontes_nuke', True).addToPane(pane)


def dropper(mimeType, text):
    from Hydra.core import connect_db as con
    db = con.server.hydra
    if mimeType == 'text/plain':
        asset = db.publish.find_one({"UUID": text})
        UUID_obj = utils.UUID(text, "shot")
        if asset is not None:
            asset_path = asset.get('path')
            filename, file_extension = os.path.splitext(asset_path)
            if file_extension in ext.valid_2D_ext:
                asset_path = asset_path.replace(asset_path.split('.')[-2], "%04d")
                asset_first = asset.get('first_frame')
                asset_last = asset.get('last_frame')
                nuke.createNode('Read', 'file {0} first {1} last {2} origfirst {1} origlast {2}'.format(asset_path, asset_first, asset_last))
            if file_extension in ext.valid_scripts:
                if asset_path is not None:
                    print asset
                    nuke.scriptSource(asset_path)
            if file_extension in ext.valid_geos:
                nuke.createNode('ReadGeo2', 'file {}'.format(asset_path))
            if file_extension in ext.valid_cams and UUID_obj.task() == "CAM":
                nuke.createNode('Camera2', 'file {}'.format(asset_path))
            print asset_path
            return True
        else:
            return False
    return False
