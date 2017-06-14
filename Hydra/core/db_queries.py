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

import connect_db as con
from pprint import pprint


server = con.server
db = server.hydra


def get_statuses():
    check = False
    for n in db.utils.find():
        if "valid_statuses" in n:
            valid_statuses = n['valid_statuses']
            valid_statuses = [str(x) for x in valid_statuses]
            check = True
            break
    if check:
        return valid_statuses
    else:
        return None


def get_task_type():
    check = False
    for n in db.utils.find():
        if "task_type" in n:
            task_type = n['task_type']
            task_type = [str(x) for x in task_type]
            check = True
            break
    if check:
        return task_type
    else:
        return None


def get_all_shows():
    for n in db.shows.find({}, {'_id': False, 'sequences': False}):
        pprint(n)


def get_active_shows():
    for n in db.shows.find({"active": True}):
        pprint(n)


def get_seqs(show_name):
    seq_list = []
    show_id = db.shows.find_one({"name": show_name}).get("_id")
    for n in db.seqs.find({"show": show_id}):
        seq_list.append(str(n['name']))
    return seq_list


def get_shots(show_name, seq_name):
    shots_list = []
    try:
        show_id = db.shows.find_one({"name": show_name}).get("_id")
        seq_id = db.seqs.find_one({"name": seq_name}).get("_id")
        for n in db.shots.find({"show": show_id, "seq": seq_id}):
            shots_list.append(n)
        return shots_list
    except AttributeError:
        print "Please type a valid name for the show or the sequence"
        pass


def get_users_from_shot(shot_name):
    shot = db.shots.find_one({"name": shot_name})
    tasks = shot.get('tasks')
    users = [x['assignee'] for x in tasks]
    return users


def get_frame_range_from_shot(shot_name):
    shot = db.shots.find_one({"name": shot_name})
    frame_range = {"first": shot.get('frame_in'), "last": shot.get('frame_out')}
    return frame_range
