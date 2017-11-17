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

from connect_db import server
from Core.utils import cyc_utils as cyc
from bson.objectid import ObjectId
import datetime

# connect to Hydra's mongodb database
db = server.hydra


def push_notifications(publisher, suscribers, type_, shotname, isodate):
    """ Description:
        This is the main function that pushes the user notifications within Unity and Polyphemus. Notifications have an expiring date: they are store in the database for a month.

        Arguments:
        It takes a publisher as a dictionary with a name and an email of the one who pushed the notification, it takes a type of notification mostly for the message that will be displayed : e .g. type "dailies" : New Dailies Submissions
        for <shot> or type "publish": New Item Published : <assetName>, a shot or asset name and an isodate. It also takes a list of suscribers to receive these notifications.

        Example of usage:
        import notifications
        notifications.push_notifications({"name": "Geoff", "email": "geoff@example.com"}, ['user1', 'user2', 'user3'], "dailies", "MANOR_010", "2017-06-27T14:44:02.191Z")
    """
    datetime_now = cyc.convert_isotime_to_datetime(isodate)
    month_later = datetime_now + datetime.timedelta(+30)

    _id = db.notifications.insert(
        {"publisher": publisher, "type": type_, "shot": shotname, "expireAt": month_later, "date": isodate}
    )

    for suscriber in suscribers:
        db.users.update(
            {"name": suscriber},
            {"$inc": {"notifications": 1}}
        )
        db.users.update(
            {"name": suscriber},
            {"$push": {"notifications_msg": ObjectId(_id)}}
        )
