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

import unity
from Core.config import cyc_config as cfg
from Hydra.core import connect_db as con

db = con.server.hydra


class Model():

    def get_all_latest_publish_shot(self, show_name, shot_name):
        return unity.get_response("{}/api/unity/{}/{}?published=latest".format(cfg.POLY_SERVER, show_name, shot_name))

    def get_all_publish_shot(self, show_name, shot_name):
        return unity.get_response("{}/api/unity/{}/{}?published=all".format(cfg.POLY_SERVER, show_name, shot_name))

    def get_latest_publish_by_task(self, show_name, shot_name, task_name):
        return unity.get_response("{}/api/unity/{}/{}?published=latest&task={}".format(cfg.POLY_SERVER, show_name, shot_name, task_name))

    def get_all_publish_by_task(self, show_name, shot_name, task_name):
        return unity.get_response("{}/api/unity/{}/{}?published=all&task={}".format(cfg.POLY_SERVER, show_name, shot_name, task_name))

    def get_unity_response(self, url):
        return unity.get_response(url)

    def get_active_shows(self):
        return [x.get('name') for x in db.shows.find({"active": True})]

    def get_seqs(self, show_name):
        return [x.get('name') for x in db.seqs.find({"show": show_name})]

    def get_shots(self, show_name, seq_name):
        return [x.get('name') for x in db.shots.find({"show": show_name, "seq": seq_name})]

    def get_publish(self, UUID_name):
        return db.publish.find_one({"UUID": UUID_name})
