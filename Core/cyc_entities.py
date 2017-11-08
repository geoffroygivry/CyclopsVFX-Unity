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

# RBY_MANOR_010_lensFlare_nkScript_CMP_v02_2017-10-03T22:41:43.17900
# RBY_awning01_SHD_v03_2017-10-07T11:05:49.17900 for asset

import datetime
import os
# from Hydra.core import connect_db as con

# db = con.server.hydra


class Cyc_Publish(object):
    """ Description:
        This is the class for publishing assets and entities in the database. it takes the db as an initial argument.
    """

    def __init__(self, db, entity_type):
        self._db = db
        self.entity_type = entity_type
        self.show = os.getenv('SHOW')
        self.asset = None
        self.shot = os.getenv('SHOT')
        self.description = None
        self.task = os.getenv('TASK')
        self.version = None
        self.path = None
        self.script = None
        self.pub_date = None
        self.publisher = None
        self.comment = None
        self.first_frame = None
        self.last_frame = None
        self.tag = []

        print "intitializing Publish..."

    def set_show(self, show_name):
        self.show = show_name

    def get_show(self):
        return self.show

    def set_asset(self, asset_name):
        if self.entity_type == "asset":
            self.asset = asset_name

    def get_asset(self):
        if self.entity_type == "asset":
            return self.asset

    def set_shot(self, shot_name):
        if self.entity_type == "shot":
            self.shot = shot_name

    def get_shot(self):
        if self.entity_type == "shot":
            return self.shot

    def set_description(self, description_name):
        self.description = description_name

    def get_description(self):
        if self.entity_type == "shot":
            return self.description
        else:
            return

    def set_version(self, version_name):
        self.version = version_name

    def get_version(self):
        return self.version

    def set_task(self, task_name):
        self.task = task_name

    def get_path(self):
        return self.path

    def get_task(self):
        return self.task

    def set_path(self, path_name):
        self.path = path_name

    def set_script(self, script_name):
        self.script = script_name

    def get_script(self):
        return self.script

    def set_pub_date(self, pub_date_name):
        self.pub_date = pub_date_name

    def get_pub_date(self):
        return self.pub_date

    def set_publisher(self, publisher_name):
        self.publisher = publisher_name

    def get_publisher(self):
        return self.publisher

    def set_comment(self, comment_name):
        self.comment = comment_name

    def get_comment(self):
        return self.comment

    def set_first_frame(self, first_frame_name):
        self.first_frame = first_frame_name

    def get_first_frame(self):
        return self.first_frame

    def set_last_frame(self, last_frame_name):
        self.last_frame = last_frame_name

    def get_last_frame(self):
        return self.last_frame

    def set_tag(self, tag_name):
        self.tag.append(tag_name)

    def get_tag(self):
        return self.tag

    def generate_UUID(self):
        if self.entity_type == "shot":
            if self.show is not None and self.shot is not None and self.description is not None and self.task is not None and self.version is not None:
                return "{}_{}_{}_{}_v{}_{}".format(self.show, self.shot, self.description, self.task, self.version, datetime.datetime.utcnow().isoformat())
        if self.entity_type == "asset":
            if self.show is not None and self.asset is not None and self.task is not None and self.version is not None:
                return "{}_{}_{}_{}_v{}_{}".format(self.show, self.asset, self.task, self.version, datetime.datetime.utcnow().isoformat())
