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
import datetime
import json

from Core.config import cyc_config as cfg

import boto3
import botocore

root = os.getenv('CYC_ROOT')


def convert_isotime_to_datetime(isotime_format):
    """ Description:
    all the timestamps in CycplopsVFX's Unity are formated in ISO 8601.ISO
    This function is helping to convert iso's string into a datetime object.

    Example of use:

    now = datetime.datetime.utcnow()
    >>> now
    datetime.datetime(2017, 5, 14, 1, 59, 39, 292000)
    now_isoformat = now.isoformat()
    >>> '2017-05-14T01:59:39.292000'
    dateNow = utils.convert_isotime_to_datetime(now_isoformat)
    >>> datetime.datetime(2017, 5, 14, 1, 59, 39, 292000)
    format = "%a %d %b %Y at %H:%M:%S"
    formated_dateNow = dateNow.strftime(format)
    print formated_dateNow
    >>> Sun 14 May 2017 at 01:59:39
    """
    dt, _, us = isotime_format.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


def check_s3(basename):

    s3 = boto3.resource('s3')
    exists = False

    try:
        s3.Object(cfg.BUCKET_NAME, basename).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            raise
    else:
        exists = True

    return exists


def json_to_dict(json_file):
    with open(json_file) as j:
        json_to_dict = json.load(j)
    return json_to_dict


def check_entity(submission_task):
    tasks_json = ('./Core/config/tasks.json')
    tasks_dict = json_to_dict(tasks_json)
    
    Asset_tasks = tasks_dict.get('asset_tasks')
    Shot_tasks = tasks_dict.get('shot_tasks')
    
    check = None

    for task in Asset_tasks:
        if task in submission_task:
            check = "asset"
            break

    if check == None:
        for task in Shot_tasks:
            if task in submission_task:
                check = "shot"
                break

    return check
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
