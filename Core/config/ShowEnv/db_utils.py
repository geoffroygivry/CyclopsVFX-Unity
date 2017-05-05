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

from pymongo import MongoClient
from Core.config import cyc_config as cfg

server = MongoClient(cfg.MONGODB)
db = server['hydra']


def create_show(show_name):
    shows_collection = db['shows']

    new_show = {}
    new_show['name'] = show_name
    shows_collection.save(new_show)


def create_seq(show_name, seq_name):
    db.shows.update(
        {'name': show_name},
        {'$push':
         {'sequences': {"name": seq_name, "shots": []}}
         }
    )


def create_shot(show_name, seq_name, shot_name, frame_in, frame_out, tasks):
    db.shows.update(
        {'name': show_name, "sequences.name": seq_name},
        {'$push':
         {'sequences.$.shots': {"name": shot_name, "frame_in": frame_in, "frame_out": frame_out, "tasks": tasks}}
         }
    )
