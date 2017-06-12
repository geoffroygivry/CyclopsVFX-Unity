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
import datetime
import boto3
from boto3.s3.transfer import S3Transfer

from Core.config import cyc_config as cfg
from Core import ptuid
import notifications
import db_queries as dbq
import connect_db as con

# server = MongoClient(cfg.MONGODB)
now = datetime.datetime.utcnow().isoformat()


def get_connection():
    server = con.server
    db = server.hydra
    return db


def send_to_S3(img):
    transfer = S3Transfer(boto3.client('s3', cfg.AWS_REGION, aws_access_key_id=cfg.ACCESS_KEY_ID, aws_secret_access_key=cfg.ACCESS_SECRET_KEY))
    transfer.upload_file(img, cfg.BUCKET_NAME, os.path.basename(img), extra_args={'ACL': 'public-read'})


def sendToDailies(path, comments, bkp_script, firstFrame, lastFrame, thumb, show=os.getenv('JOB'), shot=os.getenv('SHOT'), seq=os.getenv('SEQ'), task=os.getenv('TASK'), status="WORK IN PROGRESS"):
    """ function to create a new dailies submission
    example :
    from Hydra.core import submissions
    submissions.sendToDailies('this/is/the/path', 'this is the comment', 'this/is/the/bkp_script', 'frame-range')
    """
    # db = server['hydra']

    db = get_connection()
    dailiesCollections = db['submissions']
    new_ptuid = ptuid.ptuid(show, shot, task)
    # creation of the dailies submission entry
    Submission = dict()
    Submission['Date'] = now
    Submission['type'] = "dailies"
    Submission['status'] = status
    Submission['timestamp'] = datetime.datetime.utcnow()
    Submission['Show'] = show
    Submission['seq'] = seq
    Submission['Username'] = os.getenv('USERNAME')
    Submission['Task'] = task
    Submission['ptuid'] = new_ptuid
    if Submission['Task'] == 'CreText' or Submission['Task'] == 'CreMod' or Submission['Task'] == 'EnvText' or Submission['Task'] == 'EnvMod' or Submission['Task'] == 'EnvShader' or Submission['Task'] == 'CreShader' or Submission['Task'] == 'CreRig' or Submission['Task'] == 'PropMod' or Submission['Task'] == 'PropText' or Submission['Task'] == 'PropShader' or Submission['Task'] == 'PropRig':
        Submission['AssetName'] = 'MainWall'
    else:
        Submission['Shot'] = shot
        Submission['first_frame'] = firstFrame
        Submission['last_frame'] = lastFrame
    Submission['bkp_script'] = bkp_script
    Submission['Path'] = path
    Submission['comment'] = comments
    Submission['thumbnail'] = thumb
    Submission['thumbnail_s3'] = "https://s3.amazonaws.com/cyclopsvfx/" + os.path.basename(thumb)
    dailiesCollections.save(Submission)
    send_to_S3(thumb)
    users_list = dbq.get_users_from_shot(shot)
    notifications.push_notifications({"name": os.getenv('USERNAME'), "email": os.getenv('USER_EMAIL')}, users_list, "dailies", shot, now)


def PublishIt(name, path, comments, task=os.getenv('TASK'), status="WORK IN PROGRESS"):
    """ module to create a new Publish submission
    example :
    from Hydra.core import submissions
    submissions.PublishIt('MainWall', 'this/is/the/path', 'this is the comment')
    """

    db = get_connection()

    PubCollections = db['submissions']

    # creation of the dailies submission entry
    publishDict = dict()
    publishDict['Date'] = now
    publishDict['type'] = "publish"
    publishDict['Username'] = os.getenv('USERNAME')
    publishDict['Task'] = task
    publishDict['status'] = status
    publishDict['AssetName'] = name
    publishDict['Path'] = path
    publishDict['comment'] = comments
    PubCollections.save(publishDict)
    notifications.push_notifications({"name": os.getenv('USERNAME'), "email": os.getenv('USER_EMAIL')}, users_list, "publish", shot, now)


def submit_note(note, show=None, seq=None, shot=None):
    """ Description:
        Function that is used to create a note form the user at show or seq or shot level.
        Note that you can not use more than one parameters for show/seq/shot.

        Example of usage:

        from Hydra.core import submissions
        submissions.submit_note(show="RBY", "we are sending a note for the show")
        or
        submissions.submit_note(seq="MANOR", "we are sending a note for the sequence")
        or
        submissions.submit_note(shot="MANOR_010", "we are sending a note for the shot")

    """
    db = get_connection()
    if show is not None:
        db.submissions.insert(
            {"publisher": {"name": os.getenv('USERNAME'), "email": os.getenv('USER_EMAIL')},
                "show": show,
                "note": note,
                "type": "note",
                "date": now
             }
        )
    elif seq is not None:
        db.submissions.insert(
            {"publisher": {"name": os.getenv('USERNAME'), "email": os.getenv('USER_EMAIL')},
                "seq": seq,
                "note": note,
                "type": "note",
                "date": now
             }
        )
    else:
        db.submissions.insert(
            {"publisher": {"name": os.getenv('USERNAME'), "email": os.getenv('USER_EMAIL')},
                "shot": shot,
                "note": note,
                "type": "note",
                "date": now
             }
        )
