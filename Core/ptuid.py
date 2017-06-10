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

from Hydra.core import connect_db as con

db = con.server.hydra


def get_current_ptuid(show_name):
    ptuid = db.shows.find_one({"name": show_name}).get('ptuid')
    return ptuid


def generate_ptuid(show_name, task):
    ptuid = get_current_ptuid(show_name)
    get_full_ptuid = "%s-%s-%06d" % (show_name, task, ptuid)
    return get_full_ptuid


def update_ptuid(show_name):
    db.shows.update({"name": show_name}, {'$inc': {"ptuid": 1}})


def ptuid(show_name, task):
    get_current_ptuid(show_name)
    final_ptuid = generate_ptuid(show_name, task)
    update_ptuid(show_name)
    return final_ptuid
