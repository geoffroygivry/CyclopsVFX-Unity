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


def create_show(long_name, code_name):
    """ Creation of a show entity.
    The show has 2 names: the normal name and the code name which is normally no
    more than 3 letters or numbers.
    It also creates empty lists of both sequences and shots for future creations.
    Example of use:
        create_show("RUBBISHBOY", "RBY")
    """
    db.shows.insert(
        {
            "name": code_name,
            "long_name": long_name,
            "sequences": [],
            "active": True
        }
    )


def create_seq(show_name, seq_name):
    """ creates a sequence entity for the show passed in the first argument.
    It must pass the code or short name and not the long name.
    Example of usage:
        create_seq("RBY", "MANOR")
    """
    show_id = db.shows.find_one({"name": show_name}).get("_id")
    db.seqs.insert(
        {
            "name": seq_name,
            "show": show_id
        }
    )
    db.shows.update(
        {'name': show_name},
        {'$push': {'sequences': {"name": seq_name, "shots": []}}}
    )


def create_shot(show_name, seq_name, shot_name, frame_in=1001, frame_out=1001,
                tasks=[], status="NOT STARTED", target_date=None):
    """ creates a shot entity within the show an the sequence.
    it takes some arguments like the show name, the sequence name, the shot name
    the first frame and the last frame.
    By default, the shot is created with a frame range of 1 frame starting at
    1001 and a status of "NOT STARTED" and a blank target date.
    Example of usage:
        create_shot("RBY", "MANOR", "MANOR_010", frame_in=1001, frame_out=1067)
    """
    show_id = db.shows.find_one({"name": show_name}).get("_id")
    seq_id = db.seqs.find_one({"name": seq_name}).get("_id")
    db.shots.insert(
        {
            "name": shot_name,
            "show": show_id,
            "seq": seq_id,
            "frame_in": frame_in,
            "frame_out": frame_out,
            "tasks": tasks,
            "status": status,
            "target_date": target_date
        }
    )
    shot_id = db.shots.find_one({"name": shot_name}).get("_id")
    db.shows.update(
        {'name': show_name, 'sequences.name': seq_name},
        {'$push':
         {'sequences.$.shots': {"name": shot_name, "shot_id": shot_id}}
         }
    )


def add_task(shot_name, task_type, assignee):
    """ This function is used only for adding tasks to shots."""
    user_id = db.users.find_one({"name": assignee}).get("_id")
    db.shots.update(
        {"name": shot_name},
        {"$push":
         {"tasks": {task_type: user_id}}
         }
    )


def update_shot_status(shot_name, status):
    """ update the status of the given shot."""
    valid_statuses = ["NOT_STARTED", "IN_PROGRESS", "ON_HOLD", "CANCELLED",
                      "CREATIVE_APPROVED", "FINAL_PENDING_TECH_CHECK", "FINAL"]
    for n in valid_statuses:
        if status in n:
            db.shots.update(
                {"name": shot_name},
                {"$push":
                 {"status": status}
                 }
            )


def update_shot_target_date(shot_name, target_date):
    """ Update the target date of the shot"""
    db.shots.update(
        {"name": shot_name},
        {"$push":
         {"target_date": target_date}
         }
    )


def set_active_show(show_name, true_or_false):
    db.shows.update(
        {"name": show_name},
        {"$set":
         {"active": true_or_false}
         }
    )
